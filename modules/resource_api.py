import json
from pathlib import Path
from typing import List, Dict

# In-memory store for resources
_resources: Dict[str, List[dict]] = {}

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "stubs"

def _load_resource_file(resource_type: str) -> List[dict]:
    path = DATA_DIR / f"{resource_type}.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return []
    return []

def list_resources(resource_type: str) -> List[dict]:
    if resource_type not in _resources:
        _resources[resource_type] = _load_resource_file(resource_type)
    return _resources[resource_type]

def create_resource(resource_type: str, payload: dict) -> None:
    if resource_type not in _resources:
        _resources[resource_type] = _load_resource_file(resource_type)
    _resources[resource_type].append(payload)
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path = DATA_DIR / f"{resource_type}.json"
        path.write_text(json.dumps(_resources[resource_type], indent=2))
    except Exception:
        pass
