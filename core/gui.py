import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class JarvisGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jarvis")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)  # sempre in primo piano

        # Frame per i log
        log_frame = tk.LabelFrame(self.root, text="Logger")
        log_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.log_box = ScrolledText(log_frame, height=10, state='disabled', bg="#1e1e1e", fg="white")
        self.log_box.pack(fill="both", expand=True)

        # Frame per comandi vocali e speak
        voice_frame = tk.LabelFrame(self.root, text="Riconoscimento & Speak")
        voice_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.voice_box = ScrolledText(voice_frame, height=5, state='disabled', bg="#222222", fg="lightgreen")
        self.voice_box.pack(fill="both", expand=True)

    def add_voice(self, text):
        if self.root.winfo_exists():
            # usa after per eseguire la funzione sul main thread
            self.root.after(0, lambda: self._add_voice_internal(text))

    def _add_voice_internal(self, text):
        if not self.voice_box.winfo_exists():
            return
        self.voice_box.config(state='normal')
        self.voice_box.insert('end', f"{text}\n")
        self.voice_box.see('end')
        self.voice_box.config(state='disabled')

    def add_log(self, message, type="INFO"):
        if self.root.winfo_exists():
            self.root.after(0, lambda: self._add_log_internal(message, type))

    def _add_log_internal(self, message, type):
        if not self.log_box.winfo_exists():
            return
        self.log_box.config(state='normal')
        self.log_box.insert('end', f"[{type}] {message}\n")
        self.log_box.see('end')
        self.log_box.config(state='disabled')

    def run(self):
        self.root.mainloop()
