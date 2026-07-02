"""Navigate into the Champions Meeting screen."""

import time

from ... import screen


def launch_cm():
    print("Going to the Champions Meeting")
    screen.wait("go_to_cm")
    screen.tap("go_to_cm")
    time.sleep(0.5)
    while not screen.see("in_cm"):
        time.sleep(0.5)
        screen.tap("cm_popup_close")
    print("In the Champions Meeting")
