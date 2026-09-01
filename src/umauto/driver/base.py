import contextlib
import math
import os
import time

from PIL import Image, ImageChops

from ..paths import resolve


class StopScript(Exception):
    def __init__(self, message="Script stopped"):
        super().__init__(message)


def _silent_remove(path):
    with contextlib.suppress(OSError):
        os.remove(path)


def _iou(a, b):
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    if inter == 0:
        return 0.0
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    return inter / (area_a + area_b - inter)


class Driver:
    _freeze_active = False
    _frozen_path = None

    def _screenshot(self, dest="temp.png"):
        raise NotImplementedError

    @contextlib.contextmanager
    def frozen(self):
        if self._freeze_active:
            yield
            return
        self._freeze_active = True
        self._frozen_path = None
        try:
            yield
        finally:
            if self._frozen_path:
                _silent_remove(self._frozen_path)
            self._frozen_path = None
            self._freeze_active = False

    def _capture(self):
        if not self._freeze_active:
            return self._screenshot()
        if self._frozen_path is None:
            self._frozen_path = self._screenshot()
        return self._frozen_path

    def _release(self, path):
        if not (self._freeze_active and path == self._frozen_path):
            _silent_remove(path)

    def tap(self, x, y):
        raise NotImplementedError

    def hold(self, x, y, ms=500):
        raise NotImplementedError

    def swipe(self, x1, y1, x2, y2, ms=300):
        raise NotImplementedError

    def drag_hold(self, x1, y1, x2, y2, move_ms=300, hold_ms=500):
        raise NotImplementedError

    def write(self, text):
        raise NotImplementedError

    def enter(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def focus(self):
        pass

    def ensure_ready(self):
        pass

    def stop(self, message="Script stopped"):
        raise StopScript(message)

    def screenshot(self, dest="temp.png"):
        return self._screenshot(dest)

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
        temp = self._capture()
        shot = Image.open(temp).crop(region).convert("RGB")
        reference = Image.open(resolve(reference_path)).convert("RGB")
        matched = self._similarity(shot, reference) >= threshold
        self._release(temp)
        return matched

    def wait_for_image(self, reference_path, region, threshold=0.9, poll=0.5):
        while not self.compare_image(reference_path, region, threshold):
            time.sleep(poll)

    def find_template(self, reference_path, region, threshold=0.9, scales=None):
        import cv2
        import numpy as np

        if scales is None:
            scales = (1.0, 0.9, 0.8, 0.7, 0.6, 0.5)

        temp = self._capture()
        shot = Image.open(temp).crop(region).convert("RGB")
        self._release(temp)
        haystack = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)
        ref = cv2.cvtColor(
            np.array(Image.open(resolve(reference_path)).convert("RGB")),
            cv2.COLOR_RGB2BGR,
        )

        h_h, h_w = haystack.shape[:2]
        best_score, best_loc = -1.0, None
        for scale in scales:
            tw, th = int(ref.shape[1] * scale), int(ref.shape[0] * scale)
            if tw < 1 or th < 1 or tw > h_w or th > h_h:
                continue
            template = cv2.resize(ref, (tw, th), interpolation=cv2.INTER_AREA)
            result = cv2.matchTemplate(haystack, template, cv2.TM_CCOEFF_NORMED)
            _, score, _, loc = cv2.minMaxLoc(result)
            if score > best_score:
                cx = region[0] + loc[0] + tw // 2
                cy = region[1] + loc[1] + th // 2
                best_score, best_loc = score, (cx, cy)

        return (best_score, best_loc if best_score >= threshold else None)

    def find_templates(
        self,
        reference_path,
        region,
        threshold=0.9,
        scales=None,
        max_results=30,
        color_threshold=None,
    ):
        import cv2
        import numpy as np

        if scales is None:
            scales = (1.0, 0.9, 0.8, 0.7, 0.6, 0.5)

        temp = self._capture()
        shot = Image.open(temp).crop(region).convert("RGB")
        self._release(temp)
        haystack = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)
        ref = cv2.cvtColor(
            np.array(Image.open(resolve(reference_path)).convert("RGB")),
            cv2.COLOR_RGB2BGR,
        )

        h_h, h_w = haystack.shape[:2]
        boxes = []
        for scale in scales:
            tw, th = int(ref.shape[1] * scale), int(ref.shape[0] * scale)
            if tw < 1 or th < 1 or tw > h_w or th > h_h:
                continue
            template = cv2.resize(ref, (tw, th), interpolation=cv2.INTER_AREA)
            result = cv2.matchTemplate(haystack, template, cv2.TM_CCOEFF_NORMED)
            ys, xs = np.where(result >= threshold)
            for x, y in zip(xs.tolist(), ys.tolist(), strict=False):
                boxes.append((float(result[y, x]), x, y, x + tw, y + th))

        boxes.sort(reverse=True)
        kept = []
        for _score, x1, y1, x2, y2 in boxes:
            if any(_iou((x1, y1, x2, y2), k) > 0.3 for k in kept):
                continue
            if color_threshold is not None:
                crop = haystack[y1:y2, x1:x2].astype(np.float32)
                tmpl = cv2.resize(ref, (x2 - x1, y2 - y1)).astype(np.float32)
                rms = np.sqrt(((crop - tmpl) ** 2).mean())
                if 1.0 - rms / 255.0 < color_threshold:
                    continue
            kept.append((x1, y1, x2, y2))
            if len(kept) >= max_results:
                break

        return [
            (region[0] + (x1 + x2) // 2, region[1] + (y1 + y2) // 2)
            for x1, y1, x2, y2 in kept
        ]

    def wait_for_template(
        self, reference_path, region, threshold=0.9, poll=0.5, scales=None
    ):
        while self.find_template(reference_path, region, threshold, scales)[1] is None:
            time.sleep(poll)

    def get_color(self, x, y):
        temp = self._capture()
        color = Image.open(temp).convert("RGB").getpixel((x, y))
        self._release(temp)
        return color

    def is_color(self, x, y, target, tolerance=10):
        return all(
            abs(a - b) <= tolerance
            for a, b in zip(self.get_color(x, y), target, strict=False)
        )

    def wait_for_color(self, x, y, target, tolerance=10, poll=0.5):
        while not self.is_color(x, y, target, tolerance):
            time.sleep(poll)
