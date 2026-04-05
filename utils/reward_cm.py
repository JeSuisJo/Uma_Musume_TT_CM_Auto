import tools as action
from tools import coords
import time

def reward_cm():
    action.tap(*coords("claim_reward")["tap"])
    time.sleep(3)
    action.tap(*coords("reward_next")["tap"])
