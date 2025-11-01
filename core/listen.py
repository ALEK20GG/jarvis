import time
import pyaudio
import speech_recognition as sr
from core.config import RATE, FRAME_SIZE, VAD

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Ascolto in corso...")
        r.energy_threshold = 400
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.6
        try:
            audio_data = r.listen(source, timeout=5, phrase_time_limit=None)
            text = r.recognize_google(audio_data, language="it-IT").lower().strip()
            print(f"🗣️ Testo riconosciuto: '{text}'")
            return text
        except sr.WaitTimeoutError:
            print("⏳ Nessun parlato rilevato.")
            return ""
        except sr.UnknownValueError:
            print("❌ Non ho capito cosa hai detto.")
            return ""
        except sr.RequestError as e:
            print(f"Errore nel riconoscimento vocale: {e}")
            return ""

def listen_with_vad(timeout=10):
    import core.listen as listen_mod
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=FRAME_SIZE)

    print("🎧 In ascolto intelligente...")
    voiced_frames = []
    start_time = time.time()

    while True:
        frame = stream.read(FRAME_SIZE, exception_on_overflow=False)
        if VAD.is_speech(frame, RATE):
            voiced_frames.append(frame)
            if len(voiced_frames) > 5:
                stream.stop_stream()
                stream.close()
                p.terminate()
                return listen_mod.listen()
        if time.time() - start_time > timeout:
            stream.stop_stream()
            stream.close()
            p.terminate()
            return ""
