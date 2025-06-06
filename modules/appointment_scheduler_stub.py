from modules import resource_api

def schedule_appointment(doctor: str, preferred_date: str) -> dict:
    """Schedule an appointment at 2 PM on the preferred_date with the given doctor."""
    # Generate a unique appointment ID based on existing calendar_events
    appt_id = f"appointment_{len(resource_api.list_resources('calendar_events')) + 1}"
    appt_datetime = f"{preferred_date}T14:00:00"
    payload = {
        "id": appt_id,
        "doctor": doctor,
        "datetime": appt_datetime,
        "location": "123 Main St, Suite 200",
    }
    resource_api.create_resource("calendar_events", payload)
    return payload
