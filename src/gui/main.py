import keyboard
import tkinter as tk
from tkinter import ttk


config_parametres = {
    
}


class MainTab:

    COLOR_PALETTE = {
        "bg": "#ffffff",# "#fefefe",
        "button_bg": "#4a90e2",
        "button_hover": "#357ABD",
        "text": "#333333",
        "label": "#666666",
        "dropdown_bg": "#ffffff"
    }


    cfg = {
        'speed': [0.5, 0.75, 1, 1.5, 2],
        'languages_name': ['English (US)', 'English (UK)', 'French', 'Spanish', 'Hindi', 'Japanese', 'Mandarin Chinese', 'Italian', 'Brazilian Portuguese'],
        'languages': ['a', 'b', 'f', 'e', 'h', 'j', 'z', 'i', 'p'],
    }

    def __init__(self, notebook, config, tts_player, stt_listener):
        self.tts_player = tts_player
        self.stt_listener = stt_listener

        self.frame = tk.Frame(notebook)

        self.os = config['os']

        self.text_area = None
        self.stt_recording = False
        self.text_zone_mode = tk.IntVar(value=1)
        self.setup_callbacks()
        self.setup_styles()
        self.build_ui()
        self.bind_hotkeys()
    
    # GUI

    def setup_styles(self):
        style = ttk.Style() #self.root
        style.theme_use("clam")  # Use a minimal theme

        # Button style
        style.configure("Modern.TButton",
                        font=("Segoe UI", 11),
                        padding=10,
                        relief="flat",
                        background=self.COLOR_PALETTE["button_bg"],
                        foreground="white",
                        borderwidth=0,
                        focuscolor="")
        style.map("Modern.TButton",
                  background=[("active", self.COLOR_PALETTE["button_hover"])],
                  relief=[("pressed", "flat"), ("!pressed", "flat")])
        
        # Recording button style
        style.configure("Recording.TButton",
                font=("Segoe UI", 11),
                padding=10,
                relief="flat",
                background="green",
                foreground="white",
                borderwidth=0,
                focuscolor="")
        style.map("Recording.TButton",
          background=[("active", "#228B22")],  # hover = darker green
          relief=[("pressed", "flat"), ("!pressed", "flat")])
        
        # Label style
        style.configure("TLabel",
                        font=("Segoe UI", 10),
                        background=self.COLOR_PALETTE["bg"],
                        foreground=self.COLOR_PALETTE["label"])

        # Dropdowns
        style.configure("TCombobox",
                        font=("Segoe UI", 7),
                        padding=2)


    def build_ui(self):
        # Main container
        main_frame = ttk.Frame(self.frame, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Upper section (buttons & toggles)
        upper_frame = ttk.Frame(main_frame)
        upper_frame.pack(fill="x")

        left_frame = ttk.Frame(upper_frame)
        right_frame = ttk.Frame(upper_frame)

        left_frame.pack(side="left", fill="y", padx=(0, 20))
        right_frame.pack(side="right", fill="y")

        # Frame for top row buttons (▶ ⏸ ⏹)
        top_left_frame = ttk.Frame(left_frame)
        top_left_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(
            top_left_frame, 
            text="▶", 
            command=lambda: self.tts_player.start_audio_thread(from_play=True),
            style="Modern.TButton"
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        ttk.Button(
            top_left_frame, 
            text="⏸", 
            command=self.tts_player.toggle_pause,
            style="Modern.TButton"
        ).pack(side="left", expand=True, fill="x", padx=4)

        ttk.Button(
            top_left_frame,
            text="⏹", 
            command=self.tts_player.stop_playback,
            style="Modern.TButton"
        ).pack(side="left", expand=True, fill="x", padx=(4, 0))
        
         # Frame for bottom row buttons (recording + spell check)
        bottom_left_frame = ttk.Frame(left_frame)
        bottom_left_frame.pack(fill="x", pady=(10, 0))

        self.record_btn = ttk.Button(
            bottom_left_frame,
            text="🎙",
            style="Modern.TButton",
            command=self.toggle_recording
        )
        self.record_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        ttk.Button(
            bottom_left_frame,
            text="✔",
            style="Modern.TButton",
            command=self.correct_spelling
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Toggle selection menus on the right
        ttk.Label(right_frame, text="Speed").pack(anchor="w")
        self.speed_dropdown = ttk.Combobox(right_frame, values=self.cfg["speed"], state="readonly")
        self.speed_dropdown.current(2)
        self.speed_dropdown.bind("<<ComboboxSelected>>", lambda e: self.tts_player.change_speed(float(self.speed_dropdown.get())))
        self.speed_dropdown.pack(fill="x", pady=4)


        ttk.Label(right_frame, text="Language").pack(anchor="w")
        self.language_dropdown = ttk.Combobox(right_frame, values=self.cfg["languages_name"], state="readonly")
        self.language_dropdown.current(0)
        self.language_dropdown.bind("<<ComboboxSelected>>", lambda e: self.tts_player.change_lang_code(self.cfg["languages"][self.language_dropdown.current()]))
        self.language_dropdown.pack(fill="x", pady=4)

        self.text_zone_toggle = self.text_zone_toggle = tk.Checkbutton(
            right_frame,
            text="Toggle",
            variable=self.text_zone_mode,
            onvalue=1,
            offvalue=0,
            command=self.toggle_text_zone_highlight
        )
        self.text_zone_toggle.pack(pady=4)

        # Lower text display section
        self.text_area = tk.Text(main_frame, height=5, font=("Segoe UI", 10), wrap="word", bd=1, relief="solid")
        self.text_area.pack(fill="both", expand=True, pady=(20, 0))

    # Logique

    def toggle_recording(self):
        print(self.stt_recording)
        if self.stt_recording:
            self.stt_listener.stop()
            self.stt_recording = False
            self.record_btn.config(text="🎙", style="Modern.TButton")
            print("STT stopped.")
        else:
            self.stt_listener.start()
            self.stt_recording = True
            self.record_btn.config(text="🎙", style="Recording.TButton")
            print("STT started.")

    def toggle_text_zone_highlight(self):
        if self.text_zone_mode.get() == 0:
            self.text_area.config(bg="lightyellow")
        else:
            self.text_area.config(bg="white")


    def correct_spelling(self):
        pass
    

    def setup_callbacks(self):

        self.tts_player.callback_set_text = self.process_text_player
        self.stt_listener.callback_set_text = self.process_text_listener
    
    def process_text_listener(self, content: str):
        # TODO insert .' ' if point before
        self.text_area.insert(tk.END, content + ' ')

    def process_text_player(self, content: str):
        """Set the text in the text area."""
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, content)


    def get_text(self) -> str:
        """Get the current text from the text area."""
        return self.text_area.get("1.0", tk.END).strip()


    def bind_hotkeys(self):
        if self.os == 'Linux':
            pass
            #keyboard.add_hotkey("ctrl+b", self.tts_player.start_audio_thread, suppress=True)
            #keyboard.add_hotkey("alt gr+b", self.tts_player.stop_playback, suppress=True)
        elif self.os == 'Windows':
            keyboard.add_hotkey("ctrl+²+&", self.tts_player.start_audio_thread, suppress=True)
            keyboard.add_hotkey("ctrl+²+é", self.tts_player.stop_playback, suppress=True)
        else:
            raise NotImplementedError
