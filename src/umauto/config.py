import json

from .paths import resolve


class Config:
    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def get(self, key, default=None):
        return self._data.get(key, default)


def _load():
    with open(resolve("config.json"), encoding="utf-8") as f:
        return Config(json.load(f))


config = _load()
