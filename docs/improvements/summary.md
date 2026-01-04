# Improvement Plan Summary

This document summarizes the proposed improvements for the ywfm project identified through codebase review.

## Overview

The ywfm project is well-structured but has opportunities for improvement in code quality, testing, and feature expansion.

## Categories

### [High Priority](./high-priority.md)
Critical code quality issues that should be addressed first:
- Type hint corrections in `src/main.py`
- Dead code removal
- Adding unit tests for core functionality
- Pre-commit configuration

### [Medium Priority](./medium-priority.md)
Feature enhancements for better user experience:
- List/cancel background reminders (`--list`, `--cancel`)
- Named reminders for easier management
- Dry run mode
- Configuration file support
- Recurring reminders

### [Removable Parts](./removable-parts.md)
Code simplification opportunities:
- `time_limit` flag simplification
- Redundant `sys.stdout.flush()` calls
- `description` field string concatenation pattern

### [Platform Limitation](./platform-limitation.md)
Installer improvements for broader Linux support:
- Currently assumes `apt` package manager
- Missing support for `dnf`, `pacman`, etc.

## Priority Matrix

| Priority | Effort | Impact | Items |
|----------|--------|--------|-------|
| High | Low | High | Type hints, dead code, tests |
| Medium | Medium | High | --list/--cancel commands |
| Medium | Low | Medium | Pre-commit config |
| Low | High | Medium | Recurring reminders, config file |
| Low | Medium | Low | Installer platform support |

## Task Tracking

See [tasks.todo](./tasks.todo) for actionable task list.
