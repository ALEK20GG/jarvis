from datetime import datetime

def log(message, level="INFO"):
    colors = {
        "INFO": "\033[94m",     # blu
        "WARNING": "\033[93m",  # giallo
        "ERROR": "\033[91m",    # rosso
        "SUCCESS": "\033[92m",  # verde
    }
    reset = "\033[0m"
    color = colors.get(level, "\033[0m")
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] [{level}] {message}{reset}")
