import json
import time
import azure.cognitiveservices.speech as speechsdk
import keyboard
import os
import logging
from logging_config import log_string

with open('config.json') as config_file:
    config = json.load(config_file)

class SpeechToTextManager:
    azure_speechconfig = None
    azure_audioconfig = None
    azure_speechrecognizer = None

    def __init__(self):
        # Creates an instance of a speech config with specified subscription key and service region.
        try:
            self.azure_speechconfig = speechsdk.SpeechConfig(
                subscription=config['AZURE_TTS_KEY'],
                region=config['AZURE_TTS_REGION']
            )
            self.azure_speechconfig.speech_recognition_language = config["AZURE_SPEECH_RECOGNITION_LANGUAGE"]
            print(log_string("azure_speech_initialized"))
        except TypeError:
            print(log_string("azure_speech_key_missing"))
            print(log_string("azure_speech_region_missing"))
            exit("Ooops! You forgot to set AZURE_TTS_KEY or AZURE_TTS_REGION in your environment!")

    def speechtotext_from_mic(self):
        self.azure_audioconfig = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig, audio_config=self.azure_audioconfig)
        print(log_string("speak_into_microphone"))
        speech_recognition_result = self.azure_speechrecognizer.recognize_once_async().get()
        text_result = speech_recognition_result.text
        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(log_string("azure_speech_recognition_result", speech_recognition_result.text))
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print(log_string("no_speech_recognized", speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print(log_string("azure_speech_recognition_canceled", cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(log_string("error_details", cancellation_details.error_details))
                print(log_string("check_speech_key_and_region"))
        print(log_string("got_text_result", text_result))
        return text_result

    def speechtotext_from_file(self, filename):
        self.azure_audioconfig = speechsdk.AudioConfig(filename=filename)
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig, audio_config=self.azure_audioconfig)
        print(log_string("listening_to_file"))
        speech_recognition_result = self.azure_speechrecognizer.recognize_once_async().get()
        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(log_string("azure_speech_recognition_result", speech_recognition_result.text))
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print(log_string("no_speech_recognized", speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print(log_string("azure_speech_recognition_canceled", cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(log_string("error_details", cancellation_details.error_details))
                print(log_string("check_speech_key_and_region"))
        return speech_recognition_result.text

    def speechtotext_from_file_continuous(self, filename):
        self.azure_audioconfig = speechsdk.audio.AudioConfig(filename=filename)
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig, audio_config=self.azure_audioconfig)
        done = False

        def stop_cb(evt):
            print(log_string("closing_on_event", evt))
            nonlocal done
            done = True

        self.azure_speechrecognizer.recognized.connect(lambda evt: print(log_string("recognized_event", evt)))
        self.azure_speechrecognizer.session_started.connect(lambda evt: print(log_string("session_started_event", evt)))
        self.azure_speechrecognizer.session_stopped.connect(lambda evt: print(log_string("session_stopped_event", evt)))
        self.azure_speechrecognizer.canceled.connect(lambda evt: print(log_string("canceled_event", evt)))

        self.azure_speechrecognizer.session_stopped.connect(stop_cb)
        self.azure_speechrecognizer.canceled.connect(stop_cb)

        all_results = []

        def handle_final_result(evt):
            all_results.append(evt.result.text)

        self.azure_speechrecognizer.recognized.connect(handle_final_result)

        print(log_string("processing_audio_file"))
        self.azure_speechrecognizer.start_continuous_recognition()

        while not done:
            time.sleep(.5)

        self.azure_speechrecognizer.stop_continuous_recognition()
        final_result = " ".join(all_results).strip()
        print(log_string("continuous_file_read_result", final_result))
        return final_result

    def speechtotext_from_mic_continuous(self, stop_key='p'):
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig)
        done = False

        def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            print(log_string("recognized_event", evt))

        self.azure_speechrecognizer.recognized.connect(recognized_cb)

        def stop_cb(evt: speechsdk.SessionEventArgs):
            print(log_string("closing_speech_recognition_on_event", evt))
            nonlocal done
            done = True

        self.azure_speechrecognizer.session_stopped.connect(stop_cb)
        self.azure_speechrecognizer.canceled.connect(stop_cb)

        all_results = []

        def handle_final_result(evt):
            all_results.append(evt.result.text)

        self.azure_speechrecognizer.recognized.connect(handle_final_result)

        result_future = self.azure_speechrecognizer.start_continuous_recognition_async()
        result_future.get()
        print(log_string("continuous_speech_recognition_running"))

        while not done:
            if keyboard.read_key() == stop_key:
                print(log_string("ending_azure_speech_recognition"))
                self.azure_speechrecognizer.stop_continuous_recognition_async()
                break

        final_result = " ".join(all_results).strip()
        print(log_string("continuous_speech_recognition_result", final_result))
        return final_result


# Tests
if __name__ == '__main__':
    TEST_FILE = config['TEST_FILE_AZURESPEECH']
    speechtotext_manager = SpeechToTextManager()
    while True:
        # speechtotext_manager.speechtotext_from_mic()
        # result = speechtotext_manager.speechtotext_from_file(TEST_FILE)
        # speechtotext_manager.speechtotext_from_file_continuous(TEST_FILE)
        result = speechtotext_manager.speechtotext_from_mic_continuous()
        print(log_string("final_result", result))
        time.sleep(60)
