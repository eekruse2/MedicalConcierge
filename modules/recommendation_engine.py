from modules import resource_api
from config import DEMO_MODE
import openai


def generate_recommendations() -> str:
    profiles = resource_api.list_resources('patient_profiles')
    if not profiles:
        return "No patient profile available."
    profile = profiles[-1]
    if DEMO_MODE:
        return "- Increase exercise\n- Reduce sodium intake"
    prompt = f"Generate medical recommendations for this patient profile:\n{profile}"
    resp = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
