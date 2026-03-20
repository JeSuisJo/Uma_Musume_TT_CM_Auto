import os
import sys
import json
import time
from PIL import ImageGrab
import matplotlib.pyplot as plt
import pygetwindow as gw

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(ROOT, "config.json"), encoding="utf-8") as f:
    WINDOW_TITLE = json.load(f).get("steam_window_title", "umamusume")

windows = gw.getWindowsWithTitle(WINDOW_TITLE)
if windows:
    win = windows[0]
    win.activate()
    time.sleep(0.5)
else:
    print(f"Fenêtre '{WINDOW_TITLE}' introuvable !")
    input("Press Enter to close...")
    exit()

print("Capture in progress...")
bbox = (win.left, win.top, win.right, win.bottom)
img = ImageGrab.grab(bbox=bbox)

print(f"Window size: {img.size}")
print("Click on the image to get the coordinates and the color.\n")

def on_click(event):
    if event.inaxes is None:
        return
    x, y = int(event.xdata), int(event.ydata)
    if 0 <= x < img.width and 0 <= y < img.height:
        r, g, b = img.getpixel((x, y))
        print(f"Coordinates: ({x}, {y})")
        print(f"RGB color: ({r}, {g}, {b})")

fig, ax = plt.subplots(figsize=(14, 8))
ax.imshow(img)
ax.set_title("Click to get coordinates + RGB color")
ax.axis("off")
fig.canvas.mpl_connect("button_press_event", on_click)
plt.tight_layout()
plt.show()

input("\nPress Enter to close...")
