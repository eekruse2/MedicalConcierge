import json
from pathlib import Path
from typing import List, Dict, Any

# Base directory is two levels up from this file (project_root/modules/resource_api.py → project_root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Directory where “data” lives, and specifically where stubs are stored
DATA_DIR = BASE_DIR / "data"
STUB_DIR = DATA_DIR / "stubs"

# Ensure the stubs directory exists
STUB_DIR.mkdir(parents=True, exist_ok=True)

# Map certain resource names to specific filenames under the stubs directory
RESOURCE_FILE_MAP: Dict[str, str] = {
    "calendar_events": "calendar.json",
    # You can add other mappings here if needed
}

def _get_stub_path(resource_name: str) -> Path:
    """
    Determine the JSON file path for a given resource name in the stubs directory.
    If there's a specific mapping, use that filename; otherwise, default to <resource_name>.json.
    """
    filename = RESOURCE_FILE_MAP.get(resource_name, f"{resource_name}.json")
    return STUB_DIR / filename

def list_resources(resource_name: str) -> List[Dict[str, Any]]:
    """
    Load all JSON resources of a given type.

    1) If a folder named data/<resource_name>/ exists, read every .json file inside,
       parse them individually, and return a list of parsed objects (one per file).
    2) Otherwise, fall back to reading data/stubs/<mapped_filename>.json as a single JSON list
       (if that file exists and contains a JSON array).
    3) If neither exists or parsing fails, return an empty list.
    """
    # 1) Check for a directory of individual JSON files at data/<resource_name>/
    directory = DATA_DIR / resource_name
    if directory.is_dir():
        resources: List[Dict[str, Any]] = []
        for file_path in sorted(directory.glob("*.json")):
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    parsed = json.load(f)
                    # Only append if it is a dictionary (object)
                    if isinstance(parsed, dict):
                        resources.append(parsed)
            except json.JSONDecodeError:
                # Skip any invalid JSON file
                continue
        return resources

    # 2) Fall back to a single stub file under data/stubs/
    stub_path = _get_stub_path(resource_name)
    if stub_path.exists():
        try:
            with stub_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                # Only return if it's a list of objects
                if isinstance(data, list):
                    return data  # type: ignore
        except json.JSONDecodeError:
            pass

    # 3) Nothing found or parse failures
    return []

def create_resource(resource_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Append a new payload (dict) to the stub file under data/stubs/<resource_name>.json.
    If the stub file doesn't exist yet, it will be created with a JSON array containing this payload.

    Note: This function does NOT write into the per-file directory (data/<resource_name>/). It only
    operates on a single JSON file in data/stubs/. If you need directory-based writes, handle that externally.
    """
    # Load existing list (or get empty list)
    existing = list_resources(resource_name)
    existing.append(payload)

    # Write back to the stub file
    stub_path = _get_stub_path(resource_name)
    try:
        with stub_path.open("w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)
    except OSError:
        # If writing fails (permissions, etc.), we still return the payload.
        pass

    return payload

