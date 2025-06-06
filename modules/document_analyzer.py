import os
import json
from typing import Dict, Any, List

from openai import OpenAI

client = OpenAI()
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
    chunks: List[str] = []
    for i in range(0, len(full_text), max_chars):
        chunks.append(full_text[i : i + max_chars])
    return chunks


def analyze_medical_file(file_path: str) -> Dict[str, Any]:
    """Returns a patient_profile dict after extracting and summarizing the PDF."""
    # 1. DEMO_MODE fallback
    # In demo mode, avoid expensive or network calls and always return the
    # bundled demo profile regardless of the uploaded filename. This prevents
    # internal server errors when running without valid API credentials.
    if DEMO_MODE:
        demo_json_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "demo", "demo_patient_profile.json"
        )
        with open(demo_json_path, "r", encoding="utf-8") as f:
            profile = json.load(f)

        # Assign a unique ID and persist
        next_id = len(resource_api.list_resources("patient_profile")) + 1
        profile.setdefault("id", f"profile_{next_id}")
        resource_api.create_resource("patient_profile", profile)
        return profile

    # 2. Real extraction path
    extracted_text = extract_text_from_pdf(file_path)
    chunks = chunk_text(extracted_text)

    # 3. (Optional) create embeddings for each chunk
    embeddings: List[List[float]] = []
    for chunk in chunks:
        resp = client.embeddings.create(model="o3-embedding-1", input=chunk)
        embeddings.append(resp.data[0].embedding)
        # If desired, store (file_path, chunk_index, embedding) via resource_api or another store

    # 4. Build a prompt to get structured JSON from GPT
    prompt = (
        "You are an AI-powered medical assistant. Summarize the following clinical notes. "
        "Output strictly valid JSON with keys:\n"
        "  - 'diagnoses' (list of strings),\n"
        "  - 'medications' (list of strings),\n"
        "  - 'labs' (list of {name, value, date}),\n"
        "  - 'provider_info' (clinic name and phone).\n\n"
        f"Here is the extracted text:\n\n{extracted_text}"
    )

    resp = client.chat.completions.create(model="gpt-4.1",
    messages=[{"role": "user", "content": prompt}])
    content = resp.choices[0].message.content

    # 5. Parse the JSON string returned by the model
    profile: Dict[str, Any] = json.loads(content)

    # 6. Assign a unique ID and store as a resource
    next_id = len(resource_api.list_resources("patient_profile")) + 1
    profile_id = f"profile_{next_id}"
    profile["id"] = profile_id
    resource_api.create_resource("patient_profile", profile)

    return profile
