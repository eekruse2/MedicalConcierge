import os

# Placeholder for your OpenAI API key.
# The application reads from the environment variable OPEN_API_KEY
# if it is set; otherwise this placeholder string is used.
OPEN_API_KEY = os.getenv("OPEN_API_KEY", "YOUR_OPENAI_API_KEY")

# Flag to toggle expensive operations such as OCR or embedding.
DEMO_MODE = True
