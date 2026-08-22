"""Speech-to-text engine (SpeechRecognition backends)."""

from __future__ import annotations

import datetime
import logging

import speech_recognition as sr

from config import settings

logger = logging.getLogger(__name__)


class STTEngine:
    """Capture microphone audio and transcribe it with the configured backend."""

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.language = settings.STT_LANGUAGE
        self.engine = settings.STT_ENGINE
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        logger.info("STT ready: engine=%s language=%s", self.engine, self.language)

    def listen(self, timeout: float = 5.0, phrase_time_limit: float = 10.0) -> str:
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
        except sr.WaitTimeoutError:
            return ""

        text = self._recognize(audio)
        if not text:
            return ""

        logger.info("recognized: %s", text)
        if settings.SAVE_AUDIO:
            self._save_audio(audio)
        if settings.SAVE_TRANSCRIPTS:
            self._save_transcript(text)
        return text

    def _recognize(self, audio: sr.AudioData) -> str:
        try:
            if self.engine == "sphinx":
                return self.recognizer.recognize_sphinx(audio, language=self.language)
            return self.recognizer.recognize_google(audio, language=self.language)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as exc:
            logger.error("recognition service error: %s", exc)
            return ""

    def _save_audio(self, audio: sr.AudioData) -> None:
        settings.AUDIO_DIR.mkdir(mode=0o750, parents=True, exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        (settings.AUDIO_DIR / f"audio_{stamp}.wav").write_bytes(audio.get_wav_data())

    def _save_transcript(self, text: str) -> None:
        settings.TRANSCRIPTS_DIR.mkdir(mode=0o750, parents=True, exist_ok=True)
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = settings.TRANSCRIPTS_DIR / f"transcript_{stamp}.txt"
        path.write_text(f"{stamp}: {text}\n", encoding="utf-8")
