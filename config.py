import os

# Retrieve your OpenAI API key from the environment variable OPEN_API_KEY,
# otherwise default to a test key.
OPEN_API_KEY = os.getenv("OPEN_API_KEY", "sk-test")

# Flag to toggle expensive operations such as OCR or embeddings.
DEMO_MODE = True
