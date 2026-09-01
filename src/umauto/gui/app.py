import os

_PLACEMENT_PIXELS = {"x": 967, "y": 7, "width": 947, "height": 1026}


def _placement():
    return dict(_PLACEMENT_PIXELS)


def run():
    import webview

    from .api import Api

    os.environ.setdefault(
        "WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS",
        "--disable-gpu --disable-gpu-compositing",
    )

    api = Api()
    html_path = os.path.join(os.path.dirname(__file__), "web", "index.html")

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

    webview.start(http_server=True)
