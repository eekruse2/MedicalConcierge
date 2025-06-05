"""Simple stub of the resource API used for demonstration."""

from typing import List, Dict

# A placeholder in-memory resource store
_RESOURCES = {
    "patient_profile": []
}


def list_resources(resource_type: str) -> List[Dict]:
    """Return all resources of a given type."""
    return _RESOURCES.get(resource_type, [])
