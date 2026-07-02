"""Enter Team Trials and detect when race points run out."""

import time

from ... import screen


def launch_trial():
    """Open the trial menu; return True if there are no race points left."""
    print("Team Trials")
    while not screen.see("in_trial"):
        time.sleep(0.5)
        if screen.see("next_mondays"):
            screen.tap("next_mondays")
            time.sleep(1)
    time.sleep(0.5)
    screen.tap("launch_tt_tap")
    time.sleep(1.8)
    return screen.see("no_rp")
