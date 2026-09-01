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
        merged = schema.defaults()
        merged.update(data)
        return merged, True
    return schema.defaults(), False


def _refresh_live_config():
    import sys

    cfg = sys.modules.get("umauto.config")
    if cfg is None:
        return
    with open(CONFIG_PATH, encoding="utf-8") as f:
        cfg.config._data = json.load(f)


class Api:
    def __init__(self):
        self._window = None
        self._saved_geom = None
        self._startup_steam = bool(_load_config()[0].get("steam", False))
        self._topmost_stop = None
        self._features = None
        self._warm_started = False
        self._warm_done = False
        self._warm_error = None
        self._start_warmup()

    def _overlay_wanted(self):
        cfg, _ = _load_config()
        return bool(cfg.get("steam") and cfg.get("window_on_top"))

    def _apply_topmost(self, on):
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
        if self._warm_started or not os.path.exists(CONFIG_PATH):
            return
        self._warm_started = True
        threading.Thread(target=self._warmup, daemon=True).start()

    def _warmup(self):
        try:
            from ..features.registry import FEATURES

            self._features = [{"key": k, "label": f.label} for k, f in FEATURES.items()]
        except Exception as exc:
            self._warm_error = str(exc)
        finally:
            self._warm_done = True

    def get_schema(self):
        config, exists = _load_config()
        return {"fields": schema.FIELDS, "config": config, "config_exists": exists}

    def save_config(self, data):
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
        if session.running:
            if self._overlay_wanted():
                self._hold_topmost()
            else:
                self._release_topmost()
        self._start_warmup()
        platform_changed = bool(existing.get("steam", False)) != self._startup_steam
        if platform_changed and self._window is not None:
            threading.Timer(0.4, self._restart).start()
        return {"ok": True, "restarting": platform_changed}

    def _restart(self):
        import subprocess
        import sys

        try:
            subprocess.Popen([sys.executable, "-m", "umauto.gui"], close_fds=True)
        except Exception:
            return
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
