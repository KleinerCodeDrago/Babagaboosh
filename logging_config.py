import logging
from config import config

LOG_STRINGS = {
    "en": {
        "openai_client_initialized": "OpenAI client initialized",
        "openai_api_key_missing": "OPENAI_API_KEY environment variable is missing",
        "no_input_received": "Didn't receive input!",
        "prompt_too_long": "The length of this chat question is too large for the GPT model",
        "asking_chatgpt": "Asking ChatGPT a question...",
        "chatgpt_response": "ChatGPT response: {}",
        "chat_history_length": "Chat History has a current token length of {}",
        "popped_message": "Popped a message! New token length is: {}",
        "audio_manager_initialized": "Audio manager initialized",
        "playing_audio_file": "Playing audio file: {}",
        "audio_mixer_reinitialized": "Audio mixer reinitialized",
        "unknown_file_type": "Cannot play audio, unknown file type",
        "audio_file_deleted": "Deleted the audio file: {}",
        "audio_file_delete_failed": "Couldn't remove {} because it is being used by another process.",
        "playing_audio_async": "Playing audio file asynchronously: {}",
        "test_audio_missing": "Missing test audio",
        "sleeping_until_next_file": "Sleeping until next file",
        "playing_async_audio": "Playing async audio",
        "azure_speech_key_missing": "AZURE_SPEECH_KEY environment variable is missing",
        "azure_speech_region_missing": "AZURE_SPEECH_REGION environment variable is missing",
        "azure_speech_initialized": "Azure Speech client initialized",
        "azure_speech_recognition_canceled": "Azure Speech recognition canceled. Error details: {}",
        "azure_speech_recognition_result": "Azure Speech recognition result: {}",
        "azure_speech_synthesis_error": "Azure Speech synthesis failed. Error details: {}",
        "azure_speech_synthesis_completed": "Azure Speech synthesis completed. Audio saved to: {}",
        "loop_start": "Starting main loop",
        "f4_pressed": "F4 key pressed, starting speech recognition",
        "dialogue_finished": "Dialogue finished",
        "speak_into_microphone": "Speak into your microphone.",
        "no_speech_recognized": "No speech could be recognized: {}",
        "check_speech_key_and_region": "Did you set the speech resource key and region values?",
        "got_text_result": "We got the following text: {}",
        "listening_to_file": "Listening to the file",
        "closing_on_event": "CLOSING on {}",
        "recognized_event": "RECOGNIZED: {}",
        "session_started_event": "SESSION STARTED: {}",
        "session_stopped_event": "SESSION STOPPED {}",
        "canceled_event": "CANCELED {}",
        "processing_audio_file": "Now processing the audio file...",
        "continuous_file_read_result": "Here's the result we got from continuous file read!\n\n{}\n\n",
        "closing_speech_recognition_on_event": "CLOSING speech recognition on {}",
        "continuous_speech_recognition_running": "Continuous Speech Recognition is now running, say something.",
        "ending_azure_speech_recognition": "\nEnding azure speech recognition\n",
        "continuous_speech_recognition_result": "Here's the result we got!\n\n{}\n\n",
        "final_result": "\n\nHERE IS THE RESULT:\n{}",
        "could_not_connect_obs": "\nPANIC!!\nCOULD NOT CONNECT TO OBS!\nDouble check that you have OBS open and that your websockets server is enabled in OBS.",
        "conected_to_obs": "Connected to OBS Websockets!\n"
 },
    "de": {
        "openai_client_initialized": "OpenAI-Client initialisiert",
        "openai_api_key_missing": "OPENAI_API_KEY Umgebungsvariable fehlt",
        "no_input_received": "Keine Eingabe erhalten!",
        "prompt_too_long": "Die Länge dieser Chat-Frage ist zu groß für das GPT-Modell",
        "asking_chatgpt": "Stelle ChatGPT eine Frage...",
        "chatgpt_response": "ChatGPT-Antwort: {}",
        "chat_history_length": "Der Chat-Verlauf hat eine aktuelle Token-Länge von {}",
        "popped_message": "Eine Nachricht entfernt! Neue Token-Länge ist: {}",
        "audio_manager_initialized": "Audio-Manager initialisiert",
        "playing_audio_file": "Spiele Audio-Datei ab: {}",
        "audio_mixer_reinitialized": "Audio-Mixer neu initialisiert",
        "unknown_file_type": "Kann Audio nicht abspielen, unbekannter Dateityp",
        "audio_file_deleted": "Audio-Datei gelöscht: {}",
        "audio_file_delete_failed": "Konnte {} nicht entfernen, da es von einem anderen Prozess verwendet wird.",
        "playing_audio_async": "Spiele Audio-Datei asynchron ab: {}",
        "test_audio_missing": "Test-Audio fehlt",
        "sleeping_until_next_file": "Warte bis zur nächsten Datei",
        "playing_async_audio": "Spiele asynchrone Audio-Dateien ab",
        "azure_speech_key_missing": "AZURE_SPEECH_KEY Umgebungsvariable fehlt",
        "azure_speech_region_missing": "AZURE_SPEECH_REGION Umgebungsvariable fehlt",
        "azure_speech_initialized": "Azure Speech-Client initialisiert",
        "azure_speech_recognition_canceled": "Azure Speech-Erkennung abgebrochen. Fehlerdetails: {}",
        "azure_speech_recognition_result": "Azure Speech-Erkennungsergebnis: {}",
        "azure_speech_synthesis_error": "Azure Speech-Synthese fehlgeschlagen. Fehlerdetails: {}",
        "azure_speech_synthesis_completed": "Azure Speech-Synthese abgeschlossen. Audio gespeichert unter: {}",
        "loop_start": "Hauptschleife gestartet",
        "f4_pressed": "F4-Taste gedrückt, Sprachaufnahme gestartet",
        "dialogue_finished": "Dialog beendet",
        "speak_into_microphone": "Sprechen Sie in Ihr Mikrofon.",
        "no_speech_recognized": "Es konnte keine Sprache erkannt werden: {}",
        "check_speech_key_and_region": "Haben Sie den Sprachressourcenschlüssel und die Regionswerte festgelegt?",
        "got_text_result": "Wir haben folgenden Text erhalten: {}",
        "listening_to_file": "Höre die Datei ab",
        "closing_on_event": "SCHLIESSE auf {}",
        "recognized_event": "ERKANNT: {}",
        "session_started_event": "SITZUNG GESTARTET: {}",
        "session_stopped_event": "SITZUNG GESTOPPT {}",
        "canceled_event": "ABGEBROCHEN {}",
        "processing_audio_file": "Verarbeite jetzt die Audiodatei...",
        "continuous_file_read_result": "Hier ist das Ergebnis, das wir vom kontinuierlichen Lesen der Datei erhalten haben!\n\n{}\n\n",
        "closing_speech_recognition_on_event": "SCHLIESSE Spracherkennung auf {}",
        "continuous_speech_recognition_running": "Kontinuierliche Spracherkennung läuft jetzt, sagen Sie etwas.",
        "ending_azure_speech_recognition": "\nBeende Azure-Spracherkennung\n",
        "continuous_speech_recognition_result": "Hier ist das Ergebnis, das wir erhalten haben!\n\n{}\n\n",
        "final_result": "\n\nHIER IST DAS ERGEBNIS:\n{}",
        "could_not_connect_obs": "\nPANIK!!!\nKEINE VERBINDUNG ZU OBS!\nÜberprüfen Sie, ob Sie OBS geöffnet haben und ob Ihr Websockets-Server in OBS aktiviert ist.",
        "conected_to_obs": "Verbunden mit OBS Websockets!\n"

    },
    "de_simple": {
        "openai_client_initialized": "AI-Programm ist bereit",
        "openai_api_key_missing": "AI-Login-Schlüssel fehlt",
        "no_input_received": "Keine Eingabe erhalten!",
        "prompt_too_long": "Die Frage ist zu lang für das Programm",
        "asking_chatgpt": "Programm sendet Nachricht an die AI...",
        "chatgpt_response": "Antwort von der AI: {}",
        "chat_history_length": "Der Chat-Verlauf hat eine Länge von {}",
        "popped_message": "Eine Nachricht entfernt! Neue Länge ist: {}",
        "audio_manager_initialized": "Ohren der AI sind wieder bereit aktiviert zu werden",
        "playing_audio_file": "Spiele diese Datei ab: {}",
        "audio_mixer_reinitialized": "Audio-Programm ist wieder bereit",
        "unknown_file_type": "Kann diese Datei nicht abspielen",
        "audio_file_deleted": "Datei gelöscht: {}",
        "audio_file_delete_failed": "Konnte Datei {} nicht löschen, weil sie gerade benutzt wird.",
        "playing_audio_async": "Spiele diese Datei ab, während andere Dinge laufen: {}",
        "test_audio_missing": "Test-Dateien fehlen",
        "sleeping_until_next_file": "Warte bis zur nächsten Datei",
        "playing_async_audio": "Spiele mehrere Dateien gleichzeitig ab",
        "azure_speech_key_missing": "Azure Sprach-Schlüssel fehlt",
        "azure_speech_region_missing": "Azure Sprach-Region fehlt",
        "azure_speech_initialized": "Azure Sprach-Programm ist bereit",
        "azure_speech_recognition_canceled": "Azure Sprach-Erkennung abgebrochen. Fehler: {}",
        "azure_speech_recognition_result": "Azure Sprach-Erkennung Ergebnis: {}",
        "azure_speech_synthesis_error": "Azure Sprach-Ausgabe Fehler: {}",
        "azure_speech_synthesis_completed": "Azure Sprach-Ausgabe fertig. Datei gespeichert: {}",
        "loop_start": "Hauptschleife gestartet",
        "f4_pressed": "F4-Taste gedrückt, Sprachaufnahme gestartet",
        "dialogue_finished": "Dialog beendet",
        "speak_into_microphone": "Sprich ins Mikrofon.",
        "no_speech_recognized": "Konnte keine Sprache erkennen: {}",
        "check_speech_key_and_region": "Hast du den Sprach-Schlüssel und die Region eingestellt?",
        "got_text_result": "Das habe ich verstanden: {}",
        "listening_to_file": "Ich höre mir die Datei an",
        "closing_on_event": "BEENDE wegen {}",
        "recognized_event": "ERKANNT: {}",
        "session_started_event": "AUFNAHME GESTARTET: {}",
        "session_stopped_event": "AUFNAHME GESTOPPT {}",
        "canceled_event": "ABGEBROCHEN {}",
        "processing_audio_file": "Verarbeite jetzt die Audio-Datei...",
        "continuous_file_read_result": "Das ist das Ergebnis vom Lesen der ganzen Datei!\n\n{}\n\n",
        "closing_speech_recognition_on_event": "BEENDE Spracherkennung wegen {}",
        "continuous_speech_recognition_running": "Dauernde Spracherkennung läuft jetzt, sag was.",
        "ending_azure_speech_recognition": "\nBeende Azure Spracherkennung\n",
        "continuous_speech_recognition_result": "Das ist das Ergebnis!\n\n{}\n\n",
        "final_result": "\n\nHIER IST DAS ERGEBNIS:\n{}",
        "could_not_connect_obs": "\nPANIK!!!\nKEINE VERBINDUNG ZU OBS!\nÜberprüfen Sie, ob Sie OBS geöffnet haben und ob Ihr Websockets-Server in OBS aktiviert ist.",
        "conected_to_obs": "Keine Verbindung zu OBS!\n"
    }
}


def log_string(key, value=None):
    log_str = LOG_STRINGS[config["LOG_LANGUAGE"]][key]
    if value:
        return log_str.format(value)
    else:
        return log_str