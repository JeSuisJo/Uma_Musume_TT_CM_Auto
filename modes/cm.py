import tools as action
from tools import coords
import os
import time

from utils.launch_cm import launch_cm
from utils.collect_ticket_cm import collect_ticket
from utils.setup_team_cm import setup_team
from utils.run_cm import run_cm
from utils.reward_cm import reward_cm

def menu():
    os.system("cls")
    print("="*50)
    print("Uma Musume Champions Meeting Auto")
    print("="*50)

menu()
print("Do you want to do a extra run?")
print("[1] Yes")
print("[0] No")
choice = int(input("Enter your choice: "))

menu()
print("Do you want to make your own team?")
print("[1] Yes")
print("[0] No")
team = input("Enter your choice: ")
menu()

launch_cm()

print("Checking if you have free runs")
time.sleep(1)
how_many = 0
if action.compare_image(coords("free_cm")["img"], coords("free_cm")["region"], 0.9):
    runs = 3 + choice
else:
    menu()
    how_many = int(input("How many runs have you already done?: "))
    runs = (3 - how_many) + choice

for i in range(runs):
    menu()
    print(f"Running {i+1} of {runs}")
    action.wait_for_image(coords("in_cm")["img"], coords("in_cm")["region"], 0.9, 0.5)
    time.sleep(0.5)
    if i >= 1 or how_many >= 1:
        collect_ticket()

    action.tap(*coords("cm_launch")["tap"])
    time.sleep(1)

    if action.compare_image(coords("cm_ok_freerun")["img"], coords("cm_ok_freerun")["region"], 0.9):
        action.tap(*coords("cm_ok_freerun")["tap"])

    setup_team(team)
    print("Run")
    run_cm()
    reward_cm()

print("CM finished")
action.wait_for_image(coords("in_cm")["img"], coords("in_cm")["region"], 0.9, 0.5)
action.tap(*coords("cm_finish")["tap"])
