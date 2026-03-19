import os
import sys
from PIL import ImageGrab
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.adb import path

# ---------------- Zone à capturer ----------------
x1, y1, x2, y2 = 631, 890, 663, 928
OUTPUT = "helper/capture_screen.png"
# -------------------------------------------------

print("Capture in progress...")
img = ImageGrab.grab()

region = img.crop((x1, y1, x2, y2))
print(f"Screen size: {img.size}")
print(f"Region: ({x1}, {y1}) → ({x2}, {y2})  |  size: {region.size}")

out = path(OUTPUT)
region.save(out)
print(f"Saved: {out}")

img.close()

input("\nPress Enter to close...")
