import time
from core.speak import speak
from core.utils.logger import log
from core.console_handler import hide_console, show_console

def protocollo_standby(gui=None):
    speak("Attivazione protocollo standby. A presto!")
    if gui: gui.add_voice("Attivazione protocollo standby. A presto!")
    log("Protocollo standby attivato", "INFO")
    if gui: gui.add_log("Protocollo standby attivato", "INFO")
    time.sleep(6)
    exit(0)

def protocollo_see_trough(gui=None):
    speak("Mostro la console. Rimango a tua disposizione.")
    if gui: gui.add_voice("Mostro la console. Rimango a tua disposizione.")
    log("Protocollo see trough attivato", "INFO")
    if gui: gui.add_log("Protocollo see trough attivato", "INFO")
    show_console()

def protocollo_blindness(gui=None):
    speak("Nascondo la console. Rimango a tua disposizione.")
    if gui: gui.add_voice("Nascondo la console. Rimango a tua disposizione.")
    log("Protocollo blindness attivato", "INFO")
    if gui: gui.add_log("Protocollo blindness attivato", "INFO")
    hide_console()
