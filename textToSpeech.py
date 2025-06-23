from typing import Final
from pyt2s.services.stream_elements import requestTTS, Voice

def TextToSpeech(text: str):
    data: Final = requestTTS(text=text, voice=Voice.Joanna.value)
    return data
