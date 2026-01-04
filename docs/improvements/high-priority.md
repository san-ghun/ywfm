# High Priority Improvements

Critical code quality issues that should be addressed first.

## 1. Fix Type Hint Errors

**Location:** `src/main.py:37-47`

**Problem:**
```python
@dataclass
class ReminderConfig:
    subject: str = None          # Wrong
    message: Optional[str] = None  # Correct
    timer: Optional[str] = None
    # ...
```

Fields with `= None` defaults need `Optional[T]` type annotations.

**Solution:**
```python
from typing import Optional

@dataclass
class ReminderConfig:
    subject: Optional[str] = None
    message: Optional[str] = None
    timer: Optional[str] = None
    open_url: Optional[str] = None
    command: Optional[str] = None
    show_progress: bool = False
    background: bool = False
    created_at: Optional[str] = None
    trigger_at: Optional[str] = None
    description: str = ""
    time_limit: bool = False
```

**Verification:**
```bash
mypy src/main.py
```

---

## 2. Remove Dead Code

**Location:** `src/main.py:177-178`

**Problem:**
```python
def _run_background(self):
    # ...
    if self.os_name in ["Linux", "Darwin"]:
        # ... actual code ...
    else:
        pass  # Dead code - serves no purpose
```

**Solution:**
Remove the empty `else` branch entirely. The `NotificationManager.__init__` already raises `OSError` for unsupported OS, so this branch is unreachable.

---

## 3. Add Unit Tests

**Location:** Create `tests/` directory

**Problem:**
`pytest` is in dev dependencies but no tests exist.

**Solution:**
Create tests for core functionality:

```
tests/
├── __init__.py
├── test_config.py      # ReminderConfig tests
└── test_timer.py       # Timer parsing tests
```

**Key test cases for `test_config.py`:**
```python
import pytest
from src.main import ReminderConfig

class TestParseTimer:
    def test_hours_minutes_seconds(self):
        assert ReminderConfig.parse_timer("1h10m15s") == 4215

    def test_minutes_only(self):
        assert ReminderConfig.parse_timer("30m") == 1800

    def test_seconds_only(self):
        assert ReminderConfig.parse_timer("45s") == 45

    def test_hours_only(self):
        assert ReminderConfig.parse_timer("2h") == 7200

    def test_invalid_format(self):
        with pytest.raises(ValueError):
            ReminderConfig.parse_timer("invalid")

class TestWaitTime:
    def test_minimum_time_enforcement(self):
        config = ReminderConfig(timer="5s")
        assert config.wait_time == 15  # MIN_TIME
        assert config.time_limit == True

    def test_valid_time_no_limit(self):
        config = ReminderConfig(timer="30s")
        assert config.wait_time == 30
        assert config.time_limit == False
```

**Run tests:**
```bash
pytest tests/ -v
```

---

## 4. Add Pre-commit Configuration

**Location:** Create `.pre-commit-config.yaml`

**Problem:**
`pre-commit` is in dev dependencies but no configuration exists.

**Solution:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.2
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

**Setup:**
```bash
pre-commit install
pre-commit run --all-files
```

---

## 5. Fix Typo in install.py

**Location:** `install.py:134`

**Problem:**
```python
print(f"Error occurred while installiing Python libraries: {e}")
#                         ^^^^^^^^ typo
```

**Solution:**
```python
print(f"Error occurred while installing Python libraries: {e}")
```
