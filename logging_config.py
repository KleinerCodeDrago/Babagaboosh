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
        "playing_async_audio": "Playing async audio"
        

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
        "playing_async_audio": "Spiele asynchrone Audio-Dateien ab"

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
        "audio_manager_initialized": "Audio-Programm ist bereit",
        "playing_audio_file": "Spiele diese Datei ab: {}",
        "audio_mixer_reinitialized": "Audio-Programm ist wieder bereit",
        "unknown_file_type": "Kann diese Datei nicht abspielen",
        "audio_file_deleted": "Datei gelöscht: {}",
        "audio_file_delete_failed": "Konnte Datei {} nicht löschen, weil sie gerade benutzt wird.",
        "playing_audio_async": "Spiele diese Datei ab, während andere Dinge laufen: {}",
        "test_audio_missing": "Test-Dateien fehlen",
        "sleeping_until_next_file": "Warte bis zur nächsten Datei",
        "playing_async_audio": "Spiele mehrere Dateien gleichzeitig ab"

    }
}

def log_string(key, value=None):
    log_str = LOG_STRINGS[config["LOG_LANGUAGE"]][key]
    if value:
        return log_str.format(value)
    else:
        return log_str

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
