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
# Handle della console per nascondere/mostrare
hwnd = ctypes.windll.kernel32.GetConsoleWindow()

# Lock per la funzione speak
engine_lock = threading.Lock()

# Stato di attivazione di Jarvis per ricezione comandi
jarvis_active = False

# Dizionario app (nome -> percorso eseguibile)
APP_PATHS = {
    "visual studio code": r"C:\Users\alezl\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": r"C:\Windows\System32\notepad.exe",
    "calcolatrice": r"C:\Windows\System32\calc.exe"
}

# Alias per i nomi dei processi (nome parlato -> nome processo)
PROCESS_ALIASES = {
    "microsoft store": "winstore.app.exe",
    "store": "winstore.app.exe",
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
}


# Per tenere traccia dei processi aperti per poi killarli senza problemi
open_processes = {}


def hide_console():
    ctypes.windll.user32.ShowWindow(hwnd, 0)

def show_console():
    ctypes.windll.user32.ShowWindow(hwnd, 5)  # SW_SHOW = 5

def speak(text):
    def _speak():
        with engine_lock:
            try:
                # Voce maschile italiana
                voice = "it-IT-DiegoNeural"
                output_file = f"temp_{uuid.uuid4()}.mp3"

                # Genera file audio
                asyncio.run(edge_tts.Communicate(text, voice=voice).save(output_file))

                print(f"Jarvis dice: {text}")
                playsound(output_file)
                os.remove(output_file)
            except Exception as e:
                print(f"Errore nel TTS: {e}")
    threading.Thread(target=_speak, daemon=True).start()

def listen(timeout=5, max_silence=1.5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Ascolto in corso... (parla pure)")

        # Regolazione più aggressiva del rumore
        r.energy_threshold = 400  # livello minimo di energia per considerare “voce”
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.6   # tempo minimo di silenzio per terminare una frase

        try:
            # Ascolta fino al timeout + pausa
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

def apri_app(app_name):
    app_name = app_name.lower().strip()

    # Ricerca fuzzy se vuoi maggiore tolleranza (es. “apri il blocco note”)
    from rapidfuzz import process
    best_match, score, _ = process.extractOne(app_name, APP_PATHS.keys())
    if score < 80:  # soglia di confidenza
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

    # Cerca alias
    target_proc = PROCESS_ALIASES.get(app_name, app_name)

    # Cerca tramite nome processo
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and target_proc in proc.info['name'].lower():
            proc.terminate()
            speak(f"Chiudo {app_name}")
            return

    speak(f"Non trovo nessuna app aperta chiamata {app_name}")


def execute_command(command):
    """Esegue comandi di base, facilmente espandibile"""
    command = command.lower()
    global jarvis_active
    
    if "cerca" in command or "ricerca" in command:
        query = command.replace("cerca", "").replace("ricerca", "").strip()
        if not query:
            speak("cosa vuoi cercare?")
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
    elif fuzz.ratio(command, "che ore sono") > 80:
        ora = datetime.now().strftime("%H:%M")
        speak(f"Sono le {ora}")
        jarvis_active = False
            
    elif fuzz.ratio(command, "apri google") > 80:
        webbrowser.open("https://www.google.com")
        speak("Apro Google")
        jarvis_active = False
        
    elif fuzz.ratio(command, "apri youtube") > 80:
        webbrowser.open("https://www.youtube.com")
        speak("Apro YouTube")
        jarvis_active = False
        
    elif fuzz.ratio(command, "ciao") > 80:
        speak("Ciao! Come posso aiutarti?")

    elif fuzz.ratio(command, "protocollo stand-by") > 80:
        speak("Attivazione protocollo standby. A presto!")
        time.sleep(6)
        exit(0)

    elif fuzz.ratio(command, "protocollo see-trough") > 80:
        speak("Mostro la console. Rimango a tua disposizione.")
        show_console()

    elif fuzz.ratio(command, "protocollo blindness") > 80:
        speak("Nascondo la console. Rimango a tua disposizione.")
        hide_console()
        
    else:
        speak("Comando non riconosciuto, ripeti.")

# -----------------------------
# Loop principale
hide_console()
speak("Buongiorno signore, sono a sua disposizione!")

while True:
    text = listen()

    if not jarvis_active and fuzz.ratio(text, "jarvis") > 70:
        jarvis_active = True
        speak("Sì, sono qui. Dimmi pure.")
        continue

    if jarvis_active:
        if not text:
            continue  # se non capisce nulla, resta in ascolto
        execute_command(text)

    time.sleep(0.3)
