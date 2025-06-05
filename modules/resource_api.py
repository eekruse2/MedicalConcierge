from typing import Any, Dict, List

# Simple in-memory resource store for demonstration
RESOURCE_STORE: Dict[str, List[Dict[str, Any]]] = {
    "patient_profile": []
}


def list_resources(name: str) -> List[Dict[str, Any]]:
    """Return all resources of a given type."""
    return RESOURCE_STORE.get(name, [])


def create_resource(name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Append a new resource payload to the in-memory store."""
    RESOURCE_STORE.setdefault(name, []).append(payload)
    return payload
