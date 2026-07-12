"""Enable multi-race, then start and confirm the daily race."""

import time

from ... import screen


def start_race():
    """Toggle multi-race if needed, then launch the race."""
    screen.wait("daily_race_start")
    time.sleep(0.5)
    if not screen.is_color("dr_multi_race"):
        print("Enabling multi-race")
        screen.tap("dr_multi_race")
        time.sleep(0.5)

    print("Starting the race")
    screen.tap("daily_race_start")
    time.sleep(1.5)
    screen.wait("daily_race_confirm_runner")
    screen.tap("daily_race_confirm_runner")
    time.sleep(1.5)
    screen.tap("dr_race_start")
