import os

WATSON_ASSISTANT_BASE_URL = "https://gateway.watsonplatform.net/assistant/api/v2/assistants/b3327761-5928-4000-95d1-c19c0c425c2f"
WATSON_ASSISTANT_API_KEY = os.getenv("WATSON_ASSISTANT_API_KEY")

WATSON_TTS_BASE_URL = (
    "https://gateway-wdc.watsonplatform.net/text-to-speech/api/v1/synthesize"
)
WATSON_STT_BASE_URL = (
    "https://gateway-wdc.watsonplatform.net/speech-to-text/api/v1/recognize"
)
WATSON_TTS_API_KEY = os.getenv("WATSON_TTS_API_KEY")
WATSON_STT_API_KEY = os.getenv("WATSON_STT_API_KEY")
