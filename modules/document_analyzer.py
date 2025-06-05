import os
import json
from config import DEMO_MODE
from modules import resource_api

try:
    from pdfminer.high_level import extract_text
except Exception:
    extract_text = None


def analyze_medical_file(file_path: str) -> dict:
    """Parse a medical PDF into a patient profile."""
    if DEMO_MODE:
        demo_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'demo', 'demo_patient_profile.json')
        with open(demo_path, 'r') as f:
            profile = json.load(f)
    else:
        if extract_text is None:
            raise RuntimeError("pdfminer not available")
        text = extract_text(file_path)
        # In a real implementation we'd call GPT. Here we stub.
        profile = {"raw_text": text}
    profile_id = f"profile_{len(resource_api.list_resources('patient_profiles')) + 1}"
    payload = {"id": profile_id, **profile}
    resource_api.create_resource('patient_profiles', payload)
    return payload
