import tools as action
from tools import coords
import time
import json
import utils.daily_shop as daily_shop

def finish_run():
    shopped = False
    c_fr = coords("finish_run")
    c_hs = coords("highscore")
    c_gtr = coords("next_go_to_reward")
    c_nr = coords("next_reward")
    c_sh = coords("shop")
    c_str = coords("story_unlocked")

    while not action.compare_image(c_fr["img"], c_fr["region"], 0.9):
        if action.compare_image(c_hs["img"], c_hs["region"], 0.9):
            time.sleep(0.5)
            action.tap(*c_hs["tap"])
            shopped = False

        if action.compare_image(c_str["img"], c_str["region"], 0.9):
            time.sleep(0.5)
            action.tap(*c_str["tap"])
            shopped = False

        if action.compare_image(c_gtr["img"], c_gtr["region"], 0.9):
            time.sleep(0.5)
            action.tap(*c_gtr["tap"])
            shopped = False

        if action.compare_image(c_nr["img"], c_nr["region"], 0.9):
            time.sleep(0.5)
            action.tap(*c_nr["tap"])
            shopped = False

        if action.compare_image(c_sh["img"], c_sh["region"], 0.9):
            time.sleep(0.5)
            if json.load(open("config.json"))["daily_sales_buy"] == True:
                daily_shop.shop()
                shopped = True
                break
            else:
                action.tap(*c_sh["tap"])
                time.sleep(1)
                shopped = False

        if action.compare_image(c_fr["img"], c_fr["region"], 0.9):
            shopped = False
            break

    if shopped == True:
        return
    else:
        print("Go back to the trial menu")
        time.sleep(0.8)
        action.tap(*c_fr["tap"])
