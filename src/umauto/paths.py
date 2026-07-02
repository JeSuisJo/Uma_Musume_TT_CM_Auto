"""Filesystem paths anchored at the project root.

Data files (config.json, coords.json, img/, platform-tools/) live at the repo
root, next to the ``src`` folder, so everything is resolved from there.
"""

import os

# src/umauto/paths.py -> umauto -> src -> project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


def resolve(relative_path):
    """Return an absolute path, resolving relative paths from the project root."""
    if os.path.isabs(relative_path):
        return relative_path
    return os.path.join(PROJECT_ROOT, relative_path)
