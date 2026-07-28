import os


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    "demo-openai-key"
)

ELEVENLABS_API_KEY = os.getenv(
    "ELEVENLABS_API_KEY",
    "demo-elevenlabs-key"
)

DEEPGRAM_API_KEY = os.getenv(
    "DEEPGRAM_API_KEY",
    "demo-deepgram-key"
)