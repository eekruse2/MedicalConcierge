import json
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def _resource_path(name: str) -> Path:
    return DATA_DIR / f"{name}.json"


def list_resources(name: str) -> List[Dict[str, Any]]:
    path = _resource_path(name)
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def create_resource(name: str, payload: Dict[str, Any]) -> None:
    resources = list_resources(name)
    resources.append(payload)
    with open(_resource_path(name), "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=2)

