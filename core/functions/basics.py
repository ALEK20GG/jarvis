from datetime import datetime
from core.speak import speak
from core.utils.logger import log

def ora_attuale(gui=None):
    ora = datetime.now().strftime("%H:%M")
    speak(f"Sono le {ora}")
    if gui: gui.add_voice(f"Sono le {ora}")
    log(f"Ora attuale fornita: {ora}", "INFO")
    if gui: gui.add_log(f"Ora attuale fornita: {ora}", "INFO")

def saluti(gui=None):
    speak("Ciao! Come posso aiutarti?")
    if gui: gui.add_voice("Ciao! Come posso aiutarti?")
    log("Saluto l'utente", "INFO")
    if gui: gui.add_log("Saluto l'utente", "INFO")
