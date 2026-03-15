import tools.adb as adb
import time

def run_trial():
    print("Running trial")
    while not adb.compare_image("img/quick_tt.png", (338, 962, 453, 1033), 0.9):
        if adb.compare_image("img/no_quick_tt.png", (249, 962, 356, 1030), 0.9):
            print("Quick mode activated")
            time.sleep(0.5)
            adb.tap(400, 896)

    time.sleep(0.5)
    adb.tap(407, 995)

    while not adb.compare_image("img/race_finished.png", (359, 915, 441, 955), 0.9):
        time.sleep(0.5)
        adb.tap(747, 979)

    print("Race finished")
    time.sleep(0.5)
    adb.tap(359, 915)