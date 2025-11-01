# -------------------- Imports --------------------
import speech_recognition as sr
import ctypes
import time
from datetime import datetime
import webbrowser
import subprocess
from rapidfuzz import fuzz
import threading
import asyncio
import edge_tts
from playsound import playsound
import os
import uuid
import psutil
import webrtcvad
import pyaudio
import numpy as np

# -------------------- Configurazioni globali --------------------
# precisione richiesta per similarità comandi
response_precision = 80  # Soglia di similarità x comandi (0-100)
jarvis_activation_precision = 70  # Soglia di similarità per attivazione Jarvis

# Handle console
hwnd = ctypes.windll.kernel32.GetConsoleWindow()

# Lock per la funzione speak
engine_lock = threading.Lock()

# Stato di attivazione di Jarvis
jarvis_active = False

# Configurazione VAD (voice activity detection)
vad = webrtcvad.Vad(2)  # 0 = meno sensibile, 3 = più sensibile
RATE = 16000 # 16kHz
FRAME_DURATION = 30  # ms
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000) # Numero di campioni per frame

# Sensibilità adattiva
last_check = 0
BASE_ENERGY_THRESHOLD = 400  # soglia di partenza
THRESHOLD = BASE_ENERGY_THRESHOLD
CHECK_INTERVAL = 3  # ogni quanti secondi ricalcolare la soglia

# Dizionari app / processi
APP_PATHS = {
    "visual studio code": r"C:\Users\alezl\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": r"C:\Windows\System32\notepad.exe",
    "calcolatrice": r"C:\Windows\System32\calc.exe"
}

PROCESS_ALIASES = {
    "microsoft store": "winstore.app.exe",
    "store": "winstore.app.exe",
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
}

open_processes = {}

# -------------------- Utility --------------------
def hide_console(): ctypes.windll.user32.ShowWindow(hwnd, 0) # 0 = nascondi console
def show_console(): ctypes.windll.user32.ShowWindow(hwnd, 5) # 5 = mostra console

# -------------------- Sintesi vocale --------------------
def speak(text):
    def _speak(): #doppio speak per threading
        with engine_lock:
            try:
                voice = "it-IT-DiegoNeural"
                output_file = f"temp_{uuid.uuid4()}.mp3" # file temporaneo unico per generazione speak
                asyncio.run(edge_tts.Communicate(text, voice=voice).save(output_file))
                print(f"Jarvis dice: {text}")
                playsound(output_file)
                os.remove(output_file)
            except Exception as e:
                print(f"Errore nel TTS: {e}")
    threading.Thread(target=_speak, daemon=True).start()

# -------------------- Sensibilità adattiva --------------------

def get_ambient_volume(duration=1.0):
    """Registra per un breve periodo e calcola il volume medio assoluto"""
    try:
        import sounddevice as sd
        audio = sd.rec(int(duration * RATE), samplerate=RATE, channels=1, dtype='int16')
        sd.wait()
        volume = np.mean(np.abs(audio))
        return volume
    except Exception as e:
        print(f"[ERRORE AUDIO]: {e}")
        return 0

def update_threshold():
    """Aggiorna la soglia in base al rumore di fondo"""
    global THRESHOLD
    ambient_volume = get_ambient_volume()
    print(f"[DEBUG] Volume ambiente: {ambient_volume:.2f}")

    # regolazione semplice: aumenta soglia se ambiente rumoroso, abbassa se silenzioso
    if ambient_volume > 700:
        THRESHOLD = BASE_ENERGY_THRESHOLD * 1.5
    elif ambient_volume < 200:
        THRESHOLD = BASE_ENERGY_THRESHOLD * 0.7
    else:
        THRESHOLD = BASE_ENERGY_THRESHOLD
    print(f"[DEBUG] Soglia attuale: {THRESHOLD:.2f}")


# -------------------- Ascolto intelligente --------------------
def listen_with_vad(timeout=10):
    """Usa WebRTC VAD per rilevare voce vera prima di avviare speech_recognition"""
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
        if vad.is_speech(frame, RATE):
            voiced_frames.append(frame)
            if len(voiced_frames) > 5:  # ~150ms di voce rilevata
                print("🗣️ Voce rilevata, avvio riconoscimento...")
                stream.stop_stream()
                stream.close()
                p.terminate()
                return listen()  # passa al tuo riconoscimento vocale
        if time.time() - start_time > timeout:
            stream.stop_stream()
            stream.close()
            p.terminate()
            return ""

def listen(timeout=5, max_silence=1.5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Ascolto in corso... (parla pure)")
        r.energy_threshold = 400
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.6
        try:
            audio_data = r.listen(source, timeout=timeout, phrase_time_limit=None)
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


# -------------------- Apertura / Chiusura app --------------------
def apri_app(app_name):
    app_name = app_name.lower().strip()
    from rapidfuzz import process
    best_match, score, _ = process.extractOne(app_name, APP_PATHS.keys())
    if score < 80:
        speak(f"Non conosco l'app {app_name}")
        return
    path = APP_PATHS[best_match]
    try:
        process_obj = subprocess.Popen([path])
        open_processes[best_match] = process_obj
        speak(f"Apro {best_match}")
    except Exception as e:
        speak(f"Errore nell'apertura di {best_match}")
        print(e)

def chiudi_app(app_name):
    app_name = app_name.lower()
    if app_name in open_processes:
        process = open_processes[app_name]
        process.terminate()
        del open_processes[app_name]
        speak(f"Chiudo {app_name}")
        return
    target_proc = PROCESS_ALIASES.get(app_name, app_name)
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and target_proc in proc.info['name'].lower():
            proc.terminate()
            speak(f"Chiudo {app_name}")
            return
    speak(f"Non trovo nessuna app aperta chiamata {app_name}")


# -------------------- Comandi --------------------
def execute_command(command):
    global jarvis_active
    command = command.lower()

    if "cerca" in command or "ricerca" in command:
        query = command.replace("cerca", "").replace("ricerca", "").strip()
        if not query:
            speak("Cosa vuoi cercare?")
        else:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            speak(f"Cerco {query} su Google")
            jarvis_active = False

    elif "apri" in command:
        app_name = command.replace("apri", "").strip()
        apri_app(app_name)
        jarvis_active = False

    elif "chiudi" in command:
        app_name = command.replace("chiudi", "").strip()
        chiudi_app(app_name)
        jarvis_active = False

    elif fuzz.ratio(command, "che ore sono") > response_precision:
        ora = datetime.now().strftime("%H:%M")
        speak(f"Sono le {ora}")
        jarvis_active = False

    elif fuzz.ratio(command, "apri google") > response_precision:
        webbrowser.open("https://www.google.com")
        speak("Apro Google")
        jarvis_active = False

    elif fuzz.ratio(command, "apri youtube") > response_precision:
        webbrowser.open("https://www.youtube.com")
        speak("Apro YouTube")
        jarvis_active = False

    elif fuzz.ratio(command, "ciao") > response_precision:
        speak("Ciao! Come posso aiutarti?")

    elif fuzz.ratio(command, "protocollo stand-by") >  response_precision:
        speak("Attivazione protocollo standby. A presto!")
        time.sleep(6)
        exit(0)

    elif fuzz.ratio(command, "protocollo see-trough") > response_precision:
        speak("Mostro la console. Rimango a tua disposizione.")
        show_console()

    elif fuzz.ratio(command, "protocollo blindness") > response_precision:
        speak("Nascondo la console. Rimango a tua disposizione.")
        hide_console()

    else:
        speak("Comando non riconosciuto, ripeti.")


# -------------------- Loop principale --------------------
hide_console()
speak("Buongiorno signore, sono a sua disposizione!")

while True:
    current_time = time.time()
    if current_time - last_check > CHECK_INTERVAL:
        update_threshold()
        last_check = current_time

    text = listen_with_vad()
    if not jarvis_active and fuzz.ratio(text, "jarvis") > jarvis_activation_precision:
        jarvis_active = True
        speak("Sì, sono qui. Dimmi pure.")
        continue
    if jarvis_active and text:
        execute_command(text)
    time.sleep(0.3)
