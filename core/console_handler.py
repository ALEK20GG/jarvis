import ctypes

# Handle console
hwnd = ctypes.windll.kernel32.GetConsoleWindow()

def hide_console():
    ctypes.windll.user32.ShowWindow(hwnd, 0)  # 0 = nascondi console

def show_console():
    ctypes.windll.user32.ShowWindow(hwnd, 5)  # 5 = mostra console
