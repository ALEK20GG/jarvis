import os
import time
from core.speak import speak
from core.utils.logger import log

def blocca_schermo(gui=None):
    speak("Blocco lo schermo")
    if gui: gui.add_voice("Blocco lo schermo")
    log("Blocco schermo in corso", "INFO")
    if gui: gui.add_log("Blocco schermo in corso", "INFO")
    time.sleep(1.5)
    os.system("rundll32.exe user32.dll,LockWorkStation")

def spegni_pc(gui=None):
    speak("Spegniamo il computer. A presto!")
    if gui: gui.add_voice("Spegniamo il computer. A presto!")
    log("Spegnimento PC in corso", "INFO")
    if gui: gui.add_log("Spegnimento PC in corso", "INFO")
    time.sleep(3)
    os.system("shutdown /s /t 1")

def riavvia_pc(gui=None):
    speak("Riavviando il computer.")
    if gui: gui.add_voice("Riavviando il computer.")
    log("Riavvio PC in corso", "INFO")
    if gui: gui.add_log("Riavvio PC in corso", "INFO")
    time.sleep(3)
    os.system("shutdown /r /t 1")

def disconnetti_utente(gui=None):
    speak("Disconnetto l'utente.")
    if gui: gui.add_voice("Disconnetto l'utente.")
    log("Disconnessione utente in corso", "INFO")
    if gui: gui.add_log("Disconnessione utente in corso", "INFO")
    time.sleep(1.5)
    os.system("shutdown /l")
