import tkinter as tk
from tkinter import ttk


# Local Imports
from .main import MainTab
from .settings import SettingsTab


class GUI:


    COLOR_PALETTE = {
        "bg": "#fefefe",
        "button_bg": "#4a90e2",
        "button_hover": "#357ABD",
        "text": "#333333",
        "label": "#666666",
        "dropdown_bg": "#ffffff"
    }
    
    def __init__(self, config, tts_player, stt_listener):
        self.tts_player = tts_player
        self.stt_listener = stt_listener
        self.config = config
        self.root = tk.Tk()
        self.root.title("ALTTSGS")
        self.root.geometry("500x300")
        
        self.root.configure(bg=self.COLOR_PALETTE["bg"])

        self.build_ui()

    def build_ui(self):
        # Create Notebook (Tab System)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Add Player Tab
        self.player_tab = MainTab(self.notebook, self.config, self.tts_player, self.stt_listener)
        self.notebook.add(self.player_tab.frame, text="Player")

        # Add Settings Tab
        self.settings_tab = SettingsTab(self.notebook, self.config, self.tts_player, self.stt_listener)
        self.notebook.add(self.settings_tab.frame, text="Settings")

    def run(self):
        self.root.mainloop()