import time

from ... import screen

_REWARDS = {
    "money": "dr_money",
    "support": "dr_support",
}

_DIFFICULTIES = {
    "easy": "dr_dif_easy",
    "normal": "dr_dif_normal",
    "hard": "dr_dif_hard",
    "very_hard": "dr_dif_very_hard",
}


def select_race(reward, difficulty):
    reward_coord = _REWARDS.get(reward, "dr_money")
    difficulty_coord = _DIFFICULTIES.get(difficulty, "dr_dif_very_hard")

    print(f"Selecting the {reward} race")
    screen.wait(reward_coord)
    screen.tap(reward_coord)
    time.sleep(1.5)

    print("Selecting the difficulty")
    if difficulty == "easy":
        screen.swipe_to("dr_scroll")
        time.sleep(1.5)
        screen.tap(difficulty_coord)
    else:
        screen.tap(difficulty_coord)
    time.sleep(1.5)
