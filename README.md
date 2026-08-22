# Fayna Kiosk — голосовий кіоск для точки обслуговування

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-LGPL--3-green.svg)
![Status](https://img.shields.io/badge/status-demo%20%2F%20portfolio-orange)

**Розроблено [Fayna Digital](https://www.fayna.agency)**
**Автор: Volodymyr Shevchenko**

---

Інтерактивний **голосовий кіоск**: розпізнає мову відвідувача (STT), відповідає
живим голосом (TTS) і відповідає на питання про меню, години роботи, адресу,
довіз і промоції через просту NLP-базу знань. Працює у повноекранному
кіоск-режимі на планшеті/моніторі біля входу.

> ⚠️ **Демонстраційна конфігурація.** Репозиторій налаштований на прикладі
> **вигаданого** ресторану «Bistro Przykład» — усі дані фіктивні. Реальні
> клієнтські дані (записи розмов, справжнє меню, контакти) у цей репозиторій
> **не входять**.

## Можливості

| Функція | Опис |
|---------|------|
| **STT** | Розпізнавання мови (Google Speech online, Sphinx offline як fallback), мова конфігурується (`STT_LANGUAGE`). |
| **TTS** | Відповідь голосом через `pyttsx3` (системні голоси, офлайн). |
| **NLP** | Зіставлення запиту з базою знань (`data/knowledge.json`): FAQ → страви → інфо про заклад. |
| **Кіоск-режим** | Повноекранний Chromium без панелей, авто-старт як systemd-сервіс. |
| **База знань як дані** | Меню/FAQ/інфо — у JSON, без правок коду під нового клієнта. |

## Стек

Python 3.10+ · SpeechRecognition · pyttsx3 · Chromium (kiosk) · JSON knowledge base.

## Структура

```
fayna-voice-kiosk/
├─ src/
│  ├─ main.py            # точка входу, цикл кіоску
│  ├─ stt/engine.py      # розпізнавання мови
│  ├─ tts/engine.py      # синтез мови
│  ├─ nlp/processor.py   # зіставлення запиту з базою знань
│  └─ kiosk/kiosk_mode.py# повноекранний Chromium
├─ config/settings.py    # усі налаштування (мова, аудіо, шляхи)
├─ data/                 # knowledge.json / menu.json / qa.json (демо)
├─ index.html            # демо-фронтенд кіоску
├─ scripts/install-kiosk.sh
├─ tests/                # юніт-тести NLP
└─ docs/                 # TZ.md (специфікація), PLAN.md
```

## Швидкий старт

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 -m src.main
```

Тести:

```bash
python3 -m pytest tests/ -v
```

## Налаштування під заклад

Уся специфіка закладу — у `data/knowledge.json` (назва, години, адреса,
телефон, страви, FAQ) та `config/settings.py` (мова STT/TTS, гучність, таймаути).
Код чіпати не треба.

## Ліцензія

LGPL-3.0 — див. [LICENSE](LICENSE). © Fayna Digital.
