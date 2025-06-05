import json
from pathlib import Path
from typing import List, Dict, Any

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'


def list_resources(resource_type: str) -> List[Dict[str, Any]]:
    """Load all JSON resources of a given type from data/<resource_type> directory.

    Returns an empty list if the folder does not exist or contains no JSON files.
    """
    folder = DATA_DIR / resource_type
    if not folder.is_dir():
        return []

    resources = []
    for file_path in sorted(folder.glob('*.json')):
        try:
            with open(file_path, 'r') as f:
                resources.append(json.load(f))
        except json.JSONDecodeError:
            continue
    return resources
