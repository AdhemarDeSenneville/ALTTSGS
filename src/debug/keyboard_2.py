import keyboard
import time

# Define your custom combination
required_keys = {'ctrl', '²', '&'}

# Track currently pressed keys
pressed_keys = set()

def on_key_event(event):
    if event.event_type == 'down':
        pressed_keys.add(event.name)
        # Debug print
        print(f"Pressed: {pressed_keys}")
        
        if required_keys.issubset(pressed_keys):
            print("🎯 Triggered: All 3 keys pressed!")
            # Your custom trigger goes here
            start_audio_thread()
    
    elif event.event_type == 'up':
        if event.name in pressed_keys:
            pressed_keys.remove(event.name)

def start_audio_thread():
    print("🟢 Starting audio playback thread...")

def stop_playback():
    print("🔴 Stopping audio playback...")


    # Hook all key events
keyboard.hook(on_key_event)

# Wait until ESC is pressed to exit
keyboard.wait('esc')
print("👋 Exiting.")