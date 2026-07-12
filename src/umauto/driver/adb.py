"""ADB driver: controls an Android emulator/device via platform-tools/adb."""

import subprocess
import time

from ..config import config
from ..paths import PROJECT_ROOT, resolve
from .base import Driver

_ADB = resolve("platform-tools/adb.exe")


class AdbDriver(Driver):
    def __init__(self):
        self.device = self._detect_device()

    @staticmethod
    def _list_devices():
        result = subprocess.run(
            [_ADB, "devices"], capture_output=True, text=True, timeout=10
        )
        lines = [
            line for line in result.stdout.strip().split("\n")[1:] if "\tdevice" in line
        ]
        return [line.split("\t")[0] for line in lines]

    def _detect_device(self):
        configured = config.get("device_id")

        devices = self._list_devices()
        if configured and configured in devices:
            return configured
        if devices:
            return devices[0]

        # ADB lost the connection: restart the server and retry once.
        subprocess.run([_ADB, "kill-server"], capture_output=True, timeout=10)
        time.sleep(1)
        subprocess.run([_ADB, "start-server"], capture_output=True, timeout=15)
        time.sleep(2)

        devices = self._list_devices()
        if configured and configured in devices:
            return configured
        if devices:
            return devices[0]

        # Fall back to the configured value even if it is not visible yet.
        return configured

    def _run(self, args):
        base = [_ADB, "-s", self.device] if self.device else [_ADB]
        result = subprocess.run(
            base + args, capture_output=True, text=True, timeout=30, cwd=PROJECT_ROOT
        )
        return result.returncode == 0

    def _screenshot(self, dest="temp.png"):
        dest = resolve(dest)
        self._run(["shell", "screencap", "-p", "/sdcard/tmp.png"])
        self._run(["pull", "/sdcard/tmp.png", dest])
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
