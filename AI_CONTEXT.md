# AI_CONTEXT — Fayna Kiosk

Короткий контекст для AI-асистента, що працює з цим репо.

**Що це:** голосовий кіоск (STT → NLP → TTS) для точки обслуговування. Продукт Fayna Digital.

**Точка входу:** `src/main.py` → `AIKiosk.initialize()` піднімає STT/TTS/NLP,
далі цикл listen → `NLPProcessor.process_query()` → TTS speak.

**Як працює NLP:** `src/nlp/processor.py` вантажить `data/knowledge.json` і
зіставляє нормалізований запит спершу з `faq`, тоді зі `dishes`, тоді з
полями `restaurant` (години/адреса/довіз). Немає матчу → `UNKNOWN_RESPONSE`.

**Дані ≠ код:** щоб налаштувати під інший заклад — правиться лише
`data/knowledge.json` (+ мова у `config/settings.py`). Код не чіпається.

**Заборони:** не комітити `data/audio`/`data/transcripts` (реальні розмови,
RODO), `.env`, `secrets.env`; не додавати AI co-author підписи (публічний репо).

**Тести:** `tests/test_nlp.py` — інстанціює `NLPProcessor` на демо-даних
(аудіо-заліза не потребує).
