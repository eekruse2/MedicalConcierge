from datetime import datetime, timedelta
from typing import List

from modules import resource_api


def order_tests(test_types: List[str]) -> dict:
    """Create a stub test order and store it via resource_api."""
    now = datetime.now()
    order_id = f"order_{len(resource_api.list_resources('test_orders')) + 1}"
    payload = {
        "order_id": order_id,
        "tests": test_types,
        "status": "ordered",
        "order_date": now.isoformat(),
        "expected_return": (now + timedelta(days=1)).strftime("%Y-%m-%d"),
    }
    resource_api.create_resource("test_orders", payload)
    return payload
