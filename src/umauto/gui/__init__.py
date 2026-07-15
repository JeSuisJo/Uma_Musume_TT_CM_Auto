"""Graphical front-end (pywebview) over the same features as the CLI.

The GUI never rewrites automation logic: it drives the existing ``FEATURES``
registry in a worker thread while redirecting stdout to an on-screen log and
turning ``input()`` prompts into modal dialogs (see :mod:`.runtime`).
"""
