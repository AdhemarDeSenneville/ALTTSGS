import numpy as np
import pyaudio
from src.githubs.whisper_streaming.whisper_online import *

# Audio configuration parameters
RATE = 16000       # Sampling rate in Hz
CHUNK = 1024       # Number of samples per audio chunk

# Initialize PyAudio and open a stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def capture_audio_chunk():
    """
    Capture a single audio chunk from the microphone, convert it to a numpy array 
    of floats in the range [-1, 1], and return it.
    """
    data = stream.read(CHUNK, exception_on_overflow=False)
    audio_chunk = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
    return audio_chunk

# Setup source and target language.
src_lan = "en"  # source language
tgt_lan = "en"  # target language (same as source for ASR)

# Initialize the Whisper ASR model.
asr = FasterWhisperASR(src_lan, "large-v2")
# Optional: Enable translation or voice activity detection (VAD)
# asr.set_translate_task()  
# asr.use_vad()  

# Create the online processor for streaming transcription.
online = OnlineASRProcessor(asr)

print("Listening... Press Ctrl+C to stop.")

try:
    while True:
        # Capture the next audio chunk from the microphone.
        audio_chunk = capture_audio_chunk()
        
        # Insert the chunk into the online processor.
        online.insert_audio_chunk(audio_chunk)
        
        # Process the audio to get a partial transcription.
        partial_output = online.process_iter()
        if partial_output:
            print("Partial transcription:", partial_output)
            
except KeyboardInterrupt:
    print("Ending transcription...")

# Finalize to process any remaining audio.
final_output = online.finish()
print("Final transcription:", final_output)

# Cleanup the audio stream and PyAudio instance.
stream.stop_stream()
stream.close()
p.terminate()

# Reset the online processor if you want to reuse it later.
online.init()