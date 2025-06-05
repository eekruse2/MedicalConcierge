import json
from pathlib import Path
from typing import Any, Dict, List

# Directory for storing JSON resource files
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def _resource_path(name: str) -> Path:
    """Return the Path object for data/<name>.json."""
    return DATA_DIR / f"{name}.json"


def list_resources(name: str) -> List[Dict[str, Any]]:
    """
    Load and return all resources of a given type from disk.
    If the file does not exist or is empty/invalid JSON, return an empty list.
    """
    path = _resource_path(name)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def create_resource(name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Append a new resource payload to the on-disk JSON file (and return it).
    If the file doesn’t exist yet, it will be created.
    """
    resources = list_resources(name)
    resources.append(payload)

    try:
        with open(_resource_path(name), "w", encoding="utf-8") as f:
            json.dump(resources, f, indent=2)
    except OSError:
        # If writing fails (permissions, etc.), we still return payload
        pass

    return payload
