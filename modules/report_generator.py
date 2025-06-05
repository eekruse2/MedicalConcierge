from modules import resource_api


def generate_doctor_report() -> str:
    profiles = resource_api.list_resources('patient_profiles')
    labs = resource_api.list_resources('lab_results')
    transcripts = resource_api.list_resources('appointment_transcripts')
    report = "Doctor Report\n\n"
    if profiles:
        report += f"Profile ID: {profiles[-1]['id']}\n"
    if labs:
        report += f"Latest Labs: {labs[-1]['analysis']}\n"
    if transcripts:
        report += f"Transcript Summary:\n{transcripts[-1]['content']}\n"
    return report
