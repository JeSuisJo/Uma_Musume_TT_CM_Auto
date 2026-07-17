"""Claim the Champions Meeting run reward."""

import time

from ... import screen


def claim_reward():
    screen.tap("claim_reward")
    time.sleep(1)
    screen.wait("reward_next")
    time.sleep(1)
    screen.tap("reward_next")
