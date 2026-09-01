import time

from .coords import coords
from .driver import driver


def tap(name):
    driver.tap(*coords(name)["tap"])


def swipe_to(name):
    driver.swipe(*coords(name)["swipe"])


def drag_hold_to(name, move_ms=300, hold_ms=500):
    x1, y1, x2, y2 = coords(name)["swipe"][:4]
    driver.drag_hold(x1, y1, x2, y2, move_ms=move_ms, hold_ms=hold_ms)


def see(name, threshold=0.9):
    block = coords(name)
    return driver.compare_image(block["img"], block["region"], threshold)


def is_color(name, tolerance=10):
    block = coords(name)
    x, y = block["tap"]
    return driver.is_color(x, y, block["rgb"], tolerance)


def wait(name, threshold=0.9, poll=0.5):
    block = coords(name)
    driver.wait_for_image(block["img"], block["region"], threshold, poll)


def see_template(name, threshold=0.9, scales=None):
    block = coords(name)
    _, loc = driver.find_template(block["img"], block["region"], threshold, scales)
    return loc is not None


def find(name, threshold=0.9, scales=None):
    block = coords(name)
    _, loc = driver.find_template(block["img"], block["region"], threshold, scales)
    return loc


def find_all(name, threshold=0.9, scales=None, color_threshold=None):
    block = coords(name)
    return driver.find_templates(
        block["img"],
        block["region"],
        threshold,
        scales,
        color_threshold=color_threshold,
    )


def wait_template(name, threshold=0.9, poll=0.5, scales=None):
    block = coords(name)
    driver.wait_for_template(block["img"], block["region"], threshold, poll, scales)


def tap_template(name, threshold=0.9, scales=None):
    block = coords(name)
    _, loc = driver.find_template(block["img"], block["region"], threshold, scales)
    if loc is not None:
        driver.tap(*loc)
    return loc


def see_any(*names, threshold=0.9):
    with driver.frozen():
        return any(see(name, threshold) for name in names)


def wait_any(*names, threshold=0.9, poll=0.5):
    while not see_any(*names, threshold=threshold):
        time.sleep(poll)


def wait_from_home(name, threshold=0.9, poll=0.5):
    while not see(name, threshold):
        if see("home"):
            tap("home")
        time.sleep(poll)
