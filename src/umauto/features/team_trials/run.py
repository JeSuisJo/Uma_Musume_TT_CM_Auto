"""Run a trial race and skip to the result."""

import time

from ... import screen


def run_trial():
    print("Running trial")
    while not screen.see("quick_tt"):
        if screen.see("no_quick_tt"):
            print("Quick mode activated")
            time.sleep(0.5)
            screen.tap("quick_mode_tap")

    time.sleep(0.5)
    screen.tap("run_start")

    while not screen.see("race_finished"):
        time.sleep(0.5)
        screen.tap("skip_tap")

    print("Race finished")
    time.sleep(0.5)
    screen.tap("race_finished")
