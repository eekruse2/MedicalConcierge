import json
import os
from typing import Any, Dict, List

# In-memory store that mirrors "Resource API"
_RESOURCES: Dict[str, List[Dict[str, Any]]] = {
    "uploaded_medical_files": [],
    "patient_profile": [],
    "test_orders": [],
    "test_results": [],
    "calendar_events": [],
    "test_results_summary": [],
    "appointment_transcripts": [],
}

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def create_resource(resource_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate openai.Resource.create(...)
    Persist to memory (and optionally append to a JSON file so state persists across runs)."""
    _RESOURCES.setdefault(resource_name, []).append(payload)
    # Optionally: write _RESOURCES[resource_name] to f"{DATA_DIR}/stubs/{resource_name}.json"
    return payload


def list_resources(resource_name: str) -> List[Dict[str, Any]]:
    """Simulate openai.Resource.list(resource_name=...)"""
    return _RESOURCES.get(resource_name, [])


def get_resource_by_id(resource_name: str, resource_id: str) -> Dict[str, Any]:
    for r in _RESOURCES.get(resource_name, []):
        if r.get("id") == resource_id:
            return r
    raise KeyError(f"No resource with id={resource_id} in {resource_name}")


# (Optional) helper to persist the JSON stubs on disk
def persist_stubs():
    os.makedirs(os.path.join(DATA_DIR, "stubs"), exist_ok=True)
    for name, items in _RESOURCES.items():
        with open(os.path.join(DATA_DIR, "stubs", f"{name}.json"), "w") as f:
            json.dump(items, f, indent=2)
