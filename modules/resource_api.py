RESOURCE_STORE = {}

def create_resource(name: str, payload: dict):
    resources = RESOURCE_STORE.setdefault(name, [])
    resources.append(payload)
    return payload

def list_resources(name: str):
    return RESOURCE_STORE.get(name, [])
