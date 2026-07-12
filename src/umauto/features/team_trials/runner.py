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
    run_number = 1
    need_launch = True  # re-enter through the trial menu: first run, or after a shop
    while True:
        os.system("cls")
        print("=" * 50)
        print("Uma Musume Team Trials Auto")
        print(f"Run: {run_number}")
        print("=" * 50)

        # Enter Team Trials from the home screen. Needed on the first run and
        # again after the daily shop sends us home; between runs 'race again'
        # (in finish_run) drops us straight onto selection, so we skip this.
        if need_launch:
            screen.wait_from_home("tt_button")
            screen.tap("tt_button")
            if launch_trial():
                # Entered Team Trials with no race points left.
                print("No more RP")
                screen.tap("no_rp_close")
                time.sleep(1)
                screen.tap("no_rp_confirm")
                return
            need_launch = False

        if not select_difficulty():
            setup_trial()
        run_trial()

        status = finish_run()
        if status == "no_rp":
            # Race points ran out; finish_run already dismissed and went home.
            return
        if status == "home":
            # The daily shop sent us home: go back in through the trial menu.
            need_launch = True
        run_number += 1
