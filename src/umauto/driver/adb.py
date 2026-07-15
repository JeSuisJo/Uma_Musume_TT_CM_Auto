"""ADB driver: controls an Android emulator/device via platform-tools/adb."""

import contextlib
import json
import subprocess
import sys
import time

from ..config import config
from ..paths import PROJECT_ROOT, resolve
from .base import Driver

_ADB = resolve("platform-tools/adb.exe")

# When the app runs under pythonw.exe (no console, e.g. the GUI), each adb.exe
# call would otherwise pop up its own console window. CREATE_NO_WINDOW keeps
# those child processes headless so no cmd windows flash during a run.
_NO_WINDOW = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0


def _save_device_id(device_id):
    """Persist the resolved device to config.json and the live config."""
    path = resolve("config.json")
    with contextlib.suppress(OSError, ValueError):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        data["device_id"] = device_id
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    config._data["device_id"] = device_id


class AdbDriver(Driver):
    def __init__(self):
        # The real device is resolved lazily in ensure_ready() (run start), so
        # importing the driver never blocks on adb.
        self.device = config.get("device_id")

    @staticmethod
    def _list_devices():
        result = subprocess.run(
            [_ADB, "devices"], capture_output=True, text=True, timeout=10,
            creationflags=_NO_WINDOW,
        )
        lines = [
            line for line in result.stdout.strip().split("\n")[1:] if "\tdevice" in line
        ]
        return [line.split("\t")[0] for line in lines]

    @staticmethod
    def _restart_server():
        subprocess.run(
            [_ADB, "kill-server"], capture_output=True, timeout=10,
            creationflags=_NO_WINDOW,
        )
        time.sleep(1)
        subprocess.run(
            [_ADB, "start-server"], capture_output=True, timeout=15,
            creationflags=_NO_WINDOW,
        )
        time.sleep(2)

    def _use_device(self, device_id, note):
        self.device = device_id
        _save_device_id(device_id)
        print(f"{note}: {device_id}")

    @staticmethod
    def _ask_device(devices):
        print("Multiple devices connected:")
        for i, device in enumerate(devices, 1):
            print(f"  [{i}] {device}")
        while True:
            answer = input("Select device (number): ").strip()
            if answer.isdigit() and 1 <= int(answer) <= len(devices):
                return devices[int(answer) - 1]
            print(f"  Please enter a number between 1 and {len(devices)}.")

    def _is_online(self, device_id):
        """True if a specific device is connected (direct check, no full scan)."""
        result = subprocess.run(
            [_ADB, "-s", device_id, "get-state"], capture_output=True, text=True,
            timeout=10, creationflags=_NO_WINDOW,
        )
        return result.returncode == 0 and result.stdout.strip() == "device"

    def ensure_ready(self):
        """Resolve the ADB device before a run.

        Trusts the saved device when it is still online (no detection at all);
        only scans/auto-selects/asks when the configured device is missing.
        """
        configured = config.get("device_id")

        # Saved device still online -> use it directly, skip detection entirely.
        if configured and self._is_online(configured):
            self.device = configured
            return

        # Saved device missing (or none saved): now detect what is connected.
        devices = self._list_devices()

        # Exactly one device -> adopt and remember it.
        if len(devices) == 1:
            self._use_device(devices[0], "ADB device auto-selected")
            return

        # None found: try restarting the ADB server once, then re-check.
        if not devices:
            print("No ADB device found, restarting ADB server...")
            self._restart_server()
            devices = self._list_devices()
            if configured and configured in devices:
                self.device = configured
                return
            if len(devices) == 1:
                self._use_device(devices[0], "ADB device auto-selected")
                return

        # Still nothing: cannot run without a device.
        if not devices:
            self.stop("No emulator detected. Start your emulator, then try again.")

        # Several devices. Ask only when nothing was configured; otherwise the
        # configured entry is stale, so adopt the first without prompting.
        if configured:
            self._use_device(devices[0], "ADB device auto-updated")
        else:
            self._use_device(self._ask_device(devices), "ADB device selected")

    def _run(self, args):
        base = [_ADB, "-s", self.device] if self.device else [_ADB]
        result = subprocess.run(
            base + args, capture_output=True, text=True, timeout=30,
            cwd=PROJECT_ROOT, creationflags=_NO_WINDOW,
        )
        return result.returncode == 0

    def _exec_out(self, args):
        """Run ``adb exec-out`` and return its raw stdout (empty on failure)."""
        base = [_ADB, "-s", self.device] if self.device else [_ADB]
        result = subprocess.run(
            base + ["exec-out"] + args, capture_output=True, timeout=30,
            cwd=PROJECT_ROOT, creationflags=_NO_WINDOW,
        )
        return result.stdout if result.returncode == 0 else b""

    def _screenshot(self, dest="temp.png"):
        dest = resolve(dest)
        # exec-out streams the PNG straight back, so one adb call replaces the
        # screencap + pull + rm round-trip through /sdcard.
        data = self._exec_out(["screencap", "-p"])
        if data.startswith(b"\x89PNG"):
            with open(dest, "wb") as f:
                f.write(data)
            return dest
        return self._screenshot_via_pull(dest)

    def _screenshot_via_pull(self, dest):
        """Capture via /sdcard, for adb daemons whose exec-out returns nothing.

        Every step is checked: an unchecked failure here used to surface far
        away as a confusing "file not found" from the image layer, instead of
        naming the real cause (the device went away mid-run).
        """
        if not (
            self._run(["shell", "screencap", "-p", "/sdcard/tmp.png"])
            and self._run(["pull", "/sdcard/tmp.png", dest])
        ):
            self.stop(
                "Lost contact with the ADB device while capturing the screen. "
                "Check that your emulator is still running, then try again."
            )
        self._run(["shell", "rm", "/sdcard/tmp.png"])
        return dest

    def tap(self, x, y):
        self._run(["shell", "input", "tap", str(x), str(y)])

    def hold(self, x, y, ms=500):
        self._run(["shell", "input", "swipe", str(x), str(y), str(x), str(y), str(ms)])

    def swipe(self, x1, y1, x2, y2, ms=300):
        self._run(
            ["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(ms)]
        )

    def drag_hold(self, x1, y1, x2, y2, move_ms=300, hold_ms=500):
        def motion(action, x, y):
            self._run(["shell", "input", "motionevent", action, str(x), str(y)])

        steps = 8
        motion("DOWN", x1, y1)
        for i in range(1, steps + 1):
            mx = int(x1 + (x2 - x1) * i / steps)
            my = int(y1 + (y2 - y1) * i / steps)
            motion("MOVE", mx, my)
            time.sleep(move_ms / 1000 / steps)
        # Hold at the destination so the release velocity is zero (no fling).
        time.sleep(hold_ms / 1000)
        motion("MOVE", x2, y2)
        motion("UP", x2, y2)

    def write(self, text):
        escaped = text.replace(" ", "\\ ").replace("&", "\\&")
        self._run(["shell", "input", "text", escaped])

    def enter(self):
        self._run(["shell", "input", "keyevent", "66"])

    def delete(self):
        self._run(["shell", "input", "keyevent", "67"])

    def focus(self):
        pass  # ADB sends commands directly; no focus needed.
