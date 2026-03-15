import os
import tools.adb as adb
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
        adb.wait_for_image("img/tt.png", (204, 759, 341, 792), 0.9, 0.5)
        adb.tap(204, 759)
        exec(open("modes/tt.py").read())
    elif choice == "2":
        adb.wait_for_image("img/cm.png", (452, 764, 586, 792), 0.9, 0.5)
        adb.tap(452, 764)
    elif choice == "0":
        exit()