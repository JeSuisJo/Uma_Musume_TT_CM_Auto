import tools as action
from tools import coords
import time

def run_cm():
    r = 1
    while True:
        print(f"Races number: {r}")
        reward_found = False
        while not reward_found:
            if action.compare_image(coords("race_begin")["img"], coords("race_begin")["region"], 0.95):
                break
            if action.compare_image(coords("claim_reward")["img"], coords("claim_reward")["region"], 0.95):
                reward_found = True
                break
            time.sleep(0.5)

        if reward_found:
            break

        action.tap(*coords("race_begin")["tap"])
        action.wait_for_image(coords("next_in_game")["img"], coords("next_in_game")["region"], 0.9, 0.5)
        print("Race found")
        action.tap(*coords("next_in_game")["tap"])
        time.sleep(2)
        action.tap(*coords("next_in_game")["tap"])
        action.wait_for_image(coords("race")["img"], coords("race")["region"], 0.9, 0.5)
        print("Starting race")
        action.tap(*coords("race")["tap"])
        time.sleep(2)
        print("Skipping race")
        action.tap(*coords("skip_race")["tap"])
        time.sleep(1.5)
        action.tap(*coords("skip_race")["tap"])
        time.sleep(3.7)
        action.tap(*coords("skip_race")["tap"])
        time.sleep(1.5)
        action.tap(*coords("skip_race")["tap"])
        while not action.compare_image(coords("cm_race_finished")["img"], coords("cm_race_finished")["region"], 0.9):
            action.tap(*coords("rank_up_cm")["tap"])
            time.sleep(0.5)
        print("Race finished")
        time.sleep(0.5)
        action.tap(*coords("cm_race_finished")["tap"])
        r += 1
