# Medium Priority Improvements

Feature enhancements for better user experience.

## 1. List/Cancel Background Reminders

**Problem:**
Currently users must manually find and kill background processes:
```bash
kill $(cat ~/.local/state/ywfm/ywfm.pid)
```

**Solution:**
Add `--list` and `--cancel` command-line options.

**Proposed CLI:**
```bash
# List all active reminders
ywfm --list

# Cancel a specific reminder by PID
ywfm --cancel 12345

# Cancel all reminders
ywfm --cancel-all
```

**Implementation approach:**
1. Read JSON files from `~/.local/state/ywfm/*.json`
2. Check if PIDs are still running using `os.kill(pid, 0)`
3. Display active reminders in table format
4. For cancel: send SIGTERM to the process

**Example output for `--list`:**
```
PID     Subject         Trigger At              Duration
12345   Long Task       2024-03-21 16:30:00     2h
12346   Break           2024-03-21 14:45:00     30m
```

---

## 2. Named Reminders

**Problem:**
PIDs are hard to remember and manage.

**Solution:**
Allow optional naming of reminders for easier reference.

**Proposed CLI:**
```bash
# Create named reminder
ywfm -t 1h -s "Lunch" --name lunch -b

# Cancel by name
ywfm --cancel lunch
```

**Implementation approach:**
1. Add `--name` argument to argparse
2. Store name in JSON output and as symlink: `~/.local/state/ywfm/names/lunch -> 12345.json`
3. Resolve name to PID when cancelling

---

## 3. Dry Run Mode

**Problem:**
No way to verify reminder configuration without actually starting it.

**Solution:**
Add `--dry-run` flag that shows what would happen.

**Proposed CLI:**
```bash
ywfm -t 1h30m -s "Meeting" -o "https://zoom.us/..." --dry-run
```

**Example output:**
```json
{
  "mode": "dry-run",
  "params": {
    "subject": "Meeting",
    "message": "Well done!",
    "duration": "1h30m",
    "url": "https://zoom.us/...",
    "command": null
  },
  "info": {
    "would_trigger_at": "2024-03-21 16:30:00",
    "seconds": 5400
  }
}
```

---

## 4. Configuration File Support

**Problem:**
Users must specify all options every time.

**Solution:**
Support configuration file for defaults.

**Location:** `~/.config/ywfm/config.toml`

**Example config:**
```toml
[defaults]
subject = "Reminder"
show_progress = true

[messages]
# Random message pool
pool = [
    "Well done!",
    "You're welcome!",
    "Great job!",
    "Time's up!"
]
```

**Implementation approach:**
1. Add `tomllib` (Python 3.11+) or `tomli` dependency
2. Load config on startup if exists
3. CLI arguments override config values

---

## 5. Recurring Reminders

**Problem:**
No support for repeated reminders (e.g., Pomodoro technique).

**Solution:**
Add `--repeat` option for recurring reminders.

**Proposed CLI:**
```bash
# Pomodoro: 25 min work, repeat 4 times
ywfm -t 25m -s "Pomodoro" --repeat 4

# Infinite repeat until cancelled
ywfm -t 1h -s "Hydrate" --repeat infinite -b
```

**Implementation approach:**
1. Add `--repeat` argument (int or "infinite")
2. Wrap execution in loop
3. Track iteration count in JSON output
4. For background mode: spawn new daemon after each notification

**Considerations:**
- How to handle `--command` with repeat? Execute each time or once?
- Should there be a `--repeat-delay` option?
