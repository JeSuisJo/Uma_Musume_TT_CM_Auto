"""Steam driver: controls the Windows game window via pyautogui/win32."""

import time

import pyautogui
import pygetwindow as gw
import pywintypes
import win32con
import win32gui
from PIL import ImageGrab

from ..config import config
from ..paths import resolve
from .base import Driver


class SteamDriver(Driver):
    def __init__(self):
        self.window_title = config.get("steam_window_title", "Umamusume")

    # --- window ---
    def _window(self):
        windows = gw.getWindowsWithTitle(self.window_title)
        if not windows:
            raise RuntimeError(f"Window '{self.window_title}' not found")
        return windows[0]

    def _offset(self):
        win = self._window()
        return win.left, win.top

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
        """Bring ``hwnd`` to the foreground.

        ``SetForegroundWindow`` fails (error 6, invalid handle) when the calling
        process does not own the foreground, so we retry with the well-known
        workarounds and never let a focus failure crash the run.
        """
        try:
            win32gui.SetForegroundWindow(hwnd)
            return
        except pywintypes.error:
            pass

        # A synthetic ALT press unlocks Windows' foreground-lock restriction.
        try:
            pyautogui.press("alt")
            win32gui.SetForegroundWindow(hwnd)
            return
        except pywintypes.error:
            pass

        # Last resort: minimizing then restoring usually forces the focus.
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
        except pywintypes.error as exc:
            print(f"Warning: could not focus the game window ({exc}).")

    def _screenshot(self, dest="temp.png"):
        dest = resolve(dest)
        win = self._window()
        image = ImageGrab.grab(bbox=(win.left, win.top, win.right, win.bottom))
        image.save(dest)
        return dest

    # --- primitives ---
    def tap(self, x, y):
        ox, oy = self._offset()
        pyautogui.click(ox + x, oy + y)

    def hold(self, x, y, ms=500):
        ox, oy = self._offset()
        pyautogui.mouseDown(ox + x, oy + y)
        time.sleep(ms / 1000)
        pyautogui.mouseUp()

    def swipe(self, x1, y1, x2, y2, ms=300):
        ox, oy = self._offset()
        pyautogui.moveTo(ox + x1, oy + y1)
        pyautogui.drag(x2 - x1, y2 - y1, duration=ms / 1000)

    def write(self, text):
        pyautogui.typewrite(text, interval=0.02)

    def enter(self):
        pyautogui.press("enter")

    def delete(self):
        pyautogui.press("backspace")
