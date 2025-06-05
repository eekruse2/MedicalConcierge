import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import openai

from modules import resource_api


# Folder where reports will be saved if `persist=True`
REPORTS_DIR = Path(__file__).resolve().parent.parent / "data" / "reports"


def _get_latest(resources_list):
    """
    Helper: return the last element of a list, or {} if the list is empty.
    """
    return resources_list[-1] if resources_list else {}


def generate_doctor_report(persist: bool = False) -> Optional[str]:
    """
    Generate a doctor report using the latest patient information.

    1. Tries to load the latest "patient_profile" or "patient_profiles".
    2. Tries to load the latest "test_results_summary" or "lab_results".
    3. Tries to load the latest "calendar_events".
    4. Tries to load the latest "appointment_transcripts".

    If `persist` is True, the generated report is written to:
        data/reports/doctor_report_<YYYYMMDD_HHMMSS>.txt
    and that file path is returned. Otherwise, the raw report string is returned.

    If any required data is missing, returns a short error string.
    """
    # 1) Load patient demographics
    profiles_a = resource_api.list_resources("patient_profile")
    profiles_b = resource_api.list_resources("patient_profiles")
    profile = _get_latest(profiles_a) or _get_latest(profiles_b)

    # 2) Load lab results / test summaries
    tests_a = resource_api.list_resources("test_results_summary")
    tests_b = resource_api.list_resources("lab_results")
    test_summary = _get_latest(tests_a) or _get_latest(tests_b)

    # 3) Load upcoming/latest appointment event (for date, doctor, location)
    appointments = resource_api.list_resources("calendar_events")
    appointment = _get_latest(appointments)

    # 4) Load latest appointment transcript (for any extra context)
    transcripts = resource_api.list_resources("appointment_transcripts")
    transcript = _get_latest(transcripts)

    # If there's no profile or no lab/test summary or no appointment, bail out.
    if not (profile and test_summary and appointment):
        return "Missing required data to generate report."

    # Extract patient info (with fallbacks)
    patient_name = profile.get("name", "John Doe")
    patient_dob = profile.get("dob", "1970-01-01")
    patient_dx = profile.get("primary_diagnoses", "not available")

    # Extract lab/test analysis (fallback to entire summary text if "analysis" is absent)
    labs_analysis = test_summary.get("analysis") or test_summary.get("summary") or "No lab analysis provided."

    # Extract appointment info
    doctor_name = appointment.get("doctor", "Unknown")
    appt_datetime = appointment.get("datetime", "Unknown date/time")
    location = appointment.get("location", "Unknown location")

    # If the appointment transcript has extra content, include a short excerpt
    transcript_excerpt = ""
    if transcript:
        full_text = transcript.get("content", "")
        # Truncate to the first 200 characters, if lengthy
        if len(full_text) > 200:
            transcript_excerpt = full_text[:200].rstrip() + "…"
        else:
            transcript_excerpt = full_text

    # Build the prompt for the AI scribe
    prompt_lines = [
        f"You are an AI medical scribe. Write a one‐page, “Dear Dr. {doctor_name}, …” letter summarizing:",
        f"• Patient: {patient_name} (DOB {patient_dob}) with primary diagnoses: {patient_dx}.",
        f"• Lab trends / analysis: {labs_analysis}.",
        f"• Upcoming appointment: {appt_datetime} at {location}.",
    ]
    if transcript_excerpt:
        prompt_lines.append(f"• Recent appointment transcript highlights (excerpt): {transcript_excerpt}.")
    prompt_lines.append("• Proposed medication or lifestyle changes (if any).")
    prompt_lines.append("End with “Sincerely, Your AI Assistant.”")

    full_prompt = "\n".join(prompt_lines)

    # Call OpenAI's ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-4-1",  # or your preferred-compatible model name
        messages=[{"role": "user", "content": full_prompt}],
    )
    report_text = response.choices[0].message.content.strip()

    # If requested, save the report to disk
    if persist:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"doctor_report_{timestamp}.txt"
        file_path = REPORTS_DIR / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        return str(file_path)

    return report_text

