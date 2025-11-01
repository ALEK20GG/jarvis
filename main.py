import time
import ctypes
from rapidfuzz import fuzz

from core.speak import speak
from core.listen import listen_with_vad
from core.commands import execute_command
from core.config import JARVIS_ACTIVATION_PRECISION

hwnd = ctypes.windll.kernel32.GetConsoleWindow()

def hide_console(): ctypes.windll.user32.ShowWindow(hwnd, 0)
def show_console(): ctypes.windll.user32.ShowWindow(hwnd, 5)

hide_console()
speak("Buongiorno signore, sono a sua disposizione!")

jarvis_active = False

while True:
    text = listen_with_vad()
    if not jarvis_active and fuzz.ratio(text, "jarvis") > JARVIS_ACTIVATION_PRECISION:
        jarvis_active = True
        speak("Sì, sono qui. Dimmi pure.")
        continue
    if jarvis_active and text:
        jarvis_active = execute_command(text, jarvis_active)
    time.sleep(0.3)
