import subprocess
import psutil
import time
import webbrowser
from datetime import datetime
from rapidfuzz import fuzz, process
from core.speak import speak
from core.config import APP_PATHS, PROCESS_ALIASES, RESPONSE_PRECISION
from main import hide_console, show_console

open_processes = {}

def apri_app(app_name):
    app_name = app_name.lower().strip()
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

def execute_command(command, jarvis_active):
    command = command.lower()

    # Ricerca Google
    if "cerca" in command or "ricerca" in command:
        query = command.replace("cerca", "").replace("ricerca", "").strip()
        if not query:
            speak("Cosa vuoi cercare?")
        else:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            speak(f"Cerco {query} su Google")
            jarvis_active = False

    # Apri app
    elif "apri" in command:
        app_name = command.replace("apri", "").strip()
        if fuzz.ratio(command, "apri google") > RESPONSE_PRECISION:
            webbrowser.open("https://www.google.com")
            speak("Apro Google")
        elif fuzz.ratio(command, "apri youtube") > RESPONSE_PRECISION:
            webbrowser.open("https://www.youtube.com")
            speak("Apro YouTube")
        elif fuzz.ratio(command, "apri visual studio code") > RESPONSE_PRECISION or fuzz.ratio(command, "programmiamo") > RESPONSE_PRECISION:
            apri_app("visual studio code")
        else:
            apri_app(app_name)
        jarvis_active = False

    # Chiudi app
    elif "chiudi" in command:
        app_name = command.replace("chiudi", "").strip()
        chiudi_app(app_name)
        jarvis_active = False

    # Che ore sono
    elif fuzz.ratio(command, "che ore sono") > RESPONSE_PRECISION:
        ora = datetime.now().strftime("%H:%M")
        speak(f"Sono le {ora}")
        jarvis_active = False

    # Saluti
    elif fuzz.ratio(command, "ciao") > RESPONSE_PRECISION:
        speak("Ciao! Come posso aiutarti?")

    # Protocollo e gestione console
    elif fuzz.ratio(command, "protocollo stand-by") > RESPONSE_PRECISION:
        speak("Attivazione protocollo standby. A presto!")
        time.sleep(6)
        exit(0)
    elif fuzz.ratio(command, "protocollo see-trough") > RESPONSE_PRECISION:
        speak("Mostro la console. Rimango a tua disposizione.")
        show_console()
    elif fuzz.ratio(command, "protocollo blindness") > RESPONSE_PRECISION:
        speak("Nascondo la console. Rimango a tua disposizione.")
        hide_console()

    # Comando non riconosciuto
    else:
        speak("Comando non riconosciuto, ripeti.")

    return jarvis_active
