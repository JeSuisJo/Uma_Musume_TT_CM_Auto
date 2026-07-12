"""Confirm the trial line-up before the race."""

import time

from ... import screen
from ...config import config


def setup_trial():
    print("Starting trial")
    screen.wait("next_tt")
    screen.tap("next_tt")
    if config.get("use_parfait_TT"):
        time.sleep(1)
        print("Using parfait")
        screen.tap("use_parfait")
    time.sleep(1)
    screen.tap("setup_confirm")
