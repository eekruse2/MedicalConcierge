import os

# Retrieve your OpenAI API key from the environment.
#
# The code first checks `OPENAI_API_KEY` (the recommended variable name). For
# backward compatibility it also falls back to `OPEN_API_KEY` before finally
# defaulting to a test key.
OPENAI_API_KEY = (
    os.getenv("OPENAI_API_KEY")
    or os.getenv("OPEN_API_KEY")
    or "sk-test"
)

# Flag to toggle expensive operations such as OCR or embeddings.
DEMO_MODE = True
