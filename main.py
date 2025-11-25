# -------------------------------- Basic imports ------------------------------- #
import time
import threading
from rapidfuzz import fuzz

# -------------------------------- Modules imports ----------------------------- #
from core.speak import speak
from core.listen import listen_with_vad
from core.commands import execute_command
from core.config import JARVIS_ACTIVATION_PRECISION
from core.console_handler import hide_console
from core.gui import JarvisGUI

# -------------------------------- Main setup ---------------------------------- #
hide_console()

# ---------------------------------- GUI init ---------------------------------- #
gui = JarvisGUI()
gui.add_log("Jarvis avviato", "SUCCESS")
speak("Buongiorno signore, sono a sua disposizione!")
gui.add_voice("Buongiorno signore, sono a sua disposizione!")

# -------------------------------- Loop vocale in thread separato ---------------- #
jarvis_active = False
activation_word = "jarvis"

def jarvis_loop():
    global jarvis_active
    while True:
        text = listen_with_vad()
        if not text:
            time.sleep(0.2)
            continue

        gui.add_voice(f"Riconosciuto: {text}")

        words = text.split()
        if not jarvis_active:
            # Verifica parola di attivazione
            if words and fuzz.ratio(words[0].lower(), activation_word) > JARVIS_ACTIVATION_PRECISION:
                jarvis_active = True
                command_after = text.replace(words[0], "", 1).strip()

                if command_after:
                    # Esegui subito il comando inline
                    jarvis_active = execute_command(command_after, jarvis_active, "command_inline")
                else:
                    speak("Sì, sono qui. Dimmi pure.")
                    gui.add_voice("Sì, sono qui. Dimmi pure.")
            continue  # non fare altro se Jarvis non è attivo

        # Se Jarvis è attivo, esegui i comandi
        jarvis_active = execute_command(text, jarvis_active, "command_query")

        time.sleep(0.2)

# Avvia il loop vocale in un thread separato
threading.Thread(target=jarvis_loop, daemon=True).start()

# -------------------------------- Avvio GUI sul main thread ------------------- #
# Tkinter mainloop deve essere sul thread principale
gui.run()
