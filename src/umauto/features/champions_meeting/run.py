"""Run Champions Meeting races until the reward screen appears."""

import time

from ... import screen


def run_cm():
    race = 1
    while True:
        print(f"Races number: {race}")

        reward_found = False
        while True:
            with screen.driver.frozen():
                matching = screen.see("matching", 0.90)
                begin = screen.see("race_begin", 0.90)
                reward = screen.see("claim_reward", 0.95)
            if matching:
                screen.tap("race_begin")
                continue
            if begin:
                break
            if reward:
                reward_found = True
                break
            time.sleep(0.5)

        if reward_found:
            break

        screen.tap("race_begin")
        screen.wait("next_in_game")
        print("Race found")
        screen.tap("next_in_game")
        screen.wait_template("view_result_cm")
        print("Skip Race")
        time.sleep(1)
        screen.tap_template("view_result_cm")

        while not screen.see("cm_race_finished"):
            screen.tap("rank_up_cm")
            time.sleep(0.5)

        print("Race finished")
        time.sleep(0.5)
        screen.tap("cm_race_finished")
        race += 1
