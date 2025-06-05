import json
import openai
from modules import resource_api


def analyze_test_results(result_file_path: str) -> dict:
    """Analyze new test results against previous labs and store a summary."""
    # 1. Load new results
    with open(result_file_path, "r", encoding="utf-8") as f:
        new_results = json.load(f)
    new_labs = new_results.get("labs", [])

    # 2. Get previous profile/labs
    profiles = resource_api.list_resources("patient_profile")
    if not profiles:
        raise ValueError("No patient profile to compare against.")
    profile = profiles[-1]
    prev_labs = profile.get("labs", [])

    # 3. Build prompt for GPT-4.1
    prompt = (
        "You are a medical\u2011AI assistant. The patient's previous labs are: "
        f"{prev_labs}. The new labs from {new_results.get('date')} are: {new_labs}.\n\n"
        "1. Describe any trends or changes since last labs.\n"
        "2. Suggest possible medication or lifestyle modifications.\n"
        "3. Should we schedule an appointment with the doctor now? Answer yes or no with rationale.\n"
        "Please output bullet points."
    )

    resp = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
    )
    analysis = resp.choices[0].message.content

    # 4. Store summary
    summary_id = f"summary_{len(resource_api.list_resources('test_results_summary')) + 1}"
    payload = {
        "id": summary_id,
        "analysis": analysis,
        "result_file": result_file_path,
    }
    resource_api.create_resource("test_results_summary", payload)
    return payload

