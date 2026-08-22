"""Keyword-based NLP over a restaurant knowledge base.

Deterministic on purpose: a kiosk must never invent menu items, prices or
allergen information, so every answer is matched against curated JSON data.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from config.settings import (
    KNOWLEDGE_FILE,
    MAX_QUERY_LENGTH,
    MENU_FILE,
    QA_FILE,
    UNKNOWN_RESPONSE,
)

logger = logging.getLogger(__name__)

_HOURS_KEYS = ("godzin", "czynne", "otwar")
_ADDRESS_KEYS = ("adres", "gdzie", "znajdu")
_DELIVERY_KEYS = ("dowóz", "dowoz", "dostaw")


class NLPProcessor:
    """Answer visitor questions from the knowledge base, or fall back gracefully."""

    def __init__(self) -> None:
        self.knowledge = self._load(KNOWLEDGE_FILE)
        self.menu = self._load(MENU_FILE)
        self.qa = self._load(QA_FILE)
        self.unknown_response = UNKNOWN_RESPONSE
        logger.info("NLP ready: %d dishes", len(self.knowledge.get("dishes", [])))

    @staticmethod
    def _load(path: Path) -> dict[str, Any]:
        try:
            with path.open(encoding="utf-8") as handle:
                return json.load(handle)
        except FileNotFoundError:
            logger.warning("knowledge file not found: %s", path)
            return {}
        except json.JSONDecodeError as exc:
            logger.error("invalid JSON in %s: %s", path, exc)
            return {}

    def greeting(self) -> str:
        """Opening line spoken on start — taken from the data, never hard-coded."""
        return self.knowledge.get("restaurant", {}).get("greeting", "")

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"[^\w\s]", "", text.lower()).strip()

    def process_query(self, query: str) -> str:
        if not query or len(query) > MAX_QUERY_LENGTH:
            return self.unknown_response

        norm = self._normalize(query)

        for key, answer in self.knowledge.get("faq", {}).items():
            if key in norm:
                return answer

        for dish in self.knowledge.get("dishes", []):
            if self._normalize(dish["name"]) in norm:
                return f"{dish['name']} – {dish['description']} Cena: {dish['price']} zł."

        restaurant = self.knowledge.get("restaurant", {})
        if any(word in norm for word in _HOURS_KEYS):
            return restaurant.get("hours", self.unknown_response)
        if any(word in norm for word in _ADDRESS_KEYS):
            return restaurant.get("address", self.unknown_response)
        if any(word in norm for word in _DELIVERY_KEYS):
            return restaurant.get("delivery", self.unknown_response)

        return self.unknown_response

    def get_all_menu(self) -> str:
        dishes = self.knowledge.get("dishes", [])
        if not dishes:
            return "Menu jest chwilowo niedostępne."
        lines = "\n".join(f"• {dish['name']} — {dish['price']} zł" for dish in dishes)
        return f"Nasze menu:\n{lines}"
