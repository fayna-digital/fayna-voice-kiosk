"""Unit tests for the deterministic NLP processor (demo knowledge base).

No audio hardware needed — NLPProcessor only reads JSON data. The repository
root is put on the path by the top-level conftest.py.
"""

from src.nlp.processor import NLPProcessor


def test_menu_lists_dishes() -> None:
    assert "Placek" in NLPProcessor().get_all_menu()


def test_faq_opening_hours() -> None:
    assert "10:00" in NLPProcessor().process_query("jakie są godziny otwarcia")


def test_address_from_faq() -> None:
    assert "Przykładowa" in NLPProcessor().process_query("gdzie jest adres")


def test_greeting_is_data_driven() -> None:
    assert NLPProcessor().greeting()  # non-empty, sourced from knowledge.json


def test_unknown_query_returns_fallback() -> None:
    nlp = NLPProcessor()
    assert nlp.process_query("czy macie lądowisko dla helikoptera") == nlp.unknown_response
