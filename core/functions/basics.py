from datetime import datetime
from core.speak import speak
from core.utils.logger import log

def ora_attuale():
        ora = datetime.now().strftime("%H:%M")
        speak(f"Sono le {ora}")
        log(f"Ora attuale fornita: {ora}", "INFO")

def saluti():
        speak("Ciao! Come posso aiutarti?")
        log("Saluto l'utente", "INFO")
