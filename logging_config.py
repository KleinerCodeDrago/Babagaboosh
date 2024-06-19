import logging
from config import config

LOG_STRINGS = {
    "en": {
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

def log_string(key, language):
    return LOG_STRINGS[language][key]

def log_string(key):
    return LOG_STRINGS[config["LOG_LANGUAGE"]][key]

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
