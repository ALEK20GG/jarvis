import speech_recognition as sr
import ctypes
import time
from datetime import datetime
import webbrowser
import subprocess
from rapidfuzz import fuzz
import threading

# Handle della console per nascondere/mostrare
hwnd = ctypes.windll.kernel32.GetConsoleWindow()

# Lock per la funzione speak
engine_lock = threading.Lock()

# Stato di attivazione di Jarvis per ricezione comandi
jarvis_active = False


def hide_console():
    ctypes.windll.user32.ShowWindow(hwnd, 0)

def show_console():
    ctypes.windll.user32.ShowWindow(hwnd, 5)  # SW_SHOW = 5

def speak(text):
    def _speak():
        import pyttsx3
        with engine_lock:
            engine = pyttsx3.init('sapi5')
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)
            print(f"Jarvis dice: {text}")
            engine.say(text)
            engine.runAndWait()
            engine.stop()
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

def execute_command(command):
    """Esegue comandi di base, facilmente espandibile"""
    command = command.lower()
    global jarvis_active
    
    if fuzz.ratio(command, "che ore sono") > 80:
        ora = datetime.now().strftime("%H:%M")
        speak(f"Sono le {ora}")
        jarvis_active = False
    
    elif fuzz.ratio(command, "apri visual studio code") > 80 or fuzz.ratio(command, "programmiamo") > 80:
        subprocess.Popen(['C:\\Users\\alezl\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'])
        speak("Apro visual studio code")
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
        jarvis_active = False

    elif fuzz.ratio(command, "protocollo stand-by") > 80:
        speak("Attivazione protocollo standby. A presto!")
        time.sleep(4)
        exit(0)

    elif fuzz.ratio(command, "protocollo see-trough") > 60:
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
speak("Sistema avviato. In ascolto della parola chiave Jarvis.")

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
