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
