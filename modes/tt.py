import tools as action
from tools import coords
import os
import time

from utils.launch_tt import launch_tt
from utils.difficulty import dif
from utils.setup import setup_trial
from utils.run import run_trial
from utils.finish_run import finish_run

run = 1

while True:
    os.system("cls")
    print("="*50)
    print("Uma Musume Team Trials Auto")
    print(f"Run: {run}")
    print("="*50)
    no_rp = launch_tt()
    if no_rp:
        break
    skip = dif()
    if not skip:
        setup_trial()
    run_trial()
    finish_run()
    run += 1

print("No more RP")
action.tap(*coords("no_rp_close")["tap"])
time.sleep(1)
action.tap(*coords("no_rp_confirm")["tap"])
