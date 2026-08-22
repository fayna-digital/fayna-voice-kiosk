# Fayna Kiosk — głosowy kiosk dla punktu obsługi

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-LGPL--3-green.svg)
![Status](https://img.shields.io/badge/status-demo%20%2F%20portfolio-orange)

**Opracowane przez [Fayna Digital](https://www.fayna.agency)**
**Autor: Volodymyr Shevchenko**

---

Interaktywny **kiosk głosowy**: rozpoznaje mowę odwiedzającego (STT), odpowiada
żywym głosem (TTS) i odpowiada na pytania o menu, godziny otwarcia, adres,
dowóz i promocje przez prostą bazę wiedzy NLP. Działa w trybie pełnoekranowego
kiosku na tablecie/monitorze przy wejściu.

> ⚠️ **Konfiguracja demonstracyjna.** Repozytorium skonfigurowane na przykładzie
> **fikcyjnej** restauracji «Bistro Przykład» — wszystkie dane są zmyślone. Realne
> dane klientów (nagrania rozmów, prawdziwe menu, kontakty) **nie wchodzą** do
> tego repozytorium.

## Możliwości

| Funkcja | Opis |
|---------|------|
| **STT** | Rozpoznawanie mowy (Google Speech online, Sphinx offline jako fallback), język konfigurowany (`STT_LANGUAGE`). |
| **TTS** | Odpowiedź głosem przez `pyttsx3` (głosy systemowe, offline). |
| **NLP** | Dopasowanie zapytania do bazy wiedzy (`data/knowledge.json`): FAQ → dania → informacje o lokalu. |
| **Tryb kiosku** | Pełnoekranowy Chromium bez pasków, auto-start jako usługa systemd. |
| **Baza wiedzy jako dane** | Menu/FAQ/info — w JSON, bez edycji kodu pod nowego klienta. |

## Stack

Python 3.10+ · SpeechRecognition · pyttsx3 · Chromium (kiosk) · JSON knowledge base.

## Struktura

```
fayna-voice-kiosk/
├─ src/
│  ├─ main.py            # punkt wejścia, pętla kiosku
│  ├─ stt/engine.py      # rozpoznawanie mowy
│  ├─ tts/engine.py      # synteza mowy
│  ├─ nlp/processor.py   # dopasowanie zapytania do bazy wiedzy
│  └─ kiosk/kiosk_mode.py# pełnoekranowy Chromium
├─ config/settings.py    # wszystkie ustawienia (język, audio, ścieżki)
├─ data/                 # knowledge.json / menu.json / qa.json (demo)
├─ index.html            # demo-frontend kiosku
├─ scripts/install-kiosk.sh
├─ tests/                # testy jednostkowe NLP
└─ docs/                 # TZ.md (specyfikacja), PLAN.md
```

## Szybki start

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 -m src.main
```

Testy:

```bash
python3 -m pytest tests/ -v
```

## Konfiguracja pod lokal

Cała specyfika lokalu — w `data/knowledge.json` (nazwa, godziny, adres,
telefon, dania, FAQ) oraz `config/settings.py` (język STT/TTS, głośność, timeouty).
Kodu nie trzeba dotykać.

Prywatność (RODO/GDPR): nagrywanie audio/transkryptów odwiedzających jest
domyślnie **wyłączone** (`KIOSK_SAVE_AUDIO` / `KIOSK_SAVE_TRANSCRIPTS` = `False`).
Włącz tylko z podstawą prawną i wyraźnym oznakowaniem na miejscu.

## Licencja

LGPL-3.0 — patrz [LICENSE](LICENSE). © Fayna Digital.
