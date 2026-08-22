# PLAN — Fayna Kiosk

## Phase 0 — Extract & sanitize ✅ (2026-07-01)

Витяг двигуна з клієнтського проєкту, знеособлення, приведення до REPO_STANDARD,
fresh git history без AI-підписів. (Процедура Project Sunset.)

## Phase 1 — Demo hardening

- Тести на всі гілки `process_query` (faq / dish / restaurant / unknown).
- Прогнати `index.html` як самодостатнє демо (без залежності від мікрофона).
- README-скріншот/GIF демо (синтетичний, без реальних людей).

## Phase 2 — Config-driven

- Винести весь контент `index.html` у `data/` (єдине джерело істини для тексту).
- Мова/голос/стиль — повністю через `config/settings.py`.

## Phase 3 — Productization (опційно)

- Офлайн-STT (Vosk/Whisper) → зняти залежність від інтернету.
- Пакет/інсталятор під пристрій-кіоск; чек-лист розгортання.
- Багатомовність (див. скіл i18n-localization).

## Checkpoints

- Кінець Phase 1 → готове до публічного портфоліо-показу.
- Кінець Phase 2 → готове до повторного продажу під новий заклад «з коробки».
