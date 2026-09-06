import json
import os

_STI = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "takster.json")
_cache = None


def hent_takster(sti: str = None) -> dict:
    """Laeser data/takster.json. Cacher resultatet, medmindre en anden sti gives."""
    global _cache
    if sti is not None:
        with open(sti, encoding="utf-8") as f:
            return json.load(f)
    if _cache is None:
        with open(_STI, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache
