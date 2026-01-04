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
uv run ruff check src/

# Testing
uv run pytest -v

# Build executable
pyinstaller --onefile src/main.py
```

## CLI Usage

```bash
# Basic reminder
ywfm -t 30m -s "Break" -m "Take a break!"

# Background reminder with name
ywfm -t 1h -s "Meeting" -n meeting -b

# List active reminders
ywfm --list

# Cancel by PID or name
ywfm --cancel 12345
ywfm --cancel meeting

# Preview without executing
ywfm -t 1h --dry-run
```

## Architecture

The codebase is a single-file CLI application (`src/main.py`) with four core classes:

- **ReminderConfig** (dataclass): Holds configuration, parses timer strings (e.g., `1h10m15s`), enforces 15-second minimum via `is_time_limited` property
- **NotificationManager**: OS-aware notification dispatch - abstracts platform differences between macOS and Linux
- **Reminder**: Main orchestration - handles foreground execution (with optional tqdm progress bar), background daemonization (double-fork), and command execution via `_trigger_reminder()`
- **ReminderManager**: Manages background reminders - list active, cancel by PID or name

Key patterns:
- Timer format: `[Nh][Nm][Ns]` parsed via regex
- Background mode uses Unix double-fork daemonization
- Logs and state stored in `~/.local/state/ywfm/`
- JSON output with 4 categories: `pid`, `params`, `info`, `extra`

## Tests

```bash
uv run pytest -v
```

Test files:
- `tests/test_config.py` - ReminderConfig, parse_timer, wait_time
- `tests/test_manager.py` - ReminderManager, list/cancel operations

## Dependencies

Runtime: `tqdm` (progress bars)

Dev: `ruff`, `pytest`, `pre-commit`, `pyinstaller`, `mypy`

System:
- macOS: `terminal-notifier` (via Homebrew)
- Linux: `notify-send`/`xdg-utils` (auto-detected: apt, dnf, yum, pacman, zypper)
