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
            logging.info(log_string("azure_speech_initialized"))
        except TypeError:
            logging.error(log_string("azure_speech_key_missing"))
            exit("Ooops! You forgot to set AZURE_TTS_KEY or AZURE_TTS_REGION in your environment!")

    def speechtotext_from_mic(self):
        self.azure_audioconfig = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig, audio_config=self.azure_audioconfig)
        logging.info("Speak into your microphone.")
        speech_recognition_result = self.azure_speechrecognizer.recognize_once_async().get()
        text_result = speech_recognition_result.text

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            logging.info(log_string("azure_speech_recognition_result", speech_recognition_result.text))
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            logging.warning("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            logging.error(log_string("azure_speech_recognition_canceled", cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                logging.error("Error details: {}".format(cancellation_details.error_details))
                logging.error("Did you set the speech resource key and region values?")
        logging.info(f"We got the following text: {text_result}")
        return text_result

    def speechtotext_from_file(self, filename):
        self.azure_audioconfig = speechsdk.AudioConfig(filename=filename)
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig, audio_config=self.azure_audioconfig)
        logging.info("Listening to the file \n")
        speech_recognition_result = self.azure_speechrecognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            logging.info(log_string("azure_speech_recognition_result", speech_recognition_result.text))
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            logging.warning("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            logging.error(log_string("azure_speech_recognition_canceled", cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                logging.error("Error details: {}".format(cancellation_details.error_details))
                logging.error("Did you set the speech resource key and region values?")
        return speech_recognition_result.text

    def speechtotext_from_file_continuous(self, filename):
        self.azure_audioconfig = speechsdk.audio.AudioConfig(filename=filename)
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig, audio_config=self.azure_audioconfig)
        done = False

        def stop_cb(evt):
            logging.info('CLOSING on {}'.format(evt))
            nonlocal done
            done = True

        # These are optional event callbacks that just print out when an event happens.
        self.azure_speechrecognizer.recognized.connect(lambda evt: logging.info('RECOGNIZED: {}'.format(evt)))
        self.azure_speechrecognizer.session_started.connect(lambda evt: logging.info('SESSION STARTED: {}'.format(evt)))
        self.azure_speechrecognizer.session_stopped.connect(lambda evt: logging.info('SESSION STOPPED {}'.format(evt)))
        self.azure_speechrecognizer.canceled.connect(lambda evt: logging.info('CANCELED {}'.format(evt)))

        # These functions will stop the program by flipping the "done" boolean when the session is either stopped or canceled
        self.azure_speechrecognizer.session_stopped.connect(stop_cb)
        self.azure_speechrecognizer.canceled.connect(stop_cb)

        # This is where we compile the results we receive from the ongoing "Recognized" events
        all_results = []

        def handle_final_result(evt):
            all_results.append(evt.result.text)

        self.azure_speechrecognizer.recognized.connect(handle_final_result)

        # Start processing the file
        logging.info("Now processing the audio file...")
        self.azure_speechrecognizer.start_continuous_recognition()

        # We wait until stop_cb() has been called above, because session either stopped or canceled
        while not done:
            time.sleep(.5)

        # Now that we're done, tell the recognizer to end session
        self.azure_speechrecognizer.stop_continuous_recognition()

        final_result = " ".join(all_results).strip()
        logging.info(f"\n\nHeres the result we got from continuous file read!\n\n{final_result}\n\n")
        return final_result

    def speechtotext_from_mic_continuous(self, stop_key='p'):
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig)
        done = False

        # Optional callback to print out whenever a chunk of speech is being recognized. This gets called basically every word.
        def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            logging.info('RECOGNIZED: {}'.format(evt))

        self.azure_speechrecognizer.recognized.connect(recognized_cb)

        # We register this to fire if we get a session_stopped or cancelled event.
        def stop_cb(evt: speechsdk.SessionEventArgs):
            logging.info('CLOSING speech recognition on {}'.format(evt))
            nonlocal done
            done = True

        # Connect callbacks to the events fired by the speech recognizer
        self.azure_speechrecognizer.session_stopped.connect(stop_cb)
        self.azure_speechrecognizer.canceled.connect(stop_cb)

        # This is where we compile the results we receive from the ongoing "Recognized" events
        all_results = []

        def handle_final_result(evt):
            all_results.append(evt.result.text)

        self.azure_speechrecognizer.recognized.connect(handle_final_result)

        # Perform recognition. `start_continuous_recognition_async asynchronously initiates continuous recognition operation,
        # Other tasks can be performed on this thread while recognition starts...
        # wait on result_future.get() to know when initialization is done.
        # Call stop_continuous_recognition_async() to stop recognition.
        result_future = self.azure_speechrecognizer.start_continuous_recognition_async()
        result_future.get()  # wait for voidfuture, so we know engine initialization is done.

        logging.info('Continuous Speech Recognition is now running, say something.')

        while not done:
            # METHOD 1 - Press the stop key. This is 'p' by default but user can provide different key
            if keyboard.read_key() == stop_key:
                logging.info("\nEnding azure speech recognition\n")
                self.azure_speechrecognizer.stop_continuous_recognition_async()
                break

        final_result = " ".join(all_results).strip()
        logging.info(f"\n\nHeres the result we got!\n\n{final_result}\n\n")
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
        logging.info(f"\n\nHERE IS THE RESULT:\n{result}")
        time.sleep(60)