
import traceback

from src.gui.full import GUI
from src.utils.utils import load_config
from src.models.tts.model import TTSPlayer


if __name__ == "__main__":

    CONFIG = load_config()

    tts_player = TTSPlayer(CONFIG)

    try:
        gui = GUI(CONFIG, tts_player)
        gui.run()
    except Exception as e:
        print('EXCEPTION HAS BEEN TRIGGERED')
        print('EXEPTION IS',e)
        print(traceback.format_exc())
        traceback.print_exc()