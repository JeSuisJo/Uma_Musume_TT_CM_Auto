import tools as action
from tools import coords
import time
import json
import utils.daily_shop as daily_shop

def finish_run():
    shopped = False

    while not action.compare_image(coords("finish_run")["img"], coords("finish_run")["region"], 0.9):
        if action.compare_image(coords("highscore")["img"], coords("highscore")["region"], 0.9):
            time.sleep(0.5)
            action.tap(*coords("highscore")["tap"])
            shopped = False

        if action.compare_image(coords("story_unlocked")["img"], coords("story_unlocked")["region"], 0.9):
            time.sleep(0.5)
            action.tap(*coords("story_unlocked")["tap"])
            shopped = False

        if action.compare_image(coords("next_go_to_reward")["img"], coords("next_go_to_reward")["region"], 0.9):
            time.sleep(0.5)
            action.tap(*coords("next_go_to_reward")["tap"])
            shopped = False

        if action.compare_image(coords("next_reward")["img"], coords("next_reward")["region"], 0.9):
            time.sleep(0.5)
            action.tap(*coords("next_reward")["tap"])
            shopped = False

        if action.compare_image(coords("shop")["img"], coords("shop")["region"], 0.9):
            time.sleep(0.5)
            if json.load(open("config.json"))["daily_sales_buy"] == True:
                daily_shop.shop()
                shopped = True
                break
            else:
                action.tap(*coords("shop")["tap"])
                time.sleep(1)
                shopped = False

        if action.compare_image(coords("finish_run")["img"], coords("finish_run")["region"], 0.9):
            shopped = False
            break

    if shopped == True:
        return
    else:
        print("Go back to the trial menu")
        time.sleep(0.8)
        action.tap(*coords("finish_run")["tap"])
