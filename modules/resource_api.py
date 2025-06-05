import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STUB_DIR = os.path.join(BASE_DIR, 'data', 'stubs')

RESOURCE_FILE_MAP = {
    'calendar_events': 'calendar.json',
}


def _get_resource_path(name: str) -> str:
    filename = RESOURCE_FILE_MAP.get(name, f"{name}.json")
    os.makedirs(STUB_DIR, exist_ok=True)
    return os.path.join(STUB_DIR, filename)


def list_resources(name: str) -> list:
    """Return a list of resources stored for the given name."""
    path = _get_resource_path(name)
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except json.JSONDecodeError:
        pass
    return []


def create_resource(name: str, payload: dict) -> dict:
    """Append a new payload to the resource file."""
    resources = list_resources(name)
    resources.append(payload)
    path = _get_resource_path(name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(resources, f, indent=2)
    return payload
