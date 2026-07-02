"""Run Champions Meeting races until the reward screen appears."""

import time

from ... import screen


def run_cm():
    race = 1
    while True:
        print(f"Races number: {race}")

        reward_found = False
        while True:
            if screen.see("race_begin", 0.90):
                break
            if screen.see("claim_reward", 0.95):
                reward_found = True
                break
            time.sleep(0.5)

        if reward_found:
            break

        screen.tap("race_begin")
        screen.wait("next_in_game")
        print("Race found")
        screen.tap("next_in_game")
        time.sleep(2)
        screen.tap("next_in_game")
        screen.wait("race")
        print("Starting race")
        screen.tap("race")
        time.sleep(2)

        print("Skipping race")
        screen.tap("skip_race")
        time.sleep(1.5)
        screen.tap("skip_race")
        time.sleep(3.7)
        screen.tap("skip_race")
        time.sleep(1.5)
        screen.tap("skip_race")

        while not screen.see("cm_race_finished"):
            screen.tap("rank_up_cm")
            time.sleep(0.5)

        print("Race finished")
        time.sleep(0.5)
        screen.tap("cm_race_finished")
        race += 1
