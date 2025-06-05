import json
import os
from modules import resource_api


def schedule_appointment(doctor_name: str, preferred_date: str) -> dict:
    """Stub to book the earliest 2 PM slot on preferred_date."""
    appt_id = f"appt_{len(resource_api.list_resources('calendar_events')) + 1}"
    appt_datetime = f"{preferred_date}T14:00:00"
    payload = {
        "appt_id": appt_id,
        "doctor": doctor_name,
        "datetime": appt_datetime,
        "location": "123 Main St, Suite 200",
    }
    resource_api.create_resource("calendar_events", payload)
    return payload

