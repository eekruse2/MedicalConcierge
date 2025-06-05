_resources = {}

def list_resources(resource_type: str):
    return _resources.get(resource_type, [])


def create_resource(resource_type: str, data):
    _resources.setdefault(resource_type, []).append(data)
    return data
