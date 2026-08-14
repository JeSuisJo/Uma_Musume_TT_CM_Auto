"""Application entry point.

``ensure_config`` runs before anything else touches config.json: on a fresh
install, the wizard is the very first thing that happens.
"""

from .setup import ensure_config


def run():
    ensure_config()
    # Imported lazily: these modules read config.json at import time.
    from .cli import main

    main()
