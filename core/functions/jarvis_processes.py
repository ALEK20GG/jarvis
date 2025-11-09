from core.console_handler import hide_console, show_console
import time
from core.speak import speak
from core.utils.logger import log

def protocollo_standby():
    speak("Attivazione protocollo standby. A presto!")
    log("Protocollo standby attivato", "INFO")
    time.sleep(6)
    exit(0)
def protocollo_see_trough():
    speak("Mostro la console. Rimango a tua disposizione.")
    log("Protocollo see trough attivato", "INFO")
    show_console()
    
def protocollo_blindness():    
    speak("Nascondo la console. Rimango a tua disposizione.")
    log("Protocollo blindness attivato", "INFO")
    hide_console()   