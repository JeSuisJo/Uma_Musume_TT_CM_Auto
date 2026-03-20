import tools as action
from tools import coords
import json
import time

def dif():
    skip_setup = False
    c_sel = coords("in_selection")
    c_selr = coords("in_selection_refresh")
    c_ntt = coords("next_tt")
    c_noq = coords("no_quick_tt")
    c_q = coords("quick_tt")

    while not action.compare_image(c_sel["img"], c_sel["region"], 0.9):
        if action.compare_image(c_selr["img"], c_selr["region"], 0.9):
            break
        if action.compare_image(c_ntt["img"], c_ntt["region"], 0.9):
            print("Run already scheduled")
            break
        if action.compare_image(c_noq["img"], c_noq["region"], 0.9):
            print("Run already scheduled")
            skip_setup = True
            break
        if action.compare_image(c_q["img"], c_q["region"], 0.9):
            print("Run already scheduled")
            skip_setup = True
            break

    if skip_setup:
        return True

    cfg = json.load(open("config.json"))
    difficulty = cfg.get("difficulty_tm")

    if action.compare_image(c_sel["img"], c_sel["region"], 0.9):
        print("Difficulty selected")
        time.sleep(0.5)
        if difficulty == "easy":
            action.tap(*coords("dif_easy")["tap"])
        elif difficulty == "medium":
            action.tap(*coords("dif_medium")["tap"])
        elif difficulty == "hard":
            action.tap(*coords("dif_hard")["tap"])

    if action.compare_image(c_selr["img"], c_selr["region"], 0.9):
        print("Difficulty selected")
        time.sleep(0.5)
        if difficulty == "easy":
            action.tap(*coords("dif_easy")["tap"])
        elif difficulty == "medium":
            action.tap(*coords("dif_medium")["tap"])
        elif difficulty == "hard":
            action.tap(*coords("dif_hard")["tap"])
