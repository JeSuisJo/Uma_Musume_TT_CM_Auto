"""Select the trial difficulty configured in config.json."""

import time

from ... import screen
from ...config import config

_DIFFICULTIES = ("easy", "medium", "hard")


def select_difficulty():
    """Pick the configured difficulty.

    Return True when a run is already scheduled and the setup step can be
    skipped, False otherwise.
    """
    while not screen.see("in_selection"):
        if screen.see("in_selection_refresh"):
            break
        if screen.see("next_tt"):
            print("Run already scheduled")
            return False
        if screen.see("no_quick_tt") or screen.see("quick_tt"):
            print("Run already scheduled")
            return True

    difficulty = config.get("difficulty_tm")
    if screen.see("in_selection") or screen.see("in_selection_refresh"):
        print("Difficulty selected")
        time.sleep(0.5)
        if difficulty in _DIFFICULTIES:
            screen.tap(f"dif_{difficulty}")
    return False
