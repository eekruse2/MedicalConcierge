# AI Medical Concierge Demo

This project provides a small FastAPI application demonstrating a medical concierge workflow.

## Quick start

1. Ensure you have **Python 3.10** or newer installed.
2. Clone this repository and change into the project directory:

   ```bash
   git clone <repo-url>
   cd tryit
   ```
3. (Optional) Create and activate a virtual environment.
4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```
5. Provide your OpenAI API key (replace `<your-key>` with the actual key):

   ```bash
   export OPENAI_API_KEY=<your-key>
   ```
6. Start the application using Uvicorn:

   ```bash
   uvicorn app:app --reload
   ```

The server will be available at `http://127.0.0.1:8000`. Uploaded files are stored under the `data/` directory:

- `data/medical_files` – uploaded medical files (PDFs)
- `data/results` – lab result files
- `data/appointments` – appointment transcripts
- `data/stubs` – stub JSON resources used by the demo
