import pyautogui
import time
from core.speak import speak
from core.utils.logger import log

def alza_volume():
    for _ in range(5):
        pyautogui.press("volumeup")
    speak("Volume alzato di 5%")
    log("Volume alzato di 5%", "INFO")

def abbassa_volume():
    for _ in range(5):
        pyautogui.press("volumedown")
    speak("Volume abbassato di 5%")
    log("Volume abbassato di 5%", "INFO")

def muto():
    speak("Volume muto attivato")
    log("Volume muto attivato", "INFO")
    time.sleep(1.5)
    pyautogui.press("volumemute")

