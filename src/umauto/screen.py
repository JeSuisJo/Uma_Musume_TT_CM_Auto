"""Semantic screen interactions: map named coordinates to driver actions.

Features work in terms of screen names ("in_trial", "cm_button", ...) instead of
raw pixels. This module is the single bridge between those names and the driver.
"""

from .coords import coords
from .driver import driver


def tap(name):
    """Tap the ``tap`` point of a named coordinate."""
    driver.tap(*coords(name)["tap"])


def see(name, threshold=0.9):
    """Return True if the named element is currently on screen."""
    block = coords(name)
    return driver.compare_image(block["img"], block["region"], threshold)


def wait(name, threshold=0.9, poll=0.5):
    """Block until the named element appears on screen."""
    block = coords(name)
    driver.wait_for_image(block["img"], block["region"], threshold, poll)
