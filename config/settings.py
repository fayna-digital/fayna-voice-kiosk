"""Runtime configuration for the Fayna Kiosk voice assistant.

Every value can be overridden via an environment variable, so the same code runs
unchanged on a demo laptop and on a production kiosk device.
"""

from __future__ import annotations

import os
from pathlib import Path


def _env_bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
AUDIO_DIR = DATA_DIR / "audio"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"

KNOWLEDGE_FILE = DATA_DIR / "knowledge.json"
MENU_FILE = DATA_DIR / "menu.json"
QA_FILE = DATA_DIR / "qa.json"

# Speech-to-text
STT_ENGINE = os.getenv("KIOSK_STT_ENGINE", "google")
STT_LANGUAGE = os.getenv("KIOSK_STT_LANGUAGE", "pl-PL")

# Text-to-speech
TTS_VOICE = os.getenv("KIOSK_TTS_VOICE", "pl")
TTS_RATE = int(os.getenv("KIOSK_TTS_RATE", "190"))
TTS_VOLUME = float(os.getenv("KIOSK_TTS_VOLUME", "0.9"))
TTS_MAX_CHARS = 1000

# Natural language
UNKNOWN_RESPONSE = os.getenv(
    "KIOSK_UNKNOWN_RESPONSE",
    "Przepraszam, nie rozumiem. Proszę zapytać obsługę.",
)
MAX_QUERY_LENGTH = 500

# Privacy (RODO/GDPR): recording visitor audio or transcripts is OFF by default.
# Enable only with a lawful basis and clear on-site signage.
SAVE_AUDIO = _env_bool("KIOSK_SAVE_AUDIO", False)
SAVE_TRANSCRIPTS = _env_bool("KIOSK_SAVE_TRANSCRIPTS", False)

# Logging
LOG_LEVEL = os.getenv("KIOSK_LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(message)s"
LOG_FILE = LOGS_DIR / "kiosk.log"


def ensure_runtime_dirs() -> None:
    """Create the directories the app writes to (logs, plus caches when enabled)."""
    LOGS_DIR.mkdir(mode=0o750, parents=True, exist_ok=True)
    if SAVE_AUDIO:
        AUDIO_DIR.mkdir(mode=0o750, parents=True, exist_ok=True)
    if SAVE_TRANSCRIPTS:
        TRANSCRIPTS_DIR.mkdir(mode=0o750, parents=True, exist_ok=True)
