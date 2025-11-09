import pyautogui
import screen_brightness_control as sbc
from core.utils.logger import log
from core.speak import speak


def alza_luminosita():
    current = sbc.get_brightness()
    sbc.set_brightness(min(100, current[0] + 5))  # aumenta del 5%
    speak("Luminosità aumentata di 5%")
    log("Luminosità aumentata di 5%", "INFO")

def abbassa_luminosita():
    current = sbc.get_brightness()
    sbc.set_brightness(max(0, current[0] - 5))  # diminuisce del 5%
    speak("Luminosità diminuita di 5%")
    log("Luminosità diminuita di 5%", "INFO")