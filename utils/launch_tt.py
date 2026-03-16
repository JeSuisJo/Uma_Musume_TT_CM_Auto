import os
import time
import tools.adb as adb

def launch_tt():
    print("Team Trials")
    while not adb.compare_image("img/in_trial.png", (557, 893, 677, 931), 0.9):
        time.sleep(0.5)
        if adb.compare_image("img/next_mondays.png", (476, 680, 585, 724), 0.9):
            adb.tap(476, 680)
            time.sleep(1)
    time.sleep(0.5)
    adb.tap(407, 681)
    time.sleep(1.8)
    if adb.compare_image("img/no_rp.png", (476, 680, 585, 724), 0.9):
        return True