from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from modules import (
    document_analyzer,
    recommendation_engine,
    test_ordering_stub,
    results_analyzer,
    appointment_scheduler_stub,
    transcription_processor,
    report_generator,
    resource_api,
)
from config import OPENAI_API_KEY, DEMO_MODE
import openai
import os

app = FastAPI()

# Ensure directories exist
os.makedirs(os.path.join('data', 'medical_files'), exist_ok=True)
os.makedirs(os.path.join('data', 'results'), exist_ok=True)
os.makedirs(os.path.join('data', 'appointments'), exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home():
    html = """
    <html><body>
    <h1>AI Medical Concierge Demo</h1>
    <form action="/upload_medical_file" enctype="multipart/form-data" method="post">
      <label>Upload medical file (PDF):</label>
      <input name="file" type="file">
      <input type="submit" value="Upload & Analyze">
    </form>
    </body></html>
    """
    return HTMLResponse(content=html)


@app.post("/upload_medical_file")
async def upload_medical_file(file: UploadFile = File(...)):
    save_path = os.path.join("data", "medical_files", file.filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())

    profile = document_analyzer.analyze_medical_file(save_path)

    html = f"""
    <html><body>
      <h2>Extracted Patient Profile</h2>
      <pre>{profile}</pre>
      <form action="/recommendations" method="get">
        <button type="submit">Get Recommendations</button>
      </form>
    </body></html>
    """
    return HTMLResponse(content=html)


@app.get("/recommendations")
async def get_recommendations():
    recs = recommendation_engine.generate_recommendations()
    html = f"""
    <html><body>
      <h2>Recommendations</h2>
      <pre>{recs}</pre>
      <form action="/order_tests" method="post">
        <input type="hidden" name="tests" value="CMP,Lipid Panel">
        <button type="submit">Order CMP & Lipid Panel</button>
      </form>
    </body></html>
    """
    return HTMLResponse(content=html)


@app.post("/order_tests")
async def order_tests_endpoint(tests: str = Form(...)):
    test_list = tests.split(",")
    order = test_ordering_stub.order_tests(test_list)
    html = f"""
    <html><body>
      <h2>Test Ordered</h2>
      <pre>{order}</pre>
      <form action="/upload_test_results" enctype="multipart/form-data" method="post">
        <label>Upload test results (JSON):</label>
        <input name="file" type="file">
        <input type="submit" value="Upload Results">
      </form>
    </body></html>
    """
    return HTMLResponse(content=html)


@app.post("/upload_test_results")
async def upload_test_results(file: UploadFile = File(...)):
    save_path = os.path.join("data", "results", file.filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())
    summary = results_analyzer.analyze_test_results(save_path)
    html = f"""
    <html><body>
      <h2>Lab Analysis</h2>
      <pre>{summary['analysis']}</pre>
      <form action="/schedule_appointment" method="post">
        <input type="hidden" name="doctor" value="Dr. Smith">
        <input type="hidden" name="date" value="2025-06-07">
        <button type="submit">Book Appointment</button>
      </form>
    </body></html>
    """
    return HTMLResponse(content=html)


@app.post("/schedule_appointment")
async def schedule_appointment_endpoint(doctor: str = Form(...), date: str = Form(...)):
    appt = appointment_scheduler_stub.schedule_appointment(doctor, date)
    html = f"""
    <html><body>
      <h2>Appointment Booked</h2>
      <pre>{appt}</pre>
      <form action="/upload_transcript" enctype="multipart/form-data" method="post">
        <label>Upload appointment transcript (TXT or WAV):</label>
        <input name="file" type="file">
        <input type="submit" value="Upload Transcript">
      </form>
    </body></html>
    """
    return HTMLResponse(content=html)


@app.post("/upload_transcript")
async def upload_transcript(file: UploadFile = File(...)):
    save_path = os.path.join("data", "appointments", file.filename)
    with open(save_path, "wb") as f:
        f.write(await file.read())
    ext = os.path.splitext(file.filename)[1].lower()
    is_audio = ext in [".wav", ".mp3", ".m4a"]
    transcript_output = transcription_processor.transcribe_and_summarize(save_path, is_audio=is_audio)
    html = f"""
    <html><body>
      <h2>Transcript & Summary</h2>
      <pre>{transcript_output}</pre>
      <form action="/doctor_report" method="get">
        <button type="submit">Generate Doctor Report</button>
      </form>
    </body></html>
    """
    return HTMLResponse(content=html)


@app.get("/doctor_report")
async def doctor_report():
    report_text = report_generator.generate_doctor_report()
    return PlainTextResponse(content=report_text)
