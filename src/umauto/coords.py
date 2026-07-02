"""Named screen coordinates and reference images (coords.json).

Each entry holds a ``tap`` point, a ``region`` and an ``img`` reference for the
active platform ("adb" or "steam").
"""

import json

from .config import config
from .paths import resolve

_MODE = "steam" if config.get("steam", False) else "adb"


def _load():
    with open(resolve("coords.json"), encoding="utf-8") as f:
        return json.load(f)


_COORDS = _load()


def coords(name):
    """Return the coordinate block for ``name`` on the active platform."""
    return _COORDS[name][_MODE]
