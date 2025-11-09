import os
import time
from core.speak import speak
from core.utils.logger import log

def blocca_schermo():
    speak("Blocco lo schermo")
    log("Blocco schermo in corso", "INFO")
    time.sleep(1.5)
    os.system("rundll32.exe user32.dll,LockWorkStation")

def spegni_pc():
    speak("Spegniamo il computer. A presto!")
    log("Spegnimento PC in corso", "INFO")
    time.sleep(3)
    os.system("shutdown /s /t 1")

def riavvia_pc():
    speak("Riavviando il computer.")
    log("Riavvio PC in corso", "INFO")
    time.sleep(3)
    os.system("shutdown /r /t 1")

def disconnetti_utente():
    speak("Disconnetto l'utente.")
    log("Disconnessione utente in corso", "INFO")
    time.sleep(1.5)
    os.system("shutdown /l")