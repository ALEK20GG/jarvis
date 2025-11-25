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
from core.functions.audio import alza_volume, abbassa_volume, muto
from core.functions.brightness import alza_luminosita, abbassa_luminosita
from core.functions.system import blocca_schermo, spegni_pc, riavvia_pc, disconnetti_utente

open_processes = {}

def apri_app(app_name, gui=None):
    app_name = app_name.lower().strip()
    best_match, score, _ = process.extractOne(app_name, APP_PATHS.keys())
    if score < 80:
        speak(f"Non conosco l'app {app_name}")
        if gui: gui.add_voice(f"Non conosco l'app {app_name}")
        log(f"App non trovata: {app_name}", "WARNING")
        if gui: gui.add_log(f"App non trovata: {app_name}", "WARNING")
        return
    path = APP_PATHS[best_match]
    try:
        process_obj = subprocess.Popen([path])
        open_processes[best_match] = process_obj
        speak(f"Apro {best_match}")
        if gui: gui.add_voice(f"Apro {best_match}")
        log(f"Aperta app: {best_match} ({path})", "SUCCESS")
        if gui: gui.add_log(f"Aperta app: {best_match} ({path})", "SUCCESS")
    except Exception as e:
        speak(f"Errore nell'apertura di {best_match}")
        if gui: gui.add_voice(f"Errore nell'apertura di {best_match}")
        log(f"Errore nell'apertura di {best_match}: {e}", "ERROR")
        if gui: gui.add_log(f"Errore nell'apertura di {best_match}: {e}", "ERROR")


def chiudi_app(app_name, gui=None):
    app_name = app_name.lower()
    if app_name in open_processes:
        process = open_processes[app_name]
        process.terminate()
        del open_processes[app_name]
        speak(f"Chiudo {app_name}")
        if gui: gui.add_voice(f"Chiudo {app_name}")
        log(f"Chiusa app: {app_name}", "SUCCESS")
        if gui: gui.add_log(f"Chiusa app: {app_name}", "SUCCESS")
        return
    target_proc = PROCESS_ALIASES.get(app_name, app_name)
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and target_proc in proc.info['name'].lower():
            proc.terminate()
            speak(f"Chiudo {app_name}")
            if gui: gui.add_voice(f"Chiudo {app_name}")
            log(f"Chiusa app: {app_name}", "SUCCESS")
            if gui: gui.add_log(f"Chiusa app: {app_name}", "SUCCESS")
            return
    speak(f"Non trovo nessuna app aperta chiamata {app_name}")
    if gui: gui.add_voice(f"Non trovo nessuna app aperta chiamata {app_name}")
    log(f"App da chiudere non trovata: {app_name}", "WARNING")
    if gui: gui.add_log(f"App da chiudere non trovata: {app_name}", "WARNING")


def execute_command(command, jarvis_active, from_where, gui=None):
    command = command.lower()

    # Ricerca Google
    if "cerca" in command or "ricerca" in command:
        query = command.replace("cerca", "").replace("ricerca", "").strip()
        if not query:
            speak("Cosa vuoi cercare?")
            if gui: gui.add_voice("Cosa vuoi cercare?")
        else:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            speak(f"Cerco {query} su Google")
            if gui: gui.add_voice(f"Cerco {query} su Google")
            log(f"Ricerca Google: {query}", "INFO")
            if gui: gui.add_log(f"Ricerca Google: {query}", "INFO")
            jarvis_active = False

    # Apri app
    elif "apri" in command:
        app_name = command.replace("apri", "").strip()
        if fuzz.ratio(command, "apri google") > RESPONSE_PRECISION:
            webbrowser.open("https://www.google.com")
            speak("Apro Google")
            if gui: gui.add_voice("Apro Google")
            log("Aperto Google", "INFO")
            if gui: gui.add_log("Aperto Google", "INFO")
        elif fuzz.ratio(command, "apri youtube") > RESPONSE_PRECISION:
            webbrowser.open("https://www.youtube.com")
            speak("Apro YouTube")
            if gui: gui.add_voice("Apro YouTube")
            log("Aperto YouTube", "INFO")
            if gui: gui.add_log("Aperto YouTube", "INFO")
        elif fuzz.ratio(command, "apri visual studio code") > RESPONSE_PRECISION or fuzz.ratio(command, "programmiamo") > RESPONSE_PRECISION:
            apri_app("visual studio code", gui=gui)
        else:
            apri_app(app_name, gui=gui)
        jarvis_active = False

    # Chiudi app
    elif "chiudi" in command:
        app_name = command.replace("chiudi", "").strip()
        chiudi_app(app_name, gui=gui)
        jarvis_active = False

    # Comandi base con fuzzy matching
    matched_command = None
    best_score = 0
    for key in COMMANDS:
        score = fuzz.ratio(command, key)
        if score > best_score:
            best_score = score
            matched_command = key

    if best_score >= RESPONSE_PRECISION:
        COMMANDS[matched_command](gui=gui)
        jarvis_active = False
    else:
        if from_where != "command_inline":
            speak("Comando non riconosciuto, ripeti.")
            if gui: gui.add_voice("Comando non riconosciuto, ripeti.")
            log(f"Comando non riconosciuto: {command}", "WARNING")
            if gui: gui.add_log(f"Comando non riconosciuto: {command}", "WARNING")

    return jarvis_active
