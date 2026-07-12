"""Daily Races mode: run a single daily race for the configured reward."""

import os

from ...config import config
from .launch import open_daily_races
from .race import collect_rewards
from .select import select_race
from .start import start_race


def run():
    os.system("cls")
    print("=" * 50)
    print("Uma Musume Daily Races Auto")
    print("=" * 50)

    difficulty = config.get("daily_race_difficulty", "very_hard")
    reward = config.get("daily_race_reward", "money")
    print(f"Difficulty: {difficulty} | Reward: {reward}")

    open_daily_races()
    select_race(reward, difficulty)
    start_race()

    print("Collecting the rewards")
    collect_rewards()
    print("Daily race finished")
