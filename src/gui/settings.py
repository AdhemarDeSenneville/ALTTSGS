import yaml

import tkinter as tk
from tkinter import ttk
import sounddevice as sd

class SettingsTab:

    # 🇺🇸 'a' => American English, 
    # 🇬🇧 'b' => British English
    # 🇯🇵 'j' => Japanese: pip install misaki[ja]
    # 🇨🇳 'z' => Mandarin Chinese: pip install misaki[zh]
    # 🇪🇸 'e' => Spanish es
    # 🇫🇷 'f' => French fr-fr
    # 🇮🇳 'h' => Hindi hi
    # 🇮🇹 'i' => Italian it
    # 🇧🇷 'p' => Brazilian Portuguese pt-br


    cfg = {
        'voices': ['af_heart', 'am_adam', 'ff_siwis'],
        'languages_name': ['English (US)', 'English (UK)', 'French', 'Spanish', 'Hindi', 'Japanese', 'Mandarin Chinese', 'Italian', 'Brazilian Portuguese'],
        'languages': ['a', 'b', 'f', 'e', 'h', 'j', 'z', 'i', 'p'],
    }


    def __init__(self, notebook, config, tts_player):
        self.tts_player = tts_player

        self.config = config
        self.config_settings = config['settings']
        self.frame = tk.Frame(notebook)
        self.get_audio_device()
        self.build_ui()
    
    def get_audio_device(self):
        self.devices = sd.query_devices()
        self.input_devices = [d['name'] for d in self.devices if d['max_input_channels'] > 0]
        self.output_devices = [d['name'] for d in self.devices if d['max_output_channels'] > 0]

    def build_ui(self):
        # Create a main frame with grid layout
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left column (Audio + Voice)
        left_col = ttk.Frame(main_frame)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        # Right column (Languages)
        right_col = ttk.Frame(main_frame)
        right_col.grid(row=0, column=1, sticky="nsew")

        # Make both columns expand equally
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Audio input dropdown
        ttk.Label(left_col, text="Audio Input Device").pack(anchor='w')
        self.input_device_combo = ttk.Combobox(left_col, values=self.input_devices, state="readonly")
        current_input = self.config_settings.get("audio_input", self.input_devices[0] if self.input_devices else "")
        self.input_device_combo.set(current_input)
        self.input_device_combo.bind("<<ComboboxSelected>>", self.on_input_device_change)
        self.input_device_combo.pack(fill="x", pady=4)

        # Audio output dropdown
        ttk.Label(left_col, text="Audio Output Device").pack(anchor='w')
        self.output_device_combo = ttk.Combobox(left_col, values=self.output_devices, state="readonly")
        current_output = self.config_settings.get("audio_output", self.output_devices[0] if self.output_devices else "")
        self.output_device_combo.set(current_output)
        self.output_device_combo.bind("<<ComboboxSelected>>", self.on_output_device_change)
        self.output_device_combo.pack(fill="x", pady=4)

        # Voice selection
        voice_frame = ttk.Frame(left_col)
        ttk.Label(voice_frame, text="Voice").pack(anchor="w")
        self.voice_dropdown = ttk.Combobox(voice_frame, values=self.cfg['voices'], state="readonly")
        self.voice_dropdown.set(self.config_settings.get("voice", self.cfg['voices'][0]))
        self.voice_dropdown.bind("<<ComboboxSelected>>", self.on_voice_change)
        self.voice_dropdown.pack(fill="x")
        voice_frame.pack(fill="x", pady=10)

        # Right column - Language 1 and 2 dropdowns
        language1_frame = ttk.Frame(right_col)
        ttk.Label(language1_frame, text="Language 1").pack(anchor="w")
        self.language1_dropdown = ttk.Combobox(language1_frame, values=self.cfg['languages_name'], state="readonly")
        self.language1_dropdown.current(self.cfg['languages'].index(self.config_settings.get("language1", self.cfg['languages'][0])))
        self.language1_dropdown.bind("<<ComboboxSelected>>", self.on_language_1_change)
        self.language1_dropdown.pack(fill="x")
        language1_frame.pack(fill="x", pady=10)

        language2_frame = ttk.Frame(right_col)
        ttk.Label(language2_frame, text="Language 2").pack(anchor="w")
        self.language2_dropdown = ttk.Combobox(language2_frame, values=self.cfg['languages_name'], state="readonly")
        self.language2_dropdown.current(self.cfg['languages'].index(self.config_settings.get("language2", self.cfg['languages'][0])))
        self.language2_dropdown.bind("<<ComboboxSelected>>", self.on_language_2_change)
        self.language2_dropdown.pack(fill="x")
        language2_frame.pack(fill="x", pady=10)

        # Save button at bottom right
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", pady=10, padx=10)
        ttk.Button(button_frame, text="Save", command=self.save).pack(side="right")
    
    def on_language_1_change(self, event):

        lang_name = self.language1_dropdown.get()
        print('Settings: language_1 - ',lang_name)
        index = self.cfg["languages_name"].index(lang_name)
        code = self.cfg["languages"][index]
        self.tts_player.change_lang_code(code)

    def on_language_2_change(self, event):
        print('Settings: language_2 - ',self.language2_dropdown.get())
        pass

    def on_voice_change(self, event):
        print('Settings: voice      - ',self.voice_dropdown.get())
        self.tts_player.change_voice(self.voice_dropdown.get())

    def on_input_device_change(self, event):
        selected_name = self.input_device_combo.get()
        index = self.input_devices.index(selected_name)
        print('Settings: audio_input -', selected_name, f"(index: {index})")
        self.config["audio_input_index"] = index  # Save index if needed

    def on_output_device_change(self, event):
        selected_name = self.output_device_combo.get()
        index = self.output_devices.index(selected_name)
        print('Settings: audio_output -', selected_name, f"(index: {index})")
        self.tts_player.change_output_device(index)

    def save(self):
        self.config['settings']["audio_input"] = self.input_device_combo.get()
        self.config['settings']["audio_output"] = self.output_device_combo.get()
        self.config['settings']["voice"] = self.voice_dropdown.get()
        
        lang_name_1 = self.language1_dropdown.get()
        lang_name_2 = self.language2_dropdown.get()

        index_1 = self.cfg["languages_name"].index(lang_name_1)
        index_2 = self.cfg["languages_name"].index(lang_name_2)

        self.config['settings']["language1"] = self.cfg["languages"][index_1]
        self.config['settings']["language2"] = self.cfg["languages"][index_2]

        with open("config_saved.yaml", "w") as f:
            yaml.dump(self.config, f)

        print("Settings updated:", self.config)