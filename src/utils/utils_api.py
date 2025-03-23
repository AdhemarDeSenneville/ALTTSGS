import keyboard
import pyperclip
import pyautogui
import time
from tkinter import messagebox



def img_to_text():
    pass


def selection_to_text(from_play):
    """Copies selected text, processes it, and plays audio."""

    clipboard_content_befor = pyperclip.paste()
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.01)
    clipboard_content = pyperclip.paste()


    if clipboard_content_befor == clipboard_content and not from_play:
        print("Selection impossible to query.")
        messagebox.showwarning("Warning", "Selection impossible to query.")
        return None

    if not clipboard_content.strip():
        print("No text selected.")
        messagebox.showwarning("Warning", "No text selected for playback.")
        return None
    
    return clipboard_content