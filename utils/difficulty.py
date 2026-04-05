import tools as action
from tools import coords
import json
import time

def dif():
    skip_setup = False

    while not action.compare_image(coords("in_selection")["img"], coords("in_selection")["region"], 0.9):
        if action.compare_image(coords("in_selection_refresh")["img"], coords("in_selection_refresh")["region"], 0.9):
            break
        if action.compare_image(coords("next_tt")["img"], coords("next_tt")["region"], 0.9):
            print("Run already scheduled")
            break
        if action.compare_image(coords("no_quick_tt")["img"], coords("no_quick_tt")["region"], 0.9):
            print("Run already scheduled")
            skip_setup = True
            break
        if action.compare_image(coords("quick_tt")["img"], coords("quick_tt")["region"], 0.9):
            print("Run already scheduled")
            skip_setup = True
            break

    if skip_setup:
        return True

    difficulty = json.load(open("config.json")).get("difficulty_tm")

    if action.compare_image(coords("in_selection")["img"], coords("in_selection")["region"], 0.9):
        print("Difficulty selected")
        time.sleep(0.5)
        if difficulty == "easy":
            action.tap(*coords("dif_easy")["tap"])
        elif difficulty == "medium":
            action.tap(*coords("dif_medium")["tap"])
        elif difficulty == "hard":
            action.tap(*coords("dif_hard")["tap"])

    if action.compare_image(coords("in_selection_refresh")["img"], coords("in_selection_refresh")["region"], 0.9):
        print("Difficulty selected")
        time.sleep(0.5)
        if difficulty == "easy":
            action.tap(*coords("dif_easy")["tap"])
        elif difficulty == "medium":
            action.tap(*coords("dif_medium")["tap"])
        elif difficulty == "hard":
            action.tap(*coords("dif_hard")["tap"])
