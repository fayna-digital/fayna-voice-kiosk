"""Fayna Kiosk — application entry point.

Run from the repository root:  python -m src.main
"""

from __future__ import annotations

import logging
import sys

from config import settings
from src.nlp.processor import NLPProcessor
from src.stt.engine import STTEngine
from src.tts.engine import TTSEngine

logger = logging.getLogger(__name__)

_STOP_WORDS = {"wyjście", "stop", "exit"}
_MENU_WORDS = {"menu", "co macie"}


class Kiosk:
    """Voice loop: listen -> understand -> speak."""

    def __init__(self) -> None:
        self.tts = TTSEngine()
        self.stt = STTEngine()
        self.nlp = NLPProcessor()

    def run(self) -> None:
        greeting = self.nlp.greeting()
        if greeting:
            self.tts.speak_wait(greeting)
        try:
            self._loop()
        except KeyboardInterrupt:
            logger.info("shutdown requested")
        finally:
            self.tts.stop()

    def _loop(self) -> None:
        while True:
            query = self.stt.listen(timeout=10)
            if not query:
                continue
            command = query.strip().lower()
            if command in _STOP_WORDS:
                self.tts.speak_wait("Do widzenia!")
                return
            if command in _MENU_WORDS:
                self.tts.speak(self.nlp.get_all_menu())
                continue
            self.tts.speak(self.nlp.process_query(query))


def _configure_logging() -> None:
    settings.ensure_runtime_dirs()
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.FileHandler(settings.LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def main() -> int:
    _configure_logging()
    try:
        Kiosk().run()
    except Exception:
        logger.exception("fatal error")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
