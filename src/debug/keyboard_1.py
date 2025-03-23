import keyboard

print("🔍 Listening for keyboard events... (Press ESC to exit)")

def on_key_event(event):
    print(f"Key: {event.name} | Type: {event.event_type}")

# Hook all key events
keyboard.hook(on_key_event)

# Wait until ESC is pressed to exit
keyboard.wait('esc')
print("👋 Exiting.")