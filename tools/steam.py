import os
import json
import time
import math
import pyautogui
import pygetwindow as gw
from PIL import Image, ImageChops, ImageGrab

# ---------------- Config ----------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "config.json"), encoding="utf-8") as f:
    _cfg = json.load(f)

WINDOW_TITLE = _cfg.get("steam_window_title", "Umamusume")

def path(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)

class StopScriptException(Exception):
    def __init__(self, msg="Script stopped"):
        super().__init__(msg)

# ---------------- Fenêtre ----------------
def _get_window():
    wins = gw.getWindowsWithTitle(WINDOW_TITLE)
    if not wins:
        raise RuntimeError(f"Fenêtre '{WINDOW_TITLE}' introuvable")
    return wins[0]

def _focus_window():
    win = _get_window()
    if not win.isActive:
        win.activate()
        time.sleep(0.3)
    return win

def _window_offset():
    win = _get_window()
    return win.left, win.top

# ---------------- Interne ----------------
def _screenshot(dest="temp.png"):
    dest = path(dest)
    win = _get_window()
    bbox = (win.left, win.top, win.right, win.bottom)
    img = ImageGrab.grab(bbox=bbox)
    img.save(dest)
    return dest

def _similarity(img1, img2):
    if img1.size != img2.size:
        img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
    hist = ImageChops.difference(img1, img2).histogram()
    total = img1.size[0] * img1.size[1] * 3
    rms = math.sqrt(sum((i % 256) ** 2 * hist[i] for i in range(768)) / total) if total else 255
    return max(0.0, min(1.0, 1.0 - rms / 255.0))

# ---------------- Actions ----------------
def tap(x, y):
    _focus_window()
    ox, oy = _window_offset()
    pyautogui.click(ox + x, oy + y)

def hold(x, y, ms=500):
    _focus_window()
    ox, oy = _window_offset()
    pyautogui.mouseDown(ox + x, oy + y)
    time.sleep(ms / 1000)
    pyautogui.mouseUp()

def swipe(x1, y1, x2, y2, ms=300):
    _focus_window()
    ox, oy = _window_offset()
    pyautogui.moveTo(ox + x1, oy + y1)
    pyautogui.drag(x2 - x1, y2 - y1, duration=ms / 1000)

def write(text):
    _focus_window()
    pyautogui.typewrite(text, interval=0.02)

def enter():
    _focus_window()
    pyautogui.press("enter")

def delete():
    _focus_window()
    pyautogui.press("backspace")

def stop(msg="Script stopped"):
    raise StopScriptException(msg)

# ---------------- Image ----------------
def compare_image(reference_path, region, threshold=0.95):
    temp = _screenshot()
    shot = Image.open(temp).crop(region).convert("RGB")
    ref = Image.open(path(reference_path)).convert("RGB")
    result = _similarity(shot, ref) >= threshold
    try: os.remove(temp)
    except OSError: pass
    return result

def wait_for_image(reference_path, region, threshold=0.9, poll=0.5):
    while not compare_image(reference_path, region, threshold):
        time.sleep(poll)

# ---------------- Couleur ----------------
def get_color(x, y):
    temp = _screenshot()
    color = Image.open(temp).convert("RGB").getpixel((x, y))
    try: os.remove(temp)
    except OSError: pass
    return color

def is_color(x, y, target, tolerance=10):
    return all(abs(a - b) <= tolerance for a, b in zip(get_color(x, y), target))

def wait_for_color(x, y, target, tolerance=10, poll=0.5):
    while not is_color(x, y, target, tolerance):
        time.sleep(poll)
