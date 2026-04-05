import tools as action
from tools import coords
import os
import time

def menu():
    os.system("cls")
    print("="*50)
    print("Uma Musume Champions Meeting Auto")
    print("="*50)


menu()
print("Do you want to do a extra run?")
print("[1] Yes")
print("[0] No")
choice = input("Enter your choice: ")
choice = int(choice)

menu()
print("Do you want to make your own team?")
print("[1] Yes")
print("[0] No")
team = input("Enter your choice: ")
menu()

print("Going to the Champions Meeting")
action.wait_for_image(coords("go_to_cm")["img"], coords("go_to_cm")["region"], 0.9, 0.5)
action.tap(*coords("go_to_cm")["tap"])
time.sleep(0.5)
while not action.compare_image(coords("in_cm")["img"], coords("in_cm")["region"], 0.9):
    time.sleep(0.5)
    action.tap(*coords("cm_popup_close")["tap"])
print("In the Champions Meeting")

print("Checking if you have free runs")
time.sleep(1)
how_many = 0
if action.compare_image(coords("free_cm")["img"], coords("free_cm")["region"], 0.9):
    runs = 3+choice
else:
    menu()
    how_many = input("How many runs have you already done?: ")
    runs = (3-int(how_many))+choice

for i in range(runs):
    menu()
    print(f"Running {i+1} of {runs}")
    action.wait_for_image(coords("in_cm")["img"], coords("in_cm")["region"], 0.9, 0.5)
    time.sleep(0.5)
    if i >= 1 or int(how_many) >= 1:
        action.tap(*coords("ticket")["tap"])
        time.sleep(2)
        action.tap(*coords("ticket_collect")["tap"])
        time.sleep(1)
        action.tap(*coords("ticket_close")["tap"])
        time.sleep(1)
        action.tap(*coords("back_to_cm")["tap"])
        time.sleep(1.5)

    action.tap(*coords("cm_launch")["tap"])
    time.sleep(1)

    if action.compare_image(coords("cm_ok_freerun")["img"], coords("cm_ok_freerun")["region"], 0.9):
        action.tap(*coords("cm_ok_freerun")["tap"])

    time.sleep(1.5)
    if action.compare_image(coords("cm_auto_team")["img"], coords("cm_auto_team")["region"], 0.9):
        if team == "1":
            input("Click enter when you have made your team")
        else:
            time.sleep(1)
            action.wait_for_image(coords("cm_auto_team")["img"], coords("cm_auto_team")["region"], 0.9, 0.5)
            action.tap(*coords("cm_auto_team")["tap"])
            time.sleep(1)
            action.wait_for_image(coords("cm_auto_team_ok")["img"], coords("cm_auto_team_ok")["region"], 0.9, 0.5)
            action.tap(*coords("cm_auto_team_ok")["tap"])
            time.sleep(1)

        action.tap(*coords("cm_team_selected")["tap"])
        time.sleep(1)
        action.tap(*coords("cm_confirm_registration")["tap"])

    print("Run")
    r = 1
    while True:
        menu()
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

    action.tap(*coords("claim_reward")["tap"])
    time.sleep(3)
    action.tap(*coords("reward_next")["tap"])
   

print("CM finished")
action.wait_for_image(coords("in_cm")["img"], coords("in_cm")["region"], 0.9, 0.5)
action.tap(*coords("cm_finish")["tap"])