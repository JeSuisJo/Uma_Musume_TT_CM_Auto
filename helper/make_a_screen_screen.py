import os
import sys
import json
import time
from PIL import ImageGrab
import pygetwindow as gw

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "config.json"), encoding="utf-8") as f:
    WINDOW_TITLE = json.load(f).get("steam_window_title", "umamusume")

def path(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)

windows = gw.getWindowsWithTitle(WINDOW_TITLE)
if windows:
    win = windows[0]
    win.activate()
    time.sleep(0.5)
else:
    print(f"Fenêtre '{WINDOW_TITLE}' introuvable !")
    input("Press Enter to close...")
    exit()

# ---------------- Zone à capturer ----------------
x1, y1, x2, y2 = 634, 685, 740, 721
OUTPUT = "helper/capture_screen.png"
# -------------------------------------------------

print("Capture in progress...")
bbox = (win.left, win.top, win.right, win.bottom)
img = ImageGrab.grab(bbox=bbox)

region = img.crop((x1, y1, x2, y2))
print(f"Window size: {img.size}")
print(f"Region: ({x1}, {y1}) → ({x2}, {y2})  |  size: {region.size}")

out = path(OUTPUT)
region.save(out)
print(f"Saved: {out}")

img.close()

input("\nPress Enter to close...")
