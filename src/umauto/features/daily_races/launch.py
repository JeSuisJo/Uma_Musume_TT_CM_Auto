"""Open the daily program and enter the Daily Races screen."""

import time

from ... import screen


def open_daily_races():
    """Navigate from home to the Daily Races reward selection."""
    print("Opening the daily program")
    screen.wait_from_home("daily_program_enter")
    screen.tap("daily_program_enter")
    time.sleep(1.5)
    screen.wait("daily_race_enter")
    screen.tap("daily_race_enter")
    time.sleep(1.5)
