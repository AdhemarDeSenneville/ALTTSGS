from RealtimeSTT import AudioToTextRecorder

def process_text(text):
    print(text)

if __name__ == '__main__':
    print("Wait until it says 'speak now'")
    recorder = AudioToTextRecorder(
        model = 'tiny',
        language = "",
        compute_type = "default",
        input_device_index = None,
        gpu_device_index = 0,
        device = "cuda",
        #on_recording_start=None,
        #on_recording_stop=None,
        #on_transcription_start=None,
        ensure_sentence_starting_uppercase=True,
        ensure_sentence_ends_with_period=True,
        #use_microphone=True,
        #spinner=True,
        #level=logging.WARNING,
    )

    while True:
        recorder.text(process_text)