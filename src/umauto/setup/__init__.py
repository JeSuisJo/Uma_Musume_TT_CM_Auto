"""Configuration wizard: create config.json, or backfill new keys on upgrade."""

from .wizard import ensure_config

__all__ = ["ensure_config"]
