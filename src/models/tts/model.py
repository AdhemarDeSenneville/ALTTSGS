
import time
import threading
import traceback
import queue
import torch

from kokoro import KPipeline, KModel
import sounddevice as sd


from .utils_text import split_text
from src.utils.utils_api import selection_to_text

def run_thread_safe(target, *args, **kwargs):
    def wrapper():
        try:
            target(*args, **kwargs)
        except Exception as e:
            print("Exception in thread:", e)
            print(traceback.print_exc())

    threading.Thread(target=wrapper, daemon=True).start()

class TTSPlayer:

    def __init__(self,config):
        
        # Extract from config
        self.config_splitter = config["splitter"]
        self.lang_code = config['tts']["lang_code"]
        self.device = config['tts']["device"]
        self.voice = config['tts']["voice"]
        self.speed = config['tts']["speed"]
        self.sample_rate = config["audio"]['samplerate']

        self.voice_tensor = torch.load(f'src/assets/voices/{self.voice}.pt', weights_only=True)

        self.output_device = 4
        
        # Init Events
        self.stop_audio = threading.Event()
        self.paused = threading.Event()

        self.callback_set_text = None

        # Set Pipeline
        self.init_pipeline()

        self.generate_worker = None
        self.audio_thread = None
        self.audio_queue = queue.Queue()
    
    def _stop_previous_threads(self):
        # Signal old threads to stop
        self.stop_audio.set()

        # Wait on generate_worker
        if self.generate_worker and self.generate_worker.is_alive():
            self.generate_worker.join()

        # If you also keep a reference to the playback thread, join it too
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join()

        # Clear any leftover audio in the queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                pass

        # Reset the stop event, so we can reuse it
        self.stop_audio.clear()
    
    def stop_playback(self):
        self._stop_previous_threads()
        sd.stop()
        print("Audio playback stopped.")

    def toggle_pause(self):
        if self.paused.is_set():
            self.paused.clear()
            print("Resumed playback.")
        else:
            self.paused.set()
            print("Paused playback.")


    def generate_audio(self, text_splitted):
        """
        Worker thread that generates audio and pushes it into a queue.
        """
        generator = self.pipeline(
            text_splitted, voice=self.voice_tensor,
            speed=self.speed, split_pattern=r'\n+'
        )
        for i, (gs, ps, audio) in enumerate(generator):
            if self.stop_audio.is_set():
                break

            print('GENERATED :',i,gs)
            self.audio_queue.put((i, gs, audio))
        
        # signal we're done generating.
        self.audio_queue.put(None)


    def play(self, from_play = False):
        print("Start Playing")

        text = selection_to_text(from_play)
        print('Text :',text)

        text_splitted = split_text(text, **self.config_splitter)
        print('Splitted :',text)

        # Start a background thread to generate audio
        self.generate_worker = threading.Thread(target=self.generate_audio, args=(text_splitted,))
        self.generate_worker.start()

        # Continuously pull chunks from the queue and play them
        for item in iter(lambda: self.audio_queue.get(), None):
            if self.stop_audio.is_set():
                print("Playback stopped before finishing.")
                break

            i, gs, audio = item
            print('PLAYING   :',i, gs)

            # Play the current audio chunk
            self.callback_set_text(gs)
            sd.play(audio, samplerate=self.sample_rate) # TODO , device=self.output_device

            # Wait until this chunk finishes playing (or is stopped/paused)
            while sd.get_stream().active:
                # Check if user stopped
                if self.stop_audio.is_set():
                    sd.stop()
                    print("Playback interrupted.")
                    break

                # Handle pausing
                while self.paused.is_set():
                    time.sleep(0.1)

                time.sleep(0.05)

        self.generate_worker.join()
        print("Playback finished.")


    def start_audio_thread(self, from_play=True):
        self._stop_previous_threads()
        
        self.stop_audio.clear()
        if self.paused.is_set():
            self.paused.clear()
        
        self.audio_thread = run_thread_safe(lambda: self.play(from_play=from_play))
    

    # Else
    def change_lang_code(self, lang_code):
        self.lang_code = lang_code
        self.init_pipeline()


    def change_speed(self, speed):
        self.speed = speed


    def change_voice(self, voice):
        self.voice = voice
        self.voice_tensor = torch.load(f'src/assets/voices/{voice}.pt', weights_only=True)


    def change_output_device(self, output_device):
        self.output_device = output_device


    def init_pipeline(self):

        model = KModel(config = 'src/assets/weights/tts/config.json', model = 'src/assets/weights/tts/kokoro-v1_0.pth')

        self.pipeline = KPipeline(
            lang_code=self.lang_code,
            device=self.device,
            model = model
        )