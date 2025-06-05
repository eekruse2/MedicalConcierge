import os

# Retrieve your OpenAI API key from the environment.
#
# The code checks `OPENAI_API_KEY` (the recommended variable name) and defaults
# to a test key if it is not set.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "sk-test"

# Flag to toggle expensive operations such as OCR or embeddings.
DEMO_MODE = True
