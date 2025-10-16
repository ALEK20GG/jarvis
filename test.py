import speech_recognition as sr
import pyttsx3
import pyautogui
import requests
import webbrowser
import ctypes

try:
    import win32gui, win32con
    print("pywin32 import OK")
except ImportError:
    print("Errore: pywin32 non trovato")

# ---- Test nascondere finestra console ----
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
print("La finestra della console dovrebbe essere nascosta ora (riapri per verificare)")

# ---- Test sintesi vocale ----
engine = pyttsx3.init()
engine.say("Ciao! Sto testando tutte le librerie. Se mi senti, funziona!")
engine.runAndWait()
print("pyttsx3 OK")

# ---- Test microfono ----
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Parla qualcosa per testare il microfono...")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="it-IT")
    print(f"Hai detto: {text}")
except sr.UnknownValueError:
    print("Non ho capito il parlato")
except sr.RequestError as e:
    print(f"Errore servizio Google Speech Recognition; {e}")

# ---- Test pyautogui ----
screen_width, screen_height = pyautogui.size()
print(f"pyautogui OK - Risoluzione schermo: {screen_width}x{screen_height}")

# ---- Test requests ----
try:
    response = requests.get("https://api.github.com")
    print(f"requests OK - Status code: {response.status_code}")
except Exception as e:
    print(f"Errore requests: {e}")

# ---- Test webbrowser ----
print("Aprendo una pagina web di prova...")
webbrowser.open("https://www.google.com")
