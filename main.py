import os
import tools as action
from tools import coords

valid_choices = ["1", "2", "0"]

while True:
    choice = ""
    while choice not in valid_choices:
        os.system("cls")
        print("="*50)
        print("Uma Musume TT CM Auto")
        print("="*50)

        print("[1] Team Trials")
        print("[2] Champions Meeting")
        print("[0] Exit")

        choice = input("Enter your choice: ")

    if choice == "1":
        c = coords("tt_button")
        action.wait_for_image(c["img"], c["region"], 0.9, 0.5)
        action.tap(*c["tap"])
        exec(open("modes/tt.py").read())
    elif choice == "2":
        c = coords("cm_button")
        action.wait_for_image(c["img"], c["region"], 0.9, 0.5)
        action.tap(*c["tap"])
    elif choice == "0":
        exit()
