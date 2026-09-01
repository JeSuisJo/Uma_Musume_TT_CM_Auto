import time

from ... import screen
from ...driver import driver
from .champions import COORD_BY_NAME, DEFAULT

_MAX_SCROLLS = 10


def select_champion(champion):
    champion_coord = COORD_BY_NAME.get(champion, COORD_BY_NAME[DEFAULT])

    print(f"Selecting {champion}")
    time.sleep(1)
    if not screen.see_template(champion_coord, threshold=0.8):
        screen.tap("dr_scroll_up")
        time.sleep(0.5)
        screen.tap("dr_scroll_up")
        time.sleep(0.5)
        screen.tap("dr_scroll_up")
        for _ in range(_MAX_SCROLLS):
            if screen.see_template(champion_coord, threshold=0.8):
                break
            screen.drag_hold_to("dr_scroll")
            time.sleep(0.6)
    if not screen.see_template(champion_coord, threshold=0.8):
        time.sleep(0.5)
        screen.tap("home")
        driver.stop(f"{champion} not found on screen, stopping the run")
    screen.tap_template(champion_coord, threshold=0.8)
    time.sleep(2)
