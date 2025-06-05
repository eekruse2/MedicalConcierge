import os
import json
from typing import Dict, Any, List

import openai
from modules import resource_api
from config import DEMO_MODE
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""
    return full_text


def chunk_text(full_text: str, max_chars: int = 3000) -> List[str]:
    """Very naive: split every `max_chars` characters."""
    chunks = []
    for i in range(0, len(full_text), max_chars):
        chunks.append(full_text[i : i + max_chars])
    return chunks


def analyze_medical_file(file_path: str) -> Dict[str, Any]:
    """Returns a patient_profile dict."""
    # 1. DEMO_MODE fallback
    if DEMO_MODE and os.path.basename(file_path) == "demo_scan.pdf":
        demo_json_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "demo", "demo_patient_profile.json"
        )
        with open(demo_json_path, "r") as f:
            profile = json.load(f)
        # assign a fake ID if not present
        profile.setdefault(
            "id", f"profile_{len(resource_api.list_resources('patient_profile')) + 1}"
        )
        resource_api.create_resource("patient_profile", profile)
        return profile

    # 2. Otherwise: real extraction
    extracted_text = extract_text_from_pdf(file_path)
    chunks = chunk_text(extracted_text)

    # 3. (Optional) create embeddings for each chunk with o3
    embeddings = []
    for chunk in chunks:
        resp = openai.Embedding.create(model="o3-embedding-1", input=chunk)
        embeddings.append(resp["data"][0]["embedding"])
        # You could store (file_id, chunk_index, embedding) in memory if needed

    # 4. Build a prompt to get structured JSON
    prompt = (
        "You are an AI-powered medical assistant. Summarize the following clinical notes. "
        "Output strictly valid JSON with keys: 'diagnoses' (list of strings), "
        "'medications' (list of strings), "
        "'labs' (list of {name, value, date}), "
        "'provider_info' (clinic name, phone). "
        "Here is the extracted text:\n\n"
        f"{extracted_text}"
    )

    resp = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
    )
    content = resp.choices[0].message.content

    # 5. Parse the JSON string
    profile: Dict[str, Any] = json.loads(content)

    # 6. Assign an ID and store as a resource
    profile_id = f"profile_{len(resource_api.list_resources('patient_profile')) + 1}"
    profile["id"] = profile_id
    resource_api.create_resource("patient_profile", profile)
    return profile
