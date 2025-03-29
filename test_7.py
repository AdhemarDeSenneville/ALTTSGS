
import traceback

from src.gui.full import GUI
from src.utils.utils import load_config
print('TTSPlayer')
from src.models.tts.model import TTSPlayer
print('STTListener')
from src.models.stt.model import STTListener
print('DONE')

if __name__ == "__main__":

    CONFIG = load_config()
    tts_player = TTSPlayer(CONFIG)
    stt_listener = STTListener(CONFIG)
    
    try:
        gui = GUI(CONFIG, tts_player, stt_listener)
        gui.run()
    except Exception as e:
        print('EXCEPTION HAS BEEN TRIGGERED')
        print('EXEPTION IS',e)
        print(traceback.format_exc())
        traceback.print_exc()