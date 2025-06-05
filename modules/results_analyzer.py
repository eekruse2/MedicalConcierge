import json
from modules import resource_api
from config import DEMO_MODE
import openai


def analyze_test_results(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        data = json.load(f)

    if DEMO_MODE:
        analysis = "All values stable."
    else:
        prompt = f"Analyze these lab results:\n{data}"
        resp = openai.ChatCompletion.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}],
        )
        analysis = resp.choices[0].message.content

    result_id = f"result_{len(resource_api.list_resources('lab_results')) + 1}"
    payload = {"id": result_id, "analysis": analysis, "raw": data}
    resource_api.create_resource('lab_results', payload)
    return payload
