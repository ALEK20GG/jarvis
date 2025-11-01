import threading
import asyncio
import edge_tts
from playsound import playsound
import os
import uuid

engine_lock = threading.Lock()

def speak(text):
    def _speak():
        with engine_lock:
            try:
                voice = "it-IT-DiegoNeural"
                output_file = f"temp_{uuid.uuid4()}.mp3"
                asyncio.run(edge_tts.Communicate(text, voice=voice).save(output_file))
                print(f"Jarvis dice: {text}")
                playsound(output_file)
                os.remove(output_file)
            except Exception as e:
                print(f"Errore nel TTS: {e}")
    threading.Thread(target=_speak, daemon=True).start()
