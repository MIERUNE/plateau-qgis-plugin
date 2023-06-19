import json
from pathlib import Path

_codelists = None


def get_codelist(name: str) -> dict[str, str]:
    global _codelists
    if _codelists is None:
        with open((Path(__file__).parent / "codelists.json").resolve()) as f:
            _codelists = json.load(f)

    return _codelists[name]
