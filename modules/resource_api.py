import json
from pathlib import Path
from typing import Any, Dict, List

# In‐memory cache for resources loaded from disk (or newly created)
_resources: Dict[str, List[Dict[str, Any]]] = {}

# Base directory where JSON “stub” files live (e.g. data/stubs/<resource_type>.json)
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "stubs"


def _load_resource_file(resource_type: str) -> List[Dict[str, Any]]:
    """
    Attempt to read data/stubs/<resource_type>.json from disk.
    If it exists and is valid JSON, return the parsed list.
    Otherwise, return an empty list.
    """
    path = DATA_DIR / f"{resource_type}.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            # If JSON is malformed, just return an empty list
            return []
    return []


def list_resources(resource_type: str) -> List[Dict[str, Any]]:
    """
    Return all resources of a given type. On first access, tries to load from
    data/stubs/<resource_type>.json into the in‐memory store.
    """
    if resource_type not in _resources:
        _resources[resource_type] = _load_resource_file(resource_type)
    return _resources[resource_type]


def create_resource(resource_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Append a new resource payload to the in‐memory store (and write it back to disk).
    Returns the newly created payload.
    """
    # Ensure the in‐memory list is initialized (and, if needed, loaded from disk)
    if resource_type not in _resources:
        _resources[resource_type] = _load_resource_file(resource_type)

    _resources[resource_type].append(payload)

    # Try writing the updated list back to DATA_DIR/<resource_type>.json
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path = DATA_DIR / f"{resource_type}.json"
        path.write_text(json.dumps(_resources[resource_type], indent=2))
    except Exception:
        # If writing fails (permissions, etc.), we silently ignore so that
        # the in‐memory store still works. In a real app, you might log this.
        pass

    return payload
