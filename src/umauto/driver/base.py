"""Driver abstraction: shared image/colour logic over platform primitives.

Subclasses implement the platform-specific primitives (``_screenshot``,
``tap``, ``swipe``, ...). Everything image- or colour-related is shared here and
relies only on ``_screenshot``, so it never gets duplicated across backends.
"""

import contextlib
import math
import os
import time

from PIL import Image, ImageChops

from ..paths import resolve


class StopScript(Exception):
    """Raised to abort the current run cleanly."""

    def __init__(self, message="Script stopped"):
        super().__init__(message)


def _silent_remove(path):
    with contextlib.suppress(OSError):
        os.remove(path)


class Driver:
    """Base driver with shared image and colour helpers."""

    # --- primitives (implemented by subclasses) ---
    def _screenshot(self, dest="temp.png"):
        raise NotImplementedError

    def tap(self, x, y):
        raise NotImplementedError

    def hold(self, x, y, ms=500):
        raise NotImplementedError

    def swipe(self, x1, y1, x2, y2, ms=300):
        raise NotImplementedError

    def write(self, text):
        raise NotImplementedError

    def enter(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def focus(self):
        """Bring the game to the foreground (no-op when not needed)."""

    def stop(self, message="Script stopped"):
        raise StopScript(message)

    def screenshot(self, dest="temp.png"):
        """Capture the current screen to ``dest`` and return its path."""
        return self._screenshot(dest)

    # --- image helpers (shared) ---
    @staticmethod
    def _similarity(img1, img2):
        if img1.size != img2.size:
            img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
        hist = ImageChops.difference(img1, img2).histogram()
        total = img1.size[0] * img1.size[1] * 3
        if not total:
            return 0.0
        rms = math.sqrt(sum((i % 256) ** 2 * hist[i] for i in range(768)) / total)
        return max(0.0, min(1.0, 1.0 - rms / 255.0))

    def compare_image(self, reference_path, region, threshold=0.95):
        temp = self._screenshot()
        shot = Image.open(temp).crop(region).convert("RGB")
        reference = Image.open(resolve(reference_path)).convert("RGB")
        matched = self._similarity(shot, reference) >= threshold
        _silent_remove(temp)
        return matched

    def wait_for_image(self, reference_path, region, threshold=0.9, poll=0.5):
        while not self.compare_image(reference_path, region, threshold):
            time.sleep(poll)

    # --- colour helpers (shared) ---
    def get_color(self, x, y):
        temp = self._screenshot()
        color = Image.open(temp).convert("RGB").getpixel((x, y))
        _silent_remove(temp)
        return color

    def is_color(self, x, y, target, tolerance=10):
        return all(
            abs(a - b) <= tolerance
            for a, b in zip(self.get_color(x, y), target, strict=False)
        )

    def wait_for_color(self, x, y, target, tolerance=10, poll=0.5):
        while not self.is_color(x, y, target, tolerance):
            time.sleep(poll)
