"""Semantic screen interactions: map named coordinates to driver actions.

Features work in terms of screen names ("in_trial", "cm_button", ...) instead of
raw pixels. This module is the single bridge between those names and the driver.
"""

import time

from .coords import coords
from .driver import driver


def tap(name):
    """Tap the ``tap`` point of a named coordinate."""
    driver.tap(*coords(name)["tap"])


def swipe_to(name):
    """Swipe using the ``swipe`` coordinates of a named entry."""
    driver.swipe(*coords(name)["swipe"])


def drag_hold_to(name, move_ms=300, hold_ms=500):
    """Drag along a named entry's ``swipe`` coords, holding at the end.

    Like :func:`swipe_to`, but keeps the touch pressed at the destination so
    the game's scroll inertia does not overshoot.
    """
    x1, y1, x2, y2 = coords(name)["swipe"][:4]
    driver.drag_hold(x1, y1, x2, y2, move_ms=move_ms, hold_ms=hold_ms)


def see(name, threshold=0.9):
    """Return True if the named element is currently on screen."""
    block = coords(name)
    return driver.compare_image(block["img"], block["region"], threshold)


def is_color(name, tolerance=10):
    """Return True if the pixel at the named ``tap`` point matches its ``rgb``."""
    block = coords(name)
    x, y = block["tap"]
    return driver.is_color(x, y, block["rgb"], tolerance)


def wait(name, threshold=0.9, poll=0.5):
    """Block until the named element appears on screen."""
    block = coords(name)
    driver.wait_for_image(block["img"], block["region"], threshold, poll)


def see_template(name, threshold=0.9, scales=None):
    """Like :func:`see`, but for a small image inside a larger region.

    Uses template matching (with multi-scale search), so the reference image
    can be smaller than its ``region`` and appear anywhere within it.
    """
    block = coords(name)
    _, loc = driver.find_template(block["img"], block["region"], threshold, scales)
    return loc is not None


def find(name, threshold=0.9, scales=None):
    """Return the centre ``(x, y)`` of a template match, or ``None``.

    Like :func:`see_template`, but gives back the match location so callers can
    tap somewhere relative to it (nothing is tapped here).
    """
    block = coords(name)
    _, loc = driver.find_template(block["img"], block["region"], threshold, scales)
    return loc


def find_all(name, threshold=0.9, scales=None, color_threshold=None):
    """Return the centres of ALL template matches of ``name`` in its region.

    Like :func:`find`, but reports every distinct on-screen copy (de-duplicated)
    so callers can act on each one -- e.g. buy a shop item that is listed twice.
    ``color_threshold`` adds a colour-sensitive check that rejects greyed-out
    (already-selected / disabled) copies which raw correlation still matches.
    """
    block = coords(name)
    return driver.find_templates(
        block["img"],
        block["region"],
        threshold,
        scales,
        color_threshold=color_threshold,
    )


def wait_template(name, threshold=0.9, poll=0.5, scales=None):
    """Block until a small/scaled ``name`` template appears inside its region."""
    block = coords(name)
    driver.wait_for_template(block["img"], block["region"], threshold, poll, scales)


def tap_template(name, threshold=0.9, scales=None):
    """Tap the centre of a template found inside its region.

    Returns the tapped ``(x, y)`` on success, or ``None`` when the template is
    not found (nothing is tapped in that case).
    """
    block = coords(name)
    _, loc = driver.find_template(block["img"], block["region"], threshold, scales)
    if loc is not None:
        driver.tap(*loc)
    return loc


def see_any(*names, threshold=0.9):
    """Return True if any of the named elements is currently on screen."""
    return any(see(name, threshold) for name in names)


def wait_any(*names, threshold=0.9, poll=0.5):
    """Block until any one of the named elements appears on screen."""
    while not see_any(*names, threshold=threshold):
        time.sleep(poll)


def wait_from_home(name, threshold=0.9, poll=0.5):
    """Block until ``name`` appears, tapping "home" to get back there.

    Like :func:`wait`, but while the target is not on screen it taps the
    "home" element whenever it is visible. This recovers when the game is
    sitting on the home screen instead of the menu that shows ``name``.
    """
    while not see(name, threshold):
        if see("home"):
            tap("home")
        time.sleep(poll)
