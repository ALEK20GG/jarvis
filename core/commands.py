import subprocess
import psutil
import time
import os
import webbrowser
from datetime import datetime
from rapidfuzz import fuzz, process
from core.utils.logger import log
from core.speak import speak
from core.config import APP_PATHS, PROCESS_ALIASES, RESPONSE_PRECISION, COMMANDS
from core.console_handler import hide_console, show_console
from core.functions.audio import alza_volume, abbassa_volume, muto
from core.functions.brightness import alza_luminosita, abbassa_luminosita
from core.functions.system import blocca_schermo, spegni_pc, riavvia_pc, disconnetti_utente

open_processes = {}

def apri_app(app_name):
    app_name = app_name.lower().strip()
    best_match, score, _ = process.extractOne(app_name, APP_PATHS.keys())
    if score < 80:
        speak(f"Non conosco l'app {app_name}")
        log(f"App non trovata: {app_name}", "WARNING")
        return
    path = APP_PATHS[best_match]
    try:
        process_obj = subprocess.Popen([path])
        open_processes[best_match] = process_obj
        speak(f"Apro {best_match}")
        log(f"Aperta app: {best_match} ({path})", "SUCCESS")
    except Exception as e:
        speak(f"Errore nell'apertura di {best_match}")
        log(f"Errore nell'apertura di {best_match}: {e}", "ERROR")

def chiudi_app(app_name):
    app_name = app_name.lower()
    if app_name in open_processes:
        process = open_processes[app_name]
        process.terminate()
        del open_processes[app_name]
        speak(f"Chiudo {app_name}")
        log(f"Chiusa app: {app_name}", "SUCCESS")
        return
    target_proc = PROCESS_ALIASES.get(app_name, app_name)
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and target_proc in proc.info['name'].lower():
            proc.terminate()
            speak(f"Chiudo {app_name}")
            log(f"Chiusa app: {app_name}", "SUCCESS")
            return
    speak(f"Non trovo nessuna app aperta chiamata {app_name}")
    log(f"App da chiudere non trovata: {app_name}", "WARNING")

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
            log(f"Ricerca Google: {query}", "INFO")
            jarvis_active = False

    # Apri app
    elif "apri" in command:
        app_name = command.replace("apri", "").strip()
        if fuzz.ratio(command, "apri google") > RESPONSE_PRECISION:
            webbrowser.open("https://www.google.com")
            speak("Apro Google")
            log("Aperto Google", "INFO")
        elif fuzz.ratio(command, "apri youtube") > RESPONSE_PRECISION:
            webbrowser.open("https://www.youtube.com")
            speak("Apro YouTube")
            log("Aperto YouTube", "INFO")
        elif fuzz.ratio(command, "apri visual studio code") > RESPONSE_PRECISION or fuzz.ratio(command, "programmiamo") > RESPONSE_PRECISION:
            apri_app("visual studio code")
            log("Aperto Visual Studio Code", "INFO")
        else:
            apri_app(app_name)
            log(f"Aperta app: {app_name}", "INFO")
        jarvis_active = False

    # Chiudi app
    elif "chiudi" in command:
        app_name = command.replace("chiudi", "").strip()
        chiudi_app(app_name)
        log(f"Chiusa app: {app_name}", "INFO")
        jarvis_active = False
    
    # -------------------- Comandi base con fuzzy matching --------------------
    matched_command = None
    best_score = 0
    for key in COMMANDS:
        score = fuzz.ratio(command, key)
        if score > best_score:
            best_score = score
            matched_command = key

    if best_score >= RESPONSE_PRECISION:
        COMMANDS[matched_command]()
        jarvis_active = False
    else:
        speak("Comando non riconosciuto, ripeti.")
        log(f"Comando non riconosciuto: {command}", "WARNING")

    return jarvis_active
