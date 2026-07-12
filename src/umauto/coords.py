"""Named screen coordinates and reference images (the ``coords/`` folder).

Coordinates are split one JSON file per feature (``coords/shop.json``,
``coords/team_trials.json``, ...) plus ``coords/common.json`` for entries shared
by several modes -- mirroring the ``features/`` packages. They are merged into a
single flat namespace at import time, so callers still look names up globally
(``coords("shop_star_piece")``); the split is storage-only.

Each entry holds a ``tap`` point, a ``region`` and an ``img`` reference for the
active platform ("adb" or "steam").
"""

import glob
import json
import os

from .config import config
from .paths import resolve

_MODE = "steam" if config.get("steam", False) else "adb"

_COORDS_DIR = resolve("coords")


def _load():
    """Merge every ``coords/*.json`` file, rejecting duplicate names.

    A flat global namespace means the same name defined in two files would
    silently shadow one another; instead we fail loudly with both filenames so
    the collision is fixed at its source rather than debugged on screen.
    """
    merged = {}
    origin = {}  # name -> file it came from, for collision messages
    for path in sorted(glob.glob(os.path.join(_COORDS_DIR, "*.json"))):
        name_of_file = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            entries = json.load(f)
        for name, block in entries.items():
            if name in merged:
                raise ValueError(
                    f"Duplicate coord '{name}' defined in both "
                    f"'{origin[name]}' and '{name_of_file}'"
                )
            merged[name] = block
            origin[name] = name_of_file
    return merged


_COORDS = _load()


def coords(name):
    """Return the coordinate block for ``name`` on the active platform."""
    return _COORDS[name][_MODE]
