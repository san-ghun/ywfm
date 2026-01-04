# Removable/Simplifiable Parts

Code simplification opportunities to improve maintainability.

## 1. Simplify `time_limit` Flag

**Location:** `src/main.py:47, 64-65, 131-133`

**Current implementation:**
```python
@dataclass
class ReminderConfig:
    time_limit: bool = False

    @property
    def wait_time(self) -> int:
        # ...
        if total_seconds < self.MIN_TIME:
            self.time_limit = True  # Side effect in property
            total_seconds = self.MIN_TIME
        return total_seconds

class Reminder:
    def run(self):
        if self.config.time_limit:
            info += f"[INFO] Given timer value is too small..."
```

**Problem:**
- Property has side effect (sets `time_limit`)
- Flag is only used to generate a warning message
- Mixing concerns

**Suggested simplification:**
```python
@dataclass
class ReminderConfig:
    # Remove time_limit field entirely

    @property
    def wait_time(self) -> int:
        total_seconds = self.parse_timer(self.timer)
        return max(total_seconds, self.MIN_TIME)

    @property
    def is_time_limited(self) -> bool:
        """Check if original timer was below minimum."""
        return self.parse_timer(self.timer) < self.MIN_TIME

    def get_time_limit_warning(self) -> str:
        if self.is_time_limited:
            return f"[INFO] Given timer value is too small, applying MIN_TIME {self.MIN_TIME} seconds.\n"
        return ""
```

---

## 2. Remove Redundant `sys.stdout.flush()`

**Location:** `src/main.py:242-243`

**Current implementation:**
```python
def daemonize(self):
    # ...
    for fd in range(0, 1024):
        try:
            os.close(fd)
        except OSError:
            pass

    sys.stdout.flush()  # Redundant - stdout is already closed
    sys.stderr.flush()  # Redundant - stderr is already closed
    # ...
```

**Problem:**
These flush calls occur after all file descriptors (0-1023) are closed, making them no-ops or potential errors.

**Solution:**
Move flush calls before the fd closing loop, or remove entirely:
```python
def daemonize(self):
    # ...
    sys.stdout.flush()
    sys.stderr.flush()

    for fd in range(0, 1024):
        try:
            os.close(fd)
        except OSError:
            pass
    # ...
```

---

## 3. Simplify `description` Field Concatenation

**Location:** `src/main.py:46, 133, 148`

**Current implementation:**
```python
@dataclass
class ReminderConfig:
    description: str = ""

class Reminder:
    def run(self):
        if self.config.time_limit:
            info += f"[INFO] ..."
            self.config.description += info  # String concatenation

    def _run_background(self):
        self.config.description += f"[INFO] Output and error..."  # More concatenation
```

**Problem:**
- Mutable state in dataclass
- String concatenation is inefficient for multiple appends
- Hard to track what's been added

**Suggested simplification:**
```python
@dataclass
class ReminderConfig:
    # Remove description field

class Reminder:
    def __init__(self, config: ReminderConfig):
        self.config = config
        self.info_messages: list[str] = []

    def _add_info(self, message: str):
        self.info_messages.append(message)

    @property
    def description(self) -> str:
        return "\n".join(self.info_messages)
```

---

## 4. Remove Empty Else Branch

**Location:** `src/main.py:177-178`

**Current implementation:**
```python
def _run_background(self):
    if self.os_name in ["Linux", "Darwin"]:
        # ... actual implementation ...
    else:
        pass  # Does nothing
```

**Solution:**
Simply remove the else branch. The `NotificationManager.__init__` already validates OS support, so this code path is unreachable.

---

## 5. Extract Common Execution Logic

**Location:** `src/main.py:136-139, 174-176, 190-192`

**Current implementation:**
Both `_run_foreground` and `_run_background` end with:
```python
self.notifier.send(self.config.subject, self.config.message, self.config.open_url)
if self.config.command:
    self._execute_command()
```

**Suggested simplification:**
```python
def _execute_reminder(self):
    """Common execution logic for both foreground and background modes."""
    self.notifier.send(
        self.config.subject,
        self.config.message,
        self.config.open_url
    )
    if self.config.command:
        self._execute_command()

def _run_foreground(self):
    # ... setup code ...
    time.sleep(self.config.wait_time)
    self._execute_reminder()

def _run_background(self):
    # ... daemon setup ...
    time.sleep(self.config.wait_time)
    self._execute_reminder()
```
