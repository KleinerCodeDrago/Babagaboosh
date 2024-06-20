import time
import keyboard
from rich import print
from azure_speech_to_text import SpeechToTextManager
from openai_chat import OpenAiManager, num_tokens_from_messages
from eleven_labs import ElevenLabsManager
from obs_websockets import OBSWebsocketsManager
from audio_player import AudioManager
import json
import logging
import threading
from logging_config import log_string

# Load configurations
with open('config.json') as config_file:
    config = json.load(config_file)

ELEVENLABS_VOICE = config["ELEVENLABS_VOICE"]
FIRST_SYSTEM_MESSAGE = config["FIRST_SYSTEM_MESSAGE"]
CONTINUOUS_LISTENING = config["CONTINUOUS_LISTENING"]

BACKUP_FILE = "ChatHistoryBackup.txt"

logger = logging.getLogger(__name__)

elevenlabs_manager = ElevenLabsManager()
if config["WEBSOCKET_ENABLED"]:
    obswebsockets_manager = OBSWebsocketsManager()
speechtotext_manager = SpeechToTextManager()
openai_manager = OpenAiManager()
audio_manager = AudioManager()

chat_history = [FIRST_SYSTEM_MESSAGE]

new_speech_result_available = False

def speech_recognition_loop():
    global new_speech_result_available
    while True:
        mic_result = speechtotext_manager.speechtotext_from_mic_continuous(stop_on_silence=CONTINUOUS_LISTENING)
        if mic_result is not None:
            chat_history.append({"role": "user", "content": mic_result})
            new_speech_result_available = True

speech_recognition_thread = threading.Thread(target=speech_recognition_loop)
speech_recognition_thread.daemon = True
speech_recognition_thread.start()

print(log_string("loop_start"))
while True:
    if not CONTINUOUS_LISTENING:
        if keyboard.read_key() != "f4":
            time.sleep(0.1)
            continue
        print(log_string("f4_pressed"))

    if new_speech_result_available:
        new_speech_result_available = False
        if chat_history and isinstance(chat_history[-1]["content"], str) and chat_history[-1]["content"].strip():
            speechtotext_manager.is_speaking = True

            # Check total token limit. Remove old messages as needed
            print(log_string("chat_history_length", num_tokens_from_messages(chat_history)))
            while num_tokens_from_messages(chat_history) > 8000:
                if len(chat_history) > 2:
                    chat_history.pop(1)  # Remove the oldest user message
                    chat_history.pop(1)  # Remove the corresponding assistant message
                else:
                    break
                print(log_string("popped_message", num_tokens_from_messages(chat_history)))

            print(log_string("asking_chatgpt"))
            completion = openai_manager.client.chat.completions.create(
                model=config["AI_MODEL"],
                messages=chat_history
            )

            # Add this answer to our chat history
            chat_history.append({"role": completion.choices[0].message.role, "content": completion.choices[0].message.content})

            # Process the answer
            openai_answer = completion.choices[0].message.content
            print(log_string("chatgpt_response", openai_answer))

            with open(BACKUP_FILE, "w") as file:
                file.write(str(chat_history))

            elevenlabs_output = elevenlabs_manager.text_to_audio(openai_answer, ELEVENLABS_VOICE, False)

            if config["WEBSOCKET_ENABLED"]:
                obswebsockets_manager.set_source_visibility(config["SCENE_NAME"], config["SOURCE_NAME"], True)

            audio_manager.play_audio(elevenlabs_output, True, True, True)

            if config["WEBSOCKET_ENABLED"]:
                obswebsockets_manager.set_source_visibility(config["SCENE_NAME"], config["SOURCE_NAME"], False)

            print(log_string("dialogue_finished"))
            speechtotext_manager.is_speaking = False
