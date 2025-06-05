import json
from pathlib import Path

# Base directory is two levels up from this file: project_root/modules/resource_api.py -> project_root
BASE_DIR = Path(__file__).parent.parent
STUB_DIR = BASE_DIR / "data" / "stubs"
STUB_DIR.mkdir(parents=True, exist_ok=True)

# Map certain resource names to specific filenames
RESOURCE_FILE_MAP = {
    "calendar_events": "calendar.json",
}

def _get_resource_path(name: str) -> Path:
    """
    Determine the JSON file path for a given resource name.
    If there's a specific mapping, use that filename; otherwise, default to <name>.json.
    Ensures the stub directory exists.
    """
    filename = RESOURCE_FILE_MAP.get(name, f"{name}.json")
    return STUB_DIR / filename

def list_resources(name: str) -> list:
    """
    Return a list of all resources stored under the given resource name.
    If the file doesn't exist or contains invalid JSON, return an empty list.
    """
    path = _get_resource_path(name)
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except json.JSONDecodeError:
        pass
    return []

def create_resource(name: str, payload: dict) -> dict:
    """
    Append a new payload to the resource file (creating it if necessary),
    and return the payload dict.
    """
    resources = list_resources(name)
    resources.append(payload)
    path = _get_resource_path(name)
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(resources, f, indent=2)
    except OSError:
        # If writing fails (permissions, etc.), we still return the payload
        pass
    return payload

