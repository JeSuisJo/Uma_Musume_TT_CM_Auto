import tools as action
from tools import coords
import time

def collect_ticket():
    action.tap(*coords("ticket")["tap"])
    time.sleep(2)
    action.tap(*coords("ticket_collect")["tap"])
    time.sleep(1)
    action.tap(*coords("ticket_close")["tap"])
    time.sleep(1)
    action.tap(*coords("back_to_cm")["tap"])
    time.sleep(1.5)
