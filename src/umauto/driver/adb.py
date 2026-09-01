import contextlib
import json
import re
import subprocess
import sys
import time

from ..config import config
from ..paths import PROJECT_ROOT, resolve
from ..setup.prompts import ask_from_list
from .base import Driver

_ADB = resolve("platform-tools/adb.exe")

_NO_WINDOW = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

_COMPONENT = re.compile(r"([A-Za-z0-9_.]+/[A-Za-z0-9_.$]+)")
_RESUMED_MARKERS = ("topResumedActivity=", "ResumedActivity:")


def _save_device_id(device_id):
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
        self.device = config.get("device_id")

    @staticmethod
    def _adb(args, timeout=10):
        try:
            result = subprocess.run(
                [_ADB] + args, capture_output=True, text=True, timeout=timeout,
                creationflags=_NO_WINDOW,
            )
        except (OSError, subprocess.SubprocessError):
            return ""
        return result.stdout if result.returncode == 0 else ""

    @classmethod
    def _list_devices(cls):
        lines = [
            line
            for line in cls._adb(["devices"]).strip().split("\n")[1:]
            if "\tdevice" in line
        ]
        return [line.split("\t")[0] for line in lines]

    @classmethod
    def _restart_server(cls):
        cls._adb(["kill-server"])
        time.sleep(1)
        cls._adb(["start-server"], timeout=15)
        time.sleep(2)

    @classmethod
    def _foreground_app(cls, device_id):
        dump = cls._adb(
            ["-s", device_id, "shell", "dumpsys", "activity", "activities"], timeout=15
        )
        for line in dump.split("\n"):
            marker = next((m for m in _RESUMED_MARKERS if m in line), None)
            if not marker:
                continue
            match = _COMPONENT.search(line.split(marker, 1)[1])
            if match and "launcher" not in match.group(1).lower():
                return match.group(1).split("/")[0]
        return ""

    def _use_device(self, device_id, note):
        self.device = device_id
        _save_device_id(device_id)
        print(f"{note}: {device_id}")

    @classmethod
    def _ask_device(cls, devices):
        labels = []
        for device in devices:
            app = cls._foreground_app(device)
            labels.append(f"{device} - {app}" if app else device)
        chosen = ask_from_list("Multiple devices connected:", labels, labels[0])
        return devices[labels.index(chosen)]

    @classmethod
    def _is_online(cls, device_id):
        return cls._adb(["-s", device_id, "get-state"]).strip() == "device"

    def ensure_ready(self):
        configured = config.get("device_id")

        if configured and self._is_online(configured):
            self.device = configured
            return

        devices = self._list_devices()

        if len(devices) == 1:
            self._use_device(devices[0], "ADB device auto-selected")
            return

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

        if not devices:
            self.stop("No emulator detected. Start your emulator, then try again.")

        self._use_device(self._ask_device(devices), "ADB device selected")

    def _run(self, args):
        base = [_ADB, "-s", self.device] if self.device else [_ADB]
        result = subprocess.run(
            base + args, capture_output=True, text=True, timeout=30,
            cwd=PROJECT_ROOT, creationflags=_NO_WINDOW,
        )
        return result.returncode == 0

    def _exec_out(self, args):
        base = [_ADB, "-s", self.device] if self.device else [_ADB]
        result = subprocess.run(
            base + ["exec-out"] + args, capture_output=True, timeout=30,
            cwd=PROJECT_ROOT, creationflags=_NO_WINDOW,
        )
        return result.stdout if result.returncode == 0 else b""

    def _screenshot(self, dest="temp.png"):
        dest = resolve(dest)
        data = self._exec_out(["screencap", "-p"])
        if data.startswith(b"\x89PNG"):
            with open(dest, "wb") as f:
                f.write(data)
            return dest
        return self._screenshot_via_pull(dest)

    def _screenshot_via_pull(self, dest):
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
        pass
