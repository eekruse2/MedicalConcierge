import openai
from datetime import datetime
from modules import resource_api
from config import DEMO_MODE


def generate_recommendations() -> str:
    """Generate patient recommendations from the latest profile."""
    profiles = resource_api.list_resources("patient_profile")
    if not profiles:
        return "No patient profile found."

    # If running in demo mode, return a simple stubbed recommendation.
    if DEMO_MODE:
        return (
            "- Encourage at least 150 minutes of moderate-intensity exercise per week\n"
            "- Adopt a low-sodium diet\n"
            "- Ensure medication adherence and schedule regular follow-ups\n"
            "- Monitor blood pressure and blood glucose at home\n"
            "- Schedule HbA1c every 3 months and lipid panel every 6 months"
        )

    profile = profiles[-1]

    dob = profile.get("dob", "")
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
        "2. Which labs or vitals should be monitored monthly vs. quarterly? "
        "Please output concise bullet points and cite relevant guidelines (e.g., ADA, ACC)."
    )

    resp = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
