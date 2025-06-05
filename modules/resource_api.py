# In-memory resource store
RESOURCE_STORE: Dict[str, List[Dict[str, Any]]] = {}


def list_resources(name: str) -> List[Dict[str, Any]]:
    """Return a list of resources for the given resource type."""
    return RESOURCE_STORE.get(name, [])


def create_resource(name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Append a new resource payload to the in-memory store."""
    RESOURCE_STORE.setdefault(name, []).append(payload)
    return payload
