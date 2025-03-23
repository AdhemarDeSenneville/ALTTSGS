import threading
import traceback
import queue

from transformers import pipeline


def run_thread_safe(target, *args, **kwargs):
    def wrapper():
        try:
            target(*args, **kwargs)
        except Exception as e:
            print("Exception in thread:", e)
            print(traceback.print_exc())

    threading.Thread(target=wrapper, daemon=True).start()


class SpellFixer:
    def __init__(self, config):
        self.model_path = config["speller"]["model_path"]
        self.device = config["speller"].get("device", -1)
        self.max_length = config["speller"].get("max_length", 256)

        self.stop_processing = threading.Event()
        self.processing_thread = None
        self.text_queue = queue.Queue()

        self.callback_set_text = None

        self.init_pipeline()

    def init_pipeline(self):
        print(f"Loading spell correction model from: {self.model_path}")
        self.pipeline = pipeline(
            "text2text-generation",
            model=self.model_path,
            device=self.device
        )

    def fix_text(self, text):
        prompt = "fix:" + text
        result = self.pipeline(prompt, max_length=self.max_length)
        return result[0]['generated_text']

    def start_processing(self):
        self.processing_thread = run_thread_safe(self.fix_text)


    def change_max_length(self, new_max):
        self.max_length = new_max

    def change_device(self, new_device):
        self.device = new_device
        self.init_pipeline()