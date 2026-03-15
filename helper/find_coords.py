import os
import sys
from PIL import Image
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.adb import _screenshot, path

print("Capture in progress...")
temp = _screenshot()
img  = Image.open(temp)
print(f"Screen size: {img.size}")
print("Click on the image to get the coordinates and the color.\n")

def on_click(event):
    if event.inaxes is None:
        return
    x, y = int(event.xdata), int(event.ydata)
    if 0 <= x < img.width and 0 <= y < img.height:
        r, g, b = img.convert("RGB").getpixel((x, y))
        print(f"Coordinates: ({x}, {y})")
        print(f"RGB color: ({r}, {g}, {b})")

fig, ax = plt.subplots(figsize=(8, 14))
ax.imshow(img)
ax.set_title("Click to get coordinates + RGB color")
ax.axis("off")
fig.canvas.mpl_connect("button_press_event", on_click)
plt.tight_layout()
plt.show()

os.remove(temp)
input("\nPress Enter to close...")
