from PIL import ImageGrab
import matplotlib.pyplot as plt

print("Capture in progress...")
img = ImageGrab.grab()

print(f"Screen size: {img.size}")
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
