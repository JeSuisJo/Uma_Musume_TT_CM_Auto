from .setup import ensure_config


def run():
    ensure_config()
    from .cli import main

    main()
