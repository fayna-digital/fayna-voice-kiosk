"""Text-to-speech engine backed by pyttsx3, with a background speech queue."""

from __future__ import annotations

import logging
import queue
import threading
from typing import Any

import pyttsx3

from config import settings

logger = logging.getLogger(__name__)

# Preferred offline voices, best first: a Polish female voice if available,
# otherwise any listed female voice, otherwise the system default.
_PREFERRED_VOICES = ("Zosia", "Ewa", "Agnieszka", "Paulina", "Milena", "Monika")


class TTSEngine:
    """Speak text aloud; queued so callers never block on the audio device."""

    def __init__(self) -> None:
        self._queue: queue.Queue[str] = queue.Queue()
        self._running = True
        self._engine = self._build_engine()
        self._worker = threading.Thread(target=self._drain_queue, daemon=True)
        self._worker.start()
        logger.info("TTS ready: rate=%s", settings.TTS_RATE)

    def _build_engine(self) -> Any | None:
        try:
            engine = pyttsx3.init()
        except Exception:
            logger.exception("TTS engine unavailable")
            return None
        engine.setProperty("rate", settings.TTS_RATE)
        engine.setProperty("volume", settings.TTS_VOLUME)
        voice_id = self._pick_voice(engine)
        if voice_id:
            engine.setProperty("voice", voice_id)
        return engine

    @staticmethod
    def _pick_voice(engine: Any) -> str | None:
        voices = engine.getProperty("voices")
        for wanted in _PREFERRED_VOICES:
            for voice in voices:
                if wanted.lower() in voice.name.lower():
                    logger.info("selected voice: %s", voice.name)
                    return str(voice.id)
        return str(voices[0].id) if voices else None

    def speak(self, text: str) -> None:
        """Queue text to be spoken (non-blocking)."""
        clamped = self._clamp(text)
        if clamped:
            self._queue.put(clamped)

    def speak_wait(self, text: str) -> None:
        """Speak text and block until it finishes."""
        clamped = self._clamp(text)
        if clamped:
            self._say(clamped)

    @staticmethod
    def _clamp(text: str) -> str:
        if not text:
            return ""
        if len(text) > settings.TTS_MAX_CHARS:
            return text[: settings.TTS_MAX_CHARS - 3] + "..."
        return text

    def _drain_queue(self) -> None:
        while self._running:
            try:
                text = self._queue.get(timeout=1)
            except queue.Empty:
                continue
            self._say(text)
            self._queue.task_done()

    def _say(self, text: str) -> None:
        if not self._engine:
            return
        try:
            self._engine.say(text)
            self._engine.runAndWait()
        except RuntimeError as exc:
            logger.error("speech failed: %s", exc)

    def stop(self) -> None:
        self._running = False
        if self._worker.is_alive():
            self._worker.join(timeout=2)
        if self._engine:
            try:
                self._engine.stop()
            except RuntimeError:
                pass
