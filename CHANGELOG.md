# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [1.1.0] - 2026-01-04

### Added

- **Reminder Management Commands**
  - `--list` / `-l`: List all active background reminders with PID, name, subject, trigger time, and duration
  - `--cancel PID_OR_NAME`: Cancel a background reminder by PID or name
  - `--name` / `-n`: Assign a name to reminders for easier management
  - `--dry-run`: Preview reminder configuration without executing

- **Unit Tests**
  - Added `tests/test_config.py` with 20 tests for `ReminderConfig` class
  - Added `tests/test_manager.py` with 10 tests for `ReminderManager` class
  - Configured pytest with proper `pythonpath` in `pyproject.toml`

- **Pre-commit Configuration**
  - Added `.pre-commit-config.yaml` with ruff and pre-commit-hooks

- **Multi-Distro Linux Support** in installer
  - Auto-detection for apt, dnf, yum, pacman, zypper package managers
  - Fallback manual installation instructions when auto-install fails
  - Support for Debian/Ubuntu, Fedora/RHEL, CentOS, Arch Linux, openSUSE

- **Improvement Plan Documentation**
  - Added `docs/improvements/` with detailed implementation plans

### Changed

- **ReminderConfig Refactoring**
  - Replaced `time_limit` field with computed `is_time_limited` property
  - Removed `description` field, now computed dynamically in `_json_output()`
  - Simplified `wait_time` property using `max()` instead of side effects
  - Moved timer default initialization to `__post_init__`

- **Reminder Class Refactoring**
  - Extracted common notification logic to `_trigger_reminder()` method
  - Added `log_dir` instance variable for cleaner state management

- **Daemonize Improvements**
  - Moved `sys.stdout.flush()` before file descriptor closing (was no-op after)
  - Removed unnecessary `'r'` mode argument from `open(os.devnull)`

- **Installer Improvements**
  - Refactored `install_dependencies()` to use detected package manager
  - Added `detect_package_manager()` function
  - Added `show_manual_instructions()` for fallback guidance
  - Added `install_linux_dependency()` helper function

- **Configuration Updates**
  - Fixed deprecated ruff config: moved `select` to `[tool.ruff.lint]`
  - Added `[tool.pytest.ini_options]` configuration

### Fixed

- Corrected `Optional` type hints in `ReminderConfig` dataclass
  - `subject: str = None` → `subject: Optional[str] = None`
  - `created_at: str = None` → `created_at: Optional[str] = None`
  - `trigger_at: str = None` → `trigger_at: Optional[str] = None`

- Removed dead code (empty `else: pass` branch in `_run_background`)

- Fixed typo "installiing" → "installing" in `install.py`

### Documentation

- Added `CLAUDE.md` for Claude Code guidance
- Added `docs/improvements/summary.md` - improvement overview
- Added `docs/improvements/high-priority.md` - critical fixes
- Added `docs/improvements/medium-priority.md` - feature enhancements
- Added `docs/improvements/removable-parts.md` - code simplification
- Added `docs/improvements/platform-limitation.md` - Linux support
- Added `docs/improvements/tasks.todo` - task tracking
