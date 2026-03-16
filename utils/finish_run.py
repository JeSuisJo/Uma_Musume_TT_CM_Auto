import tools.adb as adb
import time
import json
import utils.daily_shop as shop

def finish_run():
    while not adb.compare_image("img/finish_run.png", (459, 956, 595, 1033), 0.9):
        if adb.compare_image("img/highscore.png", (309, 339, 435, 391), 0.9):
            time.sleep(0.5)
            adb.tap(309, 339)
            shopped = False

        if adb.compare_image("img/next_go_to_reward.png", (354, 992, 439, 1033), 0.9):
            time.sleep(0.5)
            adb.tap(354, 992)
            shopped = False

        if adb.compare_image("img/next_reward.png", (353, 972, 453, 1016), 0.9):
            time.sleep(0.5)
            adb.tap(353, 972)
            shopped = False

        if adb.compare_image("img/shop.png", (489, 679, 573, 728), 0.9):
            time.sleep(0.5)
            if json.load(open("config.json"))["daily_sales_buy"] == True:
                shop()
                shopped = True
                break

            else:
                adb.tap(489, 679)
                time.sleep(1)
                shopped = False

        if adb.compare_image("img/finish_run.png", (459, 956, 595, 1033), 0.9):
            shopped = False
            break
        
    if shopped == True:
        return
    else:
        print("Go back to the trial menu")
        time.sleep(0.8)
        adb.tap(459, 956)