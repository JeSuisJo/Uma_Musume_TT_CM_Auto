import tools.adb as adb
import json

def dif():
    skip_setup = False
    while not adb.compare_image("img/in_selection.png", (631, 890, 663, 928), 0.9):
        if adb.compare_image("img/next_tt.png", (364, 892, 430, 926), 0.9):
            print("Run already scheduled")
            break
        if adb.compare_image("img/no_quick_tt.png", (249, 962, 356, 1030), 0.9):
            print("Run already scheduled")
            skip_setup = True
            break
        if adb.compare_image("img/quick_tt.png", (338, 962, 453, 1033), 0.9):
            print("Run already scheduled")
            skip_setup = True
            break

    if skip_setup:
        return True

    if adb.compare_image("img/in_selection.png", (631, 890, 663, 928), 0.9):
        print("Difficulty selected")
        if json.load(open("config.json")).get("difficulty_tm") == "easy":
            adb.tap(424, 697)
        elif json.load(open("config.json")).get("difficulty_tm") == "medium":
            adb.tap(424, 502)
        elif json.load(open("config.json")).get("difficulty_tm") == "hard":
            adb.tap(424, 306)