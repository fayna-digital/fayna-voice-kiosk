# TZ — Fayna Kiosk

Специфікація за Fayna REPO_STANDARD (6 областей).

## 1. Objective

Голосовий кіоск для точки обслуговування: відвідувач ставить питання голосом,
кіоск розпізнає (STT), знаходить відповідь у базі знань закладу (NLP) і
відповідає голосом (TTS). Мета — розвантажити персонал від типових питань
(меню, години, адреса, довіз). **Успіх** = на типове питання кіоск дає
коректну голосову відповідь офлайн-стабільно; налаштування під новий заклад —
без правок коду.

## 2. Commands

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 -m src.main                 # запуск кіоску
python3 -m pytest tests/ -v         # тести
pre-commit run --all-files          # lint + guards
sudo bash scripts/install-kiosk.sh  # systemd-сервіс автозапуску (на пристрої)
```

## 3. Project Structure

- `src/` — двигун: `main.py` (цикл), `stt/`, `tts/`, `nlp/`, `kiosk/`.
- `config/settings.py` — усі налаштування.
- `data/*.json` — база знань закладу (демо). `data/audio|transcripts/` — runtime, git-ignored.
- `tests/` — юніт-тести NLP. `docs/` — ця специфікація + PLAN.
- `index.html` — демо-фронтенд.

## 4. Code Style

Ruff (`select = E,F,I,UP,B`, line-length 100), Python 3.10+. Приклад:

```python
def process_query(self, query: str) -> str:
    if not query or len(query) > MAX_QUERY_LENGTH:
        return self.unknown_response
    ...
```

Рядки, які чує/бачить відвідувач — мовою закладу (демо: польська), у `data/`, не в коді.

## 5. Testing Strategy

`pytest`. Тести NLP інстанціюють `NLPProcessor` на демо-даних і перевіряють
матч меню/FAQ/невідомого запиту (аудіо-заліза не потребують). Ціль покриття —
критичний шлях `process_query` ≥70%.

## 6. Boundaries

- **Always:** нове меню/FAQ → у `data/*.json`; тримати `data/` без PII у git.
- **Ask first:** публічність репо, публікація демо/скріншотів, зміна ліцензії.
- **Never:** комітити реальні розмови/аудіо, `.env`/`secrets.env`, AI-підписи;
  повертати дані закритого клієнта (вихідного проєкту) у цей репозиторій.

### Success Criteria

- [ ] `pytest tests/` зелений.
- [ ] `pre-commit run --all-files` зелений (у т.ч. no-ai-signature).
- [ ] Повнотекстовий пошук по репо не містить ідентифікаторів клієнта/PII.
- [ ] Налаштування під новий заклад досягається лише через `data/` + `config`.

### Open Questions

- Винести всю специфіку фронтенду (`index.html`) у `data/` (зараз частково вшито).
- Офлайн-STT (Vosk/Whisper) як заміна Google-залежності від інтернету.
