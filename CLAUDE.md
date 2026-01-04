# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ywfm** ("You're welcome, future me!") is a cross-platform Python CLI reminder/timer tool for macOS and Linux. It uses native notification systems (`terminal-notifier` on macOS, `notify-send` on Linux) to alert users after a specified time, with support for URL opening and command execution.

## Development Commands

```bash
# Install dependencies (uses uv)
uv sync

# Run the tool directly
python3 src/main.py -t 30s -s "Test" -m "Hello"

# Linting
ruff check src/
flake8 src/

# Formatting
black src/
isort src/

# Type checking
mypy src/

# Testing
pytest

# Build executable
pyinstaller --onefile src/main.py
```

## Architecture

The codebase is a single-file CLI application (`src/main.py`) with three core classes:

- **ReminderConfig** (dataclass): Holds configuration, parses timer strings (e.g., `1h10m15s`), enforces 15-second minimum
- **NotificationManager**: OS-aware notification dispatch - abstracts platform differences between macOS and Linux
- **Reminder**: Main orchestration - handles foreground execution (with optional tqdm progress bar), background daemonization (double-fork), and command execution

Key patterns:
- Timer format: `[Nh][Nm][Ns]` parsed via regex
- Background mode uses Unix double-fork daemonization
- Logs stored in `~/.local/state/ywfm/`
- JSON output always generated with 4 categories: `pid`, `params`, `info`, `extra`

## Dependencies

Runtime: `tqdm` (progress bars)

Dev: `black`, `flake8`, `isort`, `mypy`, `pre-commit`, `pyinstaller`, `pytest`, `ruff`

System: `terminal-notifier` (macOS via brew) or `notify-send`/`xdg-utils` (Linux via apt)
