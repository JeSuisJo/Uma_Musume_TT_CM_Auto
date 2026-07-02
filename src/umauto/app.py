"""Application entry point.

``ensure_config`` runs before anything that reads config.json, so the very
first thing on a fresh install is the configuration wizard.
"""

from .setup_config import ensure_config


def run():
    ensure_config()
    # Imported lazily: these modules read config.json at import time.
    from .cli import main

    main()
