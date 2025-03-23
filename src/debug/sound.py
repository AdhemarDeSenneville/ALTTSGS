import sounddevice as sd
import numpy as np
import traceback

# Settings
SAMPLE_RATE = 44100  # Standard audio sample rate
DURATION = 2  # seconds
FREQUENCY = 440  # Hz (A4 note)

def list_devices():
    print("\n=== Available Audio Devices ===")
    print(sd.query_devices())
    print("===============================")

def generate_sine_wave(frequency, duration, samplerate):
    t = np.linspace(0, duration, int(samplerate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return wave.astype(np.float32)

def play_audio():
    try:
        list_devices()

        print("\n[INFO] Generating sine wave...")
        audio = generate_sine_wave(FREQUENCY, DURATION, SAMPLE_RATE)

        print(f"[INFO] Playing audio on device 0 ({sd.query_devices(0)['name']})...")
        sd.play(audio, samplerate=SAMPLE_RATE, device=4)
        sd.wait()
        print("[INFO] Playback finished.")

    except Exception as e:
        print("[ERROR] Exception during audio playback:", e)
        traceback.print_exc()

if __name__ == "__main__":
    play_audio()
