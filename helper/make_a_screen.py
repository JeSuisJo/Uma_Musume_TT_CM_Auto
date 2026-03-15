import os
import sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.adb import _screenshot, path

# ---------------- Zone à capturer ----------------
x1, y1, x2, y2 = 476, 680, 585, 724
OUTPUT = "helper/capture.png"
# -------------------------------------------------

print("Capture in progress...")
temp = _screenshot()

img = Image.open(temp)
region = img.crop((x1, y1, x2, y2))
print(f"Screen size: {img.size}")
print(f"Region: ({x1}, {y1}) → ({x2}, {y2})  |  size: {region.size}")

out = path(OUTPUT)
region.save(out)
print(f"Saved: {out}")

img.close()
os.remove(temp)

input("\nPress Enter to close...")
