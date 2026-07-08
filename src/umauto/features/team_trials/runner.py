"""Team Trials mode: loop runs until race points are exhausted."""

import os
import time

from ... import screen
from .difficulty import select_difficulty
from .finish import finish_run
from .launch import launch_trial
from .run import run_trial
from .setup import setup_trial


def run():
    screen.wait_from_home("tt_button")
    screen.tap("tt_button")

    run_number = 1
    while True:
        os.system("cls")
        print("=" * 50)
        print("Uma Musume Team Trials Auto")
        print(f"Run: {run_number}")
        print("=" * 50)

        if launch_trial():
            break
        if not select_difficulty():
            setup_trial()
        run_trial()
        finish_run()
        run_number += 1

    print("No more RP")
    screen.tap("no_rp_close")
    time.sleep(1)
    screen.tap("no_rp_confirm")
