import os
from openai import OpenAI

client = OpenAI()
from modules import resource_api
from config import DEMO_MODE


def transcribe_and_summarize(file_path: str, is_audio: bool = False) -> str:
    """Transcribe audio or read text and summarize."""
    if DEMO_MODE and os.path.basename(file_path) == "demo_transcript.txt":
        with open(file_path, "r") as f:
            raw_text = f.read()
    else:
        if is_audio:
            txt_path = file_path.rsplit(".", 1)[0] + ".txt"
            with open(txt_path, "r") as f:
                raw_text = f.read()
        else:
            with open(file_path, "r") as f:
                raw_text = f.read()

    prompt = (
        "You are a medical transcription AI. Here is the raw dialogue:\n\n"
        f"{raw_text}\n\n"
        "Produce two sections:\n"
        "1) Transcript (verbatim, preserve speaker labels and timestamps if present).\n"
        "2) Visit Summary (bulleted list of key decisions, med changes, follow-up tasks)."
    )

    resp = client.chat.completions.create(model="gpt-4.1",
    messages=[{"role": "user", "content": prompt}])

    transcript_output = resp.choices[0].message.content
    transcript_id = f"transcript_{len(resource_api.list_resources('appointment_transcripts')) + 1}"
    payload = {"id": transcript_id, "content": transcript_output}
    resource_api.create_resource("appointment_transcripts", payload)
    return transcript_output
