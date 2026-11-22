"""Coordinate picker for the carrot-jelly refill flow.

Run from the project root:  python tools/pick_coords.py
Works with whichever mode config.json selects (steam / adb); coordinates are
printed in the same 1920x1080-style space the bot uses.

Navigate the game to the screen named at the top, press R to re-capture,
then click the target. Backspace = undo, Esc = quit. Results go to
picked_coords.json and the console.
"""
import json
import os
import sys
import tkinter as tk

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from PIL import Image, ImageTk  # noqa: E402

from umauto.driver import driver  # noqa: E402
from umauto.paths import resolve  # noqa: E402

STEPS = [
    ("menu_button", "HOME screen: click the Menu button"),
    ("inventory_button", "MENU open: click Inventory"),
    ("carrot_use", "INVENTORY: click Use of Carrot Jelly Mini"),
    ("carrot_max", "Recover RP dialog: click Max"),
    ("carrot_ok", "Recover RP dialog: click OK"),
]


def grab():
    if hasattr(driver, "capture"):
        return driver.capture()
    return Image.open(driver._screenshot("pick.png")).convert("RGB")


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.results = {}
        self.i = 0
        self.img = grab()
        self.scale = min(1.0, 1500 / self.img.width, 900 / self.img.height)
        self.label = tk.Label(self.root, font=("Segoe UI", 14), fg="blue")
        self.label.pack()
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)
        self.root.bind("r", lambda e: self.recapture())
        self.root.bind("<BackSpace>", lambda e: self.undo())
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.draw()

    def draw(self):
        w, h = int(self.img.width * self.scale), int(self.img.height * self.scale)
        self.tk_img = ImageTk.PhotoImage(self.img.resize((w, h)))
        self.canvas.config(width=w, height=h)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        for name, (x, y) in self.results.items():
            sx, sy = x * self.scale, y * self.scale
            self.canvas.create_oval(sx - 6, sy - 6, sx + 6, sy + 6, outline="red", width=2)
            self.canvas.create_text(sx + 10, sy, text=name, fill="red", anchor="w")
        if self.i < len(STEPS):
            self.label.config(text=f"[{self.i + 1}/{len(STEPS)}] {STEPS[self.i][1]}   (R = recapture)")
        else:
            self.label.config(text="Done! See console / picked_coords.json. Esc to close.")

    def recapture(self):
        self.img = grab()
        self.draw()

    def undo(self):
        if self.i:
            self.i -= 1
            self.results.pop(STEPS[self.i][0], None)
            self.draw()

    def click(self, e):
        if self.i >= len(STEPS):
            return
        x, y = round(e.x / self.scale), round(e.y / self.scale)
        name = STEPS[self.i][0]
        self.results[name] = (x, y)
        print(f"{name}: [{x}, {y}]")
        self.i += 1
        if self.i >= len(STEPS):
            out = {k: list(v) for k, v in self.results.items()}
            with open(resolve("picked_coords.json"), "w", encoding="utf-8") as f:
                json.dump(out, f, indent=2)
            print(json.dumps(out, indent=2))
        self.draw()


if __name__ == "__main__":
    App().root.mainloop()
