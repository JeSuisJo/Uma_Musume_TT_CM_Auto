import time

import pyautogui
import pygetwindow as gw
import pywintypes
import win32con
import win32gui
from PIL import Image, ImageGrab

from ..config import config
from ..paths import resolve
from .base import Driver

REFERENCE_WIDTH = 1920
REFERENCE_HEIGHT = 1080


class SteamDriver(Driver):
    def __init__(self):
        self.window_title = config.get("steam_window_title", "Umamusume")

    def _window(self):
        windows = gw.getWindowsWithTitle(self.window_title)
        if not windows:
            self.stop(
                f"Game window '{self.window_title}' not found. "
                "Start Umamusume on Steam and wait for its window to appear, "
                "then try again."
            )
        return windows[0]

    def ensure_ready(self):
        self.client_rect()

    def client_rect(self):
        hwnd = self._window()._hWnd
        _, _, width, height = win32gui.GetClientRect(hwnd)
        if width <= 0 or height <= 0:
            self.stop(
                f"Game window '{self.window_title}' has no visible client area. "
                "Restore it (it must not be minimized), then try again."
            )
        left, top = win32gui.ClientToScreen(hwnd, (0, 0))
        return left, top, width, height

    def _to_screen(self, x, y):
        left, top, width, height = self.client_rect()
        return (
            left + round(x * width / REFERENCE_WIDTH),
            top + round(y * height / REFERENCE_HEIGHT),
        )

    def focus(self):
        win = self._window()
        hwnd = win._hWnd
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOP,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW,
        )
        self._set_foreground(hwnd)
        time.sleep(0.5)

    @staticmethod
    def _set_foreground(hwnd):
        try:
            win32gui.SetForegroundWindow(hwnd)
            return
        except pywintypes.error:
            pass

        try:
            pyautogui.press("alt")
            win32gui.SetForegroundWindow(hwnd)
            return
        except pywintypes.error:
            pass

        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
        except pywintypes.error as exc:
            print(f"Warning: could not focus the game window ({exc}).")

    def capture(self):
        left, top, width, height = self.client_rect()
        image = ImageGrab.grab(
            bbox=(left, top, left + width, top + height), all_screens=True
        )
        if image.size != (REFERENCE_WIDTH, REFERENCE_HEIGHT):
            image = image.resize(
                (REFERENCE_WIDTH, REFERENCE_HEIGHT), Image.Resampling.LANCZOS
            )
        return image

    def _screenshot(self, dest="temp.png"):
        dest = resolve(dest)
        self.capture().save(dest)
        return dest

    def tap(self, x, y):
        pyautogui.click(*self._to_screen(x, y))

    def hold(self, x, y, ms=500):
        pyautogui.mouseDown(*self._to_screen(x, y))
        time.sleep(ms / 1000)
        pyautogui.mouseUp()

    def swipe(self, x1, y1, x2, y2, ms=300):
        sx1, sy1 = self._to_screen(x1, y1)
        sx2, sy2 = self._to_screen(x2, y2)
        pyautogui.moveTo(sx1, sy1)
        pyautogui.drag(sx2 - sx1, sy2 - sy1, duration=ms / 1000)

    def drag_hold(self, x1, y1, x2, y2, move_ms=300, hold_ms=800):
        sx1, sy1 = self._to_screen(x1, y1)
        sx2, sy2 = self._to_screen(x2, y2)
        pyautogui.moveTo(sx1, sy1)
        pyautogui.mouseDown()
        pyautogui.moveTo(sx2, sy2, duration=move_ms / 1000)
        time.sleep(hold_ms / 1000)
        pyautogui.mouseUp()

    def write(self, text):
        pyautogui.typewrite(text, interval=0.02)

    def enter(self):
        pyautogui.press("enter")

    def delete(self):
        pyautogui.press("backspace")
