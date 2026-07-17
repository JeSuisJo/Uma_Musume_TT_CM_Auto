"""Open the native GUI window (pywebview) over the local HTML page.

While a mode runs, the window snaps to a fixed overlay placement so it floats on
a corner the bot never reads or clicks. Steam mode requires a 1920x1080 screen,
so the geometry is a hardcoded pixel rect (measured with helper/place_window.py).
"""

import os

# Overlay geometry while a mode runs. Fixed because Steam mode is always played
# at 1920x1080 -- measured with helper/place_window.py; paste its four numbers.
_PLACEMENT_PIXELS = {"x": 967, "y": 7, "width": 947, "height": 1026}


def _placement():
    """Overlay geometry (as create_window kwargs) for the running window."""
    return dict(_PLACEMENT_PIXELS)


def run():
    import webview

    from .api import Api

    # Force software rendering: avoids the WebView2 GPU-compositor hang that can
    # leave the window shown but the page never finishing navigation.
    os.environ.setdefault(
        "WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS",
        "--disable-gpu --disable-gpu-compositing",
    )

    api = Api()
    html_path = os.path.join(os.path.dirname(__file__), "web", "index.html")

    # Open at a comfortable default size/centre. The window only snaps to the
    # game-overlay placement (``_placement()``) once a mode is launched, and
    # restores afterwards -- handled in the API layer.
    window = webview.create_window(
        "Uma Auto",
        url=html_path,
        js_api=api,
        width=1000,
        height=760,
        min_size=(380, 520),
        background_color="#fdf2f8",
    )
    api._window = window

    # http_server serves the page over 127.0.0.1 instead of file://, which
    # WebView2 loads more reliably. Blocks until the window is closed.
    webview.start(http_server=True)
