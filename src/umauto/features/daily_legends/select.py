"""Select the configured champion in the Daily Legends list.

Scrolls the champion list looking for the champion's icon template and taps it.
Stops the run (via :meth:`driver.stop`) when the champion cannot be found.
"""

import time

from ... import screen
from ...driver import driver
from .champions import COORD_BY_NAME, DEFAULT

# How many times to scroll the list while hunting for the champion.
_MAX_SCROLLS = 4


def select_champion(champion):
    """Find and tap ``champion`` (a display name) in the Daily Legends list."""
    champion_coord = COORD_BY_NAME.get(champion, COORD_BY_NAME[DEFAULT])

    print(f"Selecting {champion}")
    if not screen.see_template(champion_coord, threshold=0.8):
        screen.swipe_to("dr_scroll_up")
        time.sleep(0.5)
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
