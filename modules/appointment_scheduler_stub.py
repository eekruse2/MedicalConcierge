from modules import resource_api


def schedule_appointment(doctor: str, date: str) -> dict:
    appt_id = f"appointment_{len(resource_api.list_resources('appointments')) + 1}"
    payload = {"id": appt_id, "doctor": doctor, "date": date}
    resource_api.create_resource('appointments', payload)
    return payload
