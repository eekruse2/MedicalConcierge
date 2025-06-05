import json
import os
from typing import Any, Dict, List

# In-memory store that mirrors "Resource API"
RESOURCE_STORE: Dict[str, List[Dict[str, Any]]] = {
    "uploaded_medical_files": [],
    "patient_profile": [],
    "test_orders": [],
    "test_results": [],
    "calendar_events": [],
    "test_results_summary": [],
    "appointment_transcripts": [],
}

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def create_resource(name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate openai.Resource.create(...)
    Persist to memory (and optionally append to a JSON file so state persists across runs)."""
    RESOURCE_STORE.setdefault(name, []).append(payload)
    return payload


def list_resources(name: str) -> List[Dict[str, Any]]:
    """Simulate openai.Resource.list(resource_name=...)"""
    return RESOURCE_STORE.get(name, [])


def get_resource_by_id(name: str, resource_id: str) -> Dict[str, Any]:
    for r in RESOURCE_STORE.get(name, []):
        if r.get("id") == resource_id:
            return r
    raise KeyError(f"No resource with id={resource_id} in {name}")


def persist_stubs():
    os.makedirs(os.path.join(DATA_DIR, "stubs"), exist_ok=True)
    for name, items in RESOURCE_STORE.items():
        with open(os.path.join(DATA_DIR, "stubs", f"{name}.json"), "w") as f:
            json.dump(items, f, indent=2)
