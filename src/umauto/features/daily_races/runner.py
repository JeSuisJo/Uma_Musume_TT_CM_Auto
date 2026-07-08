"""Daily Races mode: run a single daily race for the configured reward."""

import os
import time

from ... import screen
from ...config import config
from .race import race

# config value -> coordinate name of the reward to farm.
_REWARDS = {
    "money": "dr_money",
    "support": "dr_support",
}

# config value -> coordinate name of the difficulty to pick.
_DIFFICULTIES = {
    "easy": "dr_dif_easy",
    "normal": "dr_dif_normal",
    "hard": "dr_dif_hard",
    "very_hard": "dr_dif_very_hard",
}


def run():
    os.system("cls")
    print("=" * 50)
    print("Uma Musume Daily Races Auto")
    print("=" * 50)

    difficulty = config.get("daily_race_difficulty", "very_hard")
    difficulty_coord = _DIFFICULTIES.get(difficulty, "dr_dif_very_hard")
    reward = config.get("daily_race_reward", "money")
    print(f"Difficulty: {difficulty} | Reward: {reward}")

    print("Opening the daily program")
    screen.wait_from_home("daily_program_enter")
    screen.tap("daily_program_enter")
    time.sleep(1.5)
    screen.tap("daily_race_enter")
    time.sleep(1.5)

    print(f"Selecting the {reward} race")
    if reward == "money":
        screen.wait("dr_money")
        screen.tap("dr_money")
    else:
        screen.wait("dr_support")
        screen.tap("dr_support")
    time.sleep(1.5)

    print("Selecting the difficulty")
    if difficulty == "easy":
        screen.swipe_to("dr_scroll")
        time.sleep(1.5)
        screen.tap(difficulty_coord)
    else:
        screen.tap(difficulty_coord)
    time.sleep(1.5)

    screen.wait("daily_race_start")
    time.sleep(0.5)
    if not screen.is_color("dr_multi_race"):
        print("Enabling multi-race")
        screen.tap("dr_multi_race")
        time.sleep(0.5)

    print("Starting the race")
    screen.tap("daily_race_start")
    time.sleep(1.5)
    screen.wait("daily_race_confirm_runner")
    screen.tap("daily_race_confirm_runner")
    time.sleep(1.5)
    screen.tap("dr_race_start")

    print("Collecting the rewards")
    race()
    print("Daily race finished")
