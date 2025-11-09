import webrtcvad
from core.functions.audio import alza_volume, abbassa_volume, muto
from core.functions.brightness import alza_luminosita, abbassa_luminosita
from core.functions.system import blocca_schermo, spegni_pc, riavvia_pc, disconnetti_utente
from core.functions.jarvis_processes import protocollo_blindness, protocollo_see_trough, protocollo_standby
from core.functions.basics import ora_attuale, saluti

# Precisione comandi
RESPONSE_PRECISION = 80
JARVIS_ACTIVATION_PRECISION = 70

# VAD config
VAD = webrtcvad.Vad(2)  # 0 = meno sensibile, 3 = più sensibile
RATE = 16000
FRAME_DURATION = 30  # ms
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)

# App paths
APP_PATHS = {
    "visual studio code": r"C:\Users\alezl\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": r"C:\Windows\System32\notepad.exe",
    "calcolatrice": r"C:\Windows\System32\calc.exe"
}

# Process aliases
PROCESS_ALIASES = {
    "microsoft store": "winstore.app.exe",
    "store": "winstore.app.exe",
    "chrome": "chrome.exe",
    "google": "chrome.exe",
    "edge": "msedge.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
}

COMMANDS = {
    "alza il volume": alza_volume,
    "abbassa il volume": abbassa_volume,
    "muto": muto,
    "alza la luminosità": alza_luminosita,
    "abbassa la luminosità": abbassa_luminosita,
    "blocca lo schermo": blocca_schermo,
    "spegni il pc": spegni_pc,
    "riavvia il pc": riavvia_pc,
    "disconnetti utente": disconnetti_utente,
    "protocollo standby": protocollo_standby,
    "protocollo see trough": protocollo_see_trough,
    "protocollo blindness": protocollo_blindness,
    "che ore sono": ora_attuale,
    "ciao": saluti
}