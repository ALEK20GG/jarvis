import webrtcvad

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
    "notepad": r"C:\Windows\System32\notepad.exe",
    "calcolatrice": r"C:\Windows\System32\calc.exe"
}

# Process aliases
PROCESS_ALIASES = {
    "microsoft store": "winstore.app.exe",
    "store": "winstore.app.exe",
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
}
