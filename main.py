import speech_recognition as sr
import ctypes
import time
from datetime import datetime
import webbrowser
import subprocess

# -----------------------------
# Nasconde la finestra della console
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
# -----------------------------

import threading

def speak(text):
    def _speak():
        import pyttsx3
        engine = pyttsx3.init('sapi5')
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        print(f"Jarvis dice: {text}")
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    t = threading.Thread(target=_speak)
    t.start()

def listen(timeout=5, phrase_time_limit=7):
    """
    Ascolta l'audio dal microfono e ritorna il testo riconosciuto.
    Gestisce gli errori e i timeout senza crash.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Adatta al rumore ambientale
        r.adjust_for_ambient_noise(source, duration=1.5)
        print("Ascolto...")
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = r.recognize_google(audio, language="it-IT").lower().strip()
            print(f"Testo riconosciuto: '{text}'")
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Errore Google Speech Recognition: {e}")
            return ""
        except sr.WaitTimeoutError:
            print("Nessun audio rilevato (timeout).")
            return ""

def execute_command(command):
    """Esegue comandi di base, facilmente espandibile"""
    command = command.lower()
    
    if "che ore sono" in command or "ora" in command:
        ora = datetime.now().strftime("%H:%M")
        speak(f"Sono le {ora}")
        
    elif "apri visual studio code" in command or "programmiamo" in command or "vscode" in command or "apri code" in command or "apri visual studio co" in command or "apri visual studio" in command:
        subprocess.Popen(['C:\\Users\\alezl\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'])
        speak("Apro visual studio code")

    elif "apri google" in command or "google" in command:
        webbrowser.open("https://www.google.com")
        speak("Apro Google")
        
    elif "apri youtube" in command or "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Apro YouTube")
        
    elif "ciao" in command or "salve" in command:
        speak("Ciao! Come posso aiutarti?")
        
    else:
        speak("Comando non riconosciuto.")

# -----------------------------
# Loop principale
speak("Sistema avviato. In ascolto della parola chiave Jarvis.")

while True:
    text = listen()
    if "jarvis" in text or "jarvi" in text or "jà" in text:
        speak("Sì, sono qui. Qual è il comando?")
        command = listen()
        if command:
            execute_command(command)
        else:
            speak("Non ho capito il comando.")
    
    time.sleep(0.3)  # piccolo delay per ridurre l’uso di CPU
