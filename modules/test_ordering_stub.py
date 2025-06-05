from modules import resource_api


def order_tests(tests):
    order_id = f"order_{len(resource_api.list_resources('test_orders')) + 1}"
    payload = {"id": order_id, "tests": tests}
    resource_api.create_resource('test_orders', payload)
    return payload
