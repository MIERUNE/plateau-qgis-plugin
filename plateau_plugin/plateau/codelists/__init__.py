import json
from pathlib import Path
from typing import Optional

_codelists: Optional[dict[str, dict[str, str]]] = None


def get_codelist(name: str) -> dict[str, str]:
    global _codelists
    if _codelists is None:
        with open((Path(__file__).parent / "codelists.json").resolve()) as f:
            _codelists = json.load(f)

    assert _codelists is not None
    return _codelists[name]
