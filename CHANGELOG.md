# Changelog

Формат — [Keep a Changelog](https://keepachangelog.com/uk/1.1.0/),
версіонування — [SemVer](https://semver.org/lang/uk/).

## [0.1.0] — 2026-07-01

### Added
- Початковий публічний витяг двигуна **Fayna Kiosk** (STT / TTS / NLP / kiosk mode).
- Демо-набір даних для вигаданого ресторану «Bistro Przykład» (усе фіктивне).
- Репозиторій приведено до Fayna **REPO_STANDARD**: README, LICENSE, CLAUDE.md,
  `docs/TZ.md`, `docs/PLAN.md`, `tests/`, `.pre-commit-config.yaml`, CI.
- `no-ai-signature` guard (pre-commit) — блокує AI-атрибуцію в коді й комітах.

### Notes
- Витягнуто з внутрішнього клієнтського проєкту за процедурою **Project Sunset**.
  Свідомо **не перенесено**: ідентичність клієнта, реальні записи розмов
  відвідувачів (RODO), стара git-історія з AI-підписами, macOS-специфічний
  `pip freeze` (замінено на охайний `requirements.txt`).
