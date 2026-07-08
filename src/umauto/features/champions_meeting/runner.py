"""Champions Meeting mode: run the remaining daily attempts."""

import os
import time

from ... import screen
from ...config import config
from .launch import launch_cm
from .reward import claim_reward
from .run import run_cm
from .team import setup_team
from .ticket import collect_ticket


def _header():
    os.system("cls")
    print("=" * 50)
    print("Uma Musume Champions Meeting Auto")
    print("=" * 50)


def run(already_done):
    extra_run = 1 if config.get("cm_extra_run", False) else 0
    make_own_team = config.get("make_your_own_team", False)

    screen.wait_from_home("cm_button")
    screen.tap("cm_button")

    launch_cm()

    print("Checking if you have free runs")
    time.sleep(1)
    # With free runs all 3 attempts are available; otherwise only what is left.
    done = 0 if screen.see("free_cm") else already_done
    runs = (3 - done) + extra_run

    for index in range(runs):
        _header()
        print(f"Running {index + 1} of {runs}")
        screen.wait("in_cm")
        time.sleep(0.5)
        if index >= 1 or already_done >= 1:
            collect_ticket()

        screen.tap("cm_launch")
        time.sleep(1)
        if screen.see("cm_ok_freerun"):
            screen.tap("cm_ok_freerun")

        setup_team(make_own_team)
        print("Run")
        run_cm()
        claim_reward()

    print("CM finished")
    screen.wait("in_cm")
    screen.tap("cm_finish")
