import time
import keyboard
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager
from eleven_labs import ElevenLabsManager
from obs_websockets import OBSWebsocketsManager
from audio_player import AudioManager
import json
import logging
from logging_config import log_string

# Load configurations
with open('config.json') as config_file:
    config = json.load(config_file)

ELEVENLABS_VOICE = config["ELEVENLABS_VOICE"]
FIRST_SYSTEM_MESSAGE = config["FIRST_SYSTEM_MESSAGE"]

BACKUP_FILE = "ChatHistoryBackup.txt"

logger = logging.getLogger(__name__)

elevenlabs_manager = ElevenLabsManager()
if config["WEBSOCKET_ENABLED"]:
    obswebsockets_manager = OBSWebsocketsManager()
speechtotext_manager = SpeechToTextManager()
openai_manager = OpenAiManager()
audio_manager = AudioManager()

openai_manager.chat_history.append(FIRST_SYSTEM_MESSAGE)

print(log_string("loop_start"))
while True:
    # Wait until user presses "f4" key
    if keyboard.read_key() != "f4":
        time.sleep(0.1)
        continue

    print(log_string("f4_pressed"))

    # Get question from mic
    mic_result = speechtotext_manager.speechtotext_from_mic_continuous()
    
    # Send question to OpenAi
    openai_result = openai_manager.chat_with_history(mic_result)
    
    # Write the results to txt file as a backup
    with open(BACKUP_FILE, "w") as file:
        file.write(str(openai_manager.chat_history))

    # Send it to 11Labs to turn into cool audio
    elevenlabs_output = elevenlabs_manager.text_to_audio(openai_result, ELEVENLABS_VOICE, False)

    if config["WEBSOCKET_ENABLED"]:
        obswebsockets_manager.set_source_visibility(config["SCENE_NAME"], config["SOURCE_NAME"], True)

    # Play the mp3 file
    audio_manager.play_audio(elevenlabs_output, True, True, True)

    if config["WEBSOCKET_ENABLED"]:
        # Disable Pajama Sam pic in OBS
        obswebsockets_manager.set_source_visibility(config["SCENE_NAME"], config["SOURCE_NAME"], False)

    print(log_string("dialogue_finished"))
