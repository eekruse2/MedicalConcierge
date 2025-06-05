import openai
from datetime import datetime
from modules import resource_api


def generate_recommendations() -> str:
    """Generate patient recommendations from the latest profile."""
    profiles = resource_api.list_resources("patient_profile")
    if not profiles:
        return "No patient profile found."

    profile = profiles[-1]

    dob = profile.get("dob", "1990-04-12")
    try:
        birth = datetime.fromisoformat(dob)
        age = (datetime.now() - birth).days // 365
    except Exception:
        age = None

    diagnoses = profile.get("diagnoses", [])
    medications = profile.get("medications", [])
    labs = profile.get("labs", [])

    prompt = (
        "You are a medical-AI assistant. The patient is a "
        f"{age}-year-old (DOB {dob}) with diagnoses: {', '.join(diagnoses)}. "
        f"Current medications: {', '.join(medications)}. "
        f"Labs: {labs}.\n\n"
        "1. What lifestyle or medication adjustments are recommended? "
        "2. Which labs or vitals to monitor monthly vs. quarterly? "
        "Please output concise bullet points and cite guidelines (e.g. ADA, ACC)."
    )

    resp = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
