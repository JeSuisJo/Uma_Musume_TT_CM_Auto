"""The object pywebview exposes to JavaScript as ``window.pywebview.api``.

Every method here is callable from the HTML page. Config read/write goes through
:mod:`json` directly (never ``umauto.config``) so the config screen works before
config.json exists. The heavy backend (features pull in OpenCV/NumPy; building
the driver can restart ADB) warms up in a background thread so no UI call blocks
the window; until it is ready ``list_features`` reports ``loading``.
"""

import contextlib
import json
import os
import threading

from ..paths import resolve
from . import schema
from .runtime import session

CONFIG_PATH = resolve("config.json")


def _load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            data = json.load(f)
        # Backfill any key missing from an older file so the form is complete.
        merged = schema.defaults()
        merged.update(data)
        return merged, True
    return schema.defaults(), False


def _refresh_live_config():
    """Push the on-disk config into an already-imported ``umauto.config``.

    Features read config values at run time from a single object loaded once at
    import. After the user edits and saves, we update that object in place so
    non-platform changes (difficulty, shop, champion...) take effect without a
    restart. A platform switch (Steam <-> ADB) still needs a restart because the
    driver is chosen at import; the UI warns about that.
    """
    import sys

    cfg = sys.modules.get("umauto.config")
    if cfg is None:
        return
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg.config._data = json.load(f)


class Api:
    def __init__(self):
        self._window = None
        self._saved_geom = None  # window geometry to restore after a run
        # Platform the driver/coords were built with at startup. Changing it
        # can't be done live (they are import-time singletons wired into many
        # modules), so a switch relaunches the app instead.
        self._startup_steam = bool(_load_config()[0].get("steam", False))
        # Topmost is held only while a mode runs (Steam only); this event stops
        # the thread that keeps re-asserting it.
        self._topmost_stop = None
        # Background backend warm-up state.
        self._features = None
        self._warm_started = False
        self._warm_done = False
        self._warm_error = None
        self._start_warmup()

    def _overlay_wanted(self):
        """True when the running window should float over the game: Steam only
        (in ADB mode the game isn't on this screen) and only if opted in."""
        cfg, _ = _load_config()
        return bool(cfg.get("steam") and cfg.get("window_on_top"))

    def _apply_topmost(self, on):
        """Set/clear the Win32 topmost style on our window.

        pywebview's ``on_top`` isn't enough here: the game raises itself and
        pushes us behind, so we set WS_EX_TOPMOST ourselves and re-assert it.
        SWP_NOACTIVATE keeps focus on the game while we do it.
        """
        try:
            import win32con
            import win32gui

            hwnd = win32gui.FindWindow(None, "Uma Auto")
            if not hwnd:
                return
            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_TOPMOST if on else win32con.HWND_NOTOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE,
            )
        except Exception:
            pass

    def _hold_topmost(self):
        """Keep the window topmost for as long as the mode runs.

        A single SetWindowPos loses to the game reclaiming the foreground, so a
        background thread re-asserts it until the run ends.
        """
        self._release_topmost()
        stop = threading.Event()
        self._topmost_stop = stop

        def loop():
            while not stop.wait(1.0):
                self._apply_topmost(True)

        self._apply_topmost(True)
        threading.Thread(target=loop, daemon=True).start()

    def _release_topmost(self):
        if self._topmost_stop is not None:
            self._topmost_stop.set()
            self._topmost_stop = None
            self._apply_topmost(False)

    def _snap_to_run_placement(self):
        """Move/resize the window to the game-overlay placement and pin it on
        top, saving the current geometry so it can be restored when the run ends.

        Only overlays the game on Steam with always-on-top enabled; in ADB mode
        (or without on-top) the window stays where it is.
        """
        if self._window is None or not self._overlay_wanted():
            return
        try:
            import win32gui

            from .app import _placement

            hwnd = win32gui.FindWindow(None, "Uma Auto")
            if hwnd:
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                self._saved_geom = {
                    "x": left, "y": top,
                    "width": right - left, "height": bottom - top,
                }
            geom = _placement()
            if "width" in geom and "height" in geom:
                self._window.resize(geom["width"], geom["height"])
            if "x" in geom and "y" in geom:
                self._window.move(geom["x"], geom["y"])
        except Exception:
            pass
        self._hold_topmost()

    def restore_window(self):
        """Put the window back to its pre-run size/position and drop topmost."""
        self._release_topmost()
        if self._window is not None and self._saved_geom:
            try:
                g = self._saved_geom
                self._window.resize(g["width"], g["height"])
                self._window.move(g["x"], g["y"])
            except Exception:
                pass
            self._saved_geom = None
        return {"ok": True}

    def _start_warmup(self):
        """Import the features registry + build the driver off the UI thread."""
        if self._warm_started or not os.path.exists(CONFIG_PATH):
            return
        self._warm_started = True
        threading.Thread(target=self._warmup, daemon=True).start()

    def _warmup(self):
        try:
            from ..features.registry import FEATURES

            self._features = [{"key": k, "label": f.label} for k, f in FEATURES.items()]
        except Exception as exc:  # broken config, missing driver deps, etc.
            self._warm_error = str(exc)
        finally:
            self._warm_done = True

    def get_schema(self):
        config, exists = _load_config()
        return {"fields": schema.FIELDS, "config": config, "config_exists": exists}

    def save_config(self, data):
        # Keep only known keys, coercing to the right shape from the schema.
        clean = {}
        for field in schema.FIELDS:
            key = field["key"]
            if key in data:
                clean[key] = data[key]
        existing, _ = _load_config()
        existing.update(clean)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)
        _refresh_live_config()
        # "Always on top" only applies to a running mode, so a change mid-run
        # takes effect now; outside a run there is nothing to pin.
        if session.running:
            if self._overlay_wanted():
                self._hold_topmost()
            else:
                self._release_topmost()
        # A fresh install just created config.json: kick off the warm-up now.
        self._start_warmup()
        # Switching Steam <-> ADB rebuilds the whole game-control layer, which
        # can't be swapped live, so relaunch the app to pick it up.
        platform_changed = bool(existing.get("steam", False)) != self._startup_steam
        if platform_changed and self._window is not None:
            threading.Timer(0.4, self._restart).start()
        return {"ok": True, "restarting": platform_changed}

    def _restart(self):
        """Relaunch the app in a fresh process, then close this one."""
        import subprocess
        import sys

        try:
            subprocess.Popen([sys.executable, "-m", "umauto.gui"], close_fds=True)
        except Exception:
            return  # relaunch failed: keep the current window open
        with contextlib.suppress(Exception):
            self._window.destroy()

    def list_features(self):
        if not os.path.exists(CONFIG_PATH):
            return {"ready": False, "loading": False, "features": []}
        if not self._warm_done:
            return {"ready": False, "loading": True, "features": []}
        if self._warm_error:
            return {"ready": False, "loading": False, "features": [],
                    "error": self._warm_error}
        return {"ready": True, "loading": False, "features": self._features or []}

    def run_feature(self, key):
        if session.running:
            return {"started": False, "reason": "busy"}
        started = session.start(key)
        if started:
            self._snap_to_run_placement()
        return {"started": started}

    def stop_feature(self):
        session.request_stop()
        return {"ok": True}

    def submit_prompt(self, value):
        session.answer_prompt(value)
        return {"ok": True}

    def poll(self):
        return {
            "running": session.running,
            "log": session.drain_log(),
            "prompt": session.pending_prompt(),
        }
