import keyboard
import pyperclip
import pyautogui
import time
import threading
import tkinter as tk
from tkinter import messagebox

# Audio Imports
from kokoro import KPipeline
import sounddevice as sd

# Utility Imports
from utils import split_text

CONFIG = {
    "splitter": {
        'min_length': 10,
        'max_length': 500,
        'split_pattern': '.',
    },
    "audio": {
        "device": 0,
        "samplerate": 24000,
    },
    "tts": {
        "speed": 1.3,
        "voice": 'af_heart',
        "device": 'cuda:0',
        "lang_code": 'a',
    },
}

pipeline = KPipeline(
    lang_code=CONFIG['tts']["lang_code"],
    device=CONFIG['tts']["device"],
)

# Flag to control audio playback
stop_audio = threading.Event()
paused = threading.Event()

def stop_playback():
    """Stops the currently playing audio."""
    stop_audio.set()
    sd.stop()
    print("Audio playback stopped.")

def toggle_pause():
    """Pauses or resumes playback."""
    if paused.is_set():
        paused.clear()  # Resume
        print("Resumed playback.")
    else:
        paused.set()  # Pause
        print("Paused playback.")


def copy_and_play():
    """Copies selected text, processes it, and plays audio."""
    global stop_audio
    stop_audio.clear()

    print("Playing copied text...")

    
    clipboard_content_before = pyperclip.paste()

    
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.01)
    
    clipboard_content = pyperclip.paste()


    if clipboard_content_before == clipboard_content:
        print("Selection impossible to query.")
        messagebox.showwarning("Warning", "Selection impossible to query.")
        return None

    if not clipboard_content.strip():
        print("No text selected.")
        messagebox.showwarning("Warning", "No text selected for playback.")
        return None
    
    text_splitted = split_text(clipboard_content, **CONFIG["splitter"])
    
    generator = pipeline(
        text_splitted, voice=CONFIG['tts']["voice"],
        speed=CONFIG['tts']["speed"], split_pattern=r'\n+'
    )
    
    for i, (gs, ps, audio) in enumerate(generator):
        if stop_audio.is_set():
            print("Playback stopped before finishing.")
            break 
        
        print(i, gs)
        sd.play(audio, samplerate=CONFIG["audio"]['samplerate'])

        while sd.get_stream().active:
            if stop_audio.is_set():
                sd.stop()
                print("Playback interrupted.")
                return
            
            while paused.is_set():
                time.sleep(0.1)
            time.sleep(0.05)
    
    print("Playback finished.")

def start_audio_thread():
    """Starts the audio playback in a separate thread to keep the UI responsive."""
    threading.Thread(target=copy_and_play, daemon=True).start()

if __name__ == "__main__":
    # GUI Setup
    root = tk.Tk()
    root.title("TTS Player")
    root.geometry("300x200")

    # Buttons
    play_button = tk.Button(root, text="Play", command=start_audio_thread, width=10, height=2)
    play_button.pack(pady=5)

    pause_button = tk.Button(root, text="Pause", command=toggle_pause, width=10, height=2)
    pause_button.pack(pady=5)

    stop_button = tk.Button(root, text="Stop", command=stop_playback, width=10, height=2)
    stop_button.pack(pady=5)

    # Keyboard Shortcuts (Global)
    keyboard.add_hotkey("ctrl+b", start_audio_thread, suppress=True)  # Play
    keyboard.add_hotkey("alt gr+b", stop_playback, suppress=True)  # Stop

    # Status Labels
    status_label = tk.Label(root, text="Press Ctrl+B to Play | Alt+B to Stop", fg="blue")
    status_label.pack(pady=5)

    print("Press Ctrl+B to copy selected text and play audio.")
    print("Press Alt+B to stop audio playback.")

    # Run GUI
    root.mainloop()
