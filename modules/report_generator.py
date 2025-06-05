"""Utilities for generating doctor reports from stored resources."""

from datetime import datetime
from pathlib import Path
from typing import Optional

import openai

from . import resource_api


REPORTS_DIR = Path(__file__).resolve().parent.parent / "data" / "reports"


def generate_doctor_report(persist: bool = False) -> Optional[str]:
    """Generate a doctor report using the latest patient information.

    If ``persist`` is True, the report text is written to a timestamped file in
    ``data/reports`` and the file path is returned. Otherwise the report text is
    returned directly.
    """
    profiles = resource_api.list_resources("patient_profile")
    summaries = resource_api.list_resources("test_results_summary")
    appointments = resource_api.list_resources("calendar_events")

    if not (profiles and summaries and appointments):
        return "Missing required data to generate report."

    profile = profiles[-1]
    summary = summaries[-1]
    appointment = appointments[-1]

    doctor_name = appointment.get("doctor", "")
    labs_analysis = summary.get("analysis", "")
    appt_datetime = appointment.get("datetime", "")
    location = appointment.get("location", "")

    prompt = (
        f"You are an AI medical scribe. Write a one-page, \"Dear Dr. {doctor_name}, ...\" letter summarizing:\n"
        f"• Patient: {profile.get('name', 'John Doe')} (DOB {profile.get('dob', '1990-01-01')}) and primary diagnoses.\n"
        f"• Lab trends / analysis: {labs_analysis}.\n"
        f"• Upcoming appointment info: {appt_datetime} at {location}.\n"
        "• Proposed medication or lifestyle changes.\n"
        "End with 'Sincerely, Your AI Assistant.'"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
    )
    report_text = response.choices[0].message.content

    if persist:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = REPORTS_DIR / f"doctor_report_{timestamp}.txt"
        with open(file_path, "w") as f:
            f.write(report_text)
        return str(file_path)

    return report_text
