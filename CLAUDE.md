# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

kozRandBot is an async Telegram bot (Python + aiogram 2.x) that provides randomization utilities: random numbers, list item picking, yes/no answers, coin flips, password generation, and UUIDs. Supports both polling (debug) and webhook (production) modes.

## Commands

### Setup
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
# Copy example config (required for tests)
cp config.py.example app/data/config.py
```

### Running Tests
```bash
pytest
pytest tests/test_rand.py   # single file
pytest -v                   # verbose
```

### Local Development
```bash
# Edit app/data/config.py: set DEBUG=True, add TOKEN
python app/bot.py   # uses polling mode
```

### Docker
```bash
./start.sh          # sets up config and runs docker-compose
docker compose up -d --build
```

## Architecture

### Entry Point & Bot Structure
`app/bot.py` — registers all message command handlers and starts the bot (polling or webhook). Prometheus metrics server starts on port 8000.

### Inline Handler Plugin System
`app/handler/` — pattern-based inline query handlers:
- `abc.py` — `InlineHandler` abstract base class + `HTMLMixin`/`MarkdownMixin`/`UniversalMixin` for formatting
- `impls.py` — concrete handlers: `FlipCoinHandler`, `RandNumHandler`, `YesNoHandler`, `RandItemHandler`, `PasswordHandler`, `HEXPasswordHandler`, `UUIDHandler`
- `loader.py` — `InlineHandlersLoader` discovers handler subclasses via reflection at startup

To add a new inline handler: create a subclass of `InlineHandler` in `impls.py`; the loader picks it up automatically.

### Core Modules
- `app/rand.py` — all randomization logic; uses `random.Random()` for standard users, `random.SystemRandom()` for premium users
- `app/util.py` — `Items` class parses comma/semicolon/conjunction-separated input; `from_premium()` checks hardcoded UID list
- `app/localization.py` — multi-language strings via `klocmod`
- `app/commands.py` — registers bot commands with Telegram API

### Configuration (`app/data/config.py`)
Not tracked in git. Key settings:
- `TOKEN` — Telegram bot token
- `DEBUG` — `True` = polling (local dev), `False` = webhooks (production)
- `PREMIUM_USERS_UID` — list of Telegram user IDs that get `SystemRandom`
- Password settings: `MIN/MAX/DEFAULT_PASSWORD_LENGTH`, `PASSWORD_EXTRA_CHARS`
- Network: `APP_HOST`, `APP_PORT`, `HOST`, `SERVER_PORT`, `SOCKET_TYPE` (TCP or UNIX)

### Testing
- `tests/test_rand.py` — property-based tests with `hypothesis`
- `tests/test_list.py` — `Items` parser edge cases
- `tests/test_handlers/` — handler impl and loader tests
- `PYTHONPATH=app` is required because tests import from the `app/` package root

### Deployment
Production uses Docker + nginx reverse proxy. Webhook URL pattern: `https://<HOST>/bot/<TOKEN>`. Metrics at `:8001`, app at `:8011` (docker-compose port mapping).
