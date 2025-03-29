import threading
import traceback
import logging

from RealtimeSTT import AudioToTextRecorder

def run_thread_safe(target, *args, **kwargs):
    def wrapper():
        try:
            target(*args, **kwargs)
        except Exception as e:
            print("Exception in thread:", e)
            print(traceback.print_exc())
    t = threading.Thread(target=wrapper, daemon=True)
    t.start()
    return t


class STTListener:
    def __init__(self, config):
        self.stt_cfg = config["STT"]
        self.callback_set_text = None

        self.stt_thread = None
        self.stop_event = threading.Event()

    def start(self):
        if self.stt_thread and self.stt_thread.is_alive():
            print("STT is already running.")
            return

        self.stop_event.clear()
        self.stt_thread = run_thread_safe(self._listen_loop)

    def _listen_loop(self):
        print("Listening... Say something!")
        
        self.recorder = AudioToTextRecorder(
            model=self.stt_cfg.get("model", "tiny"),
            language=self.stt_cfg.get("language", ""),
            compute_type=self.stt_cfg.get("compute_type", "default"),
            input_device_index=self.stt_cfg.get("input_device_index", None),
            gpu_device_index=self.stt_cfg.get("gpu_device_index", 0),
            device=self.stt_cfg.get("device", "cuda"),
            ensure_sentence_starting_uppercase=self.stt_cfg.get("ensure_sentence_starting_uppercase", True),
            ensure_sentence_ends_with_period=self.stt_cfg.get("ensure_sentence_ends_with_period", True),
            
            # You can expose and add these later if needed:
            use_microphone=True,
            level=logging.CRITICAL + 1  # Disable logging
            # spinner=False,
        )

        while not self.stop_event.is_set():
            text = self.recorder.text()
            print(text)

            self.callback_set_text(text)

    def stop(self):
        self.stop_event.set()
        self.recorder.shutdown()
        print("STT stopped.")

'''
    def change_input_device(self, index):
        self.recorder.input_device_index = index

    def change_language(self, language):
        self.recorder.language = language

    def change_gpu_device(self, index):
        self.recorder.gpu_device_index = index'''