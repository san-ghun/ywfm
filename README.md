# ywfm - "You're welcome, future me!"

Do something today that your future self will thank you for.

## Goal

- Python3 script file to execute and work as reminder, target OS for macOS and Linux.
- The program will use `terminal-notifier` for macOS and `notify-send` for Linux.
- The program will take options,

  - `--title <string>`
  - `--subtitle <string>`
  - `--open <URL>`
  - `--command <string>`
  - `--timer <string>`

- An example command would be like this:
  ```bash
  > reminder --title "Start building" --subtitle "github auth feat" --open "https://github.com/" --command 'echo hello' --timer 1h10m15s
  ```

---

### How to Use

0. Make it executable:
   ```bash
   chmod +x reminder.py
   ```
1. Install dependencies:
   - For macOS: Install `terminal-notifier` via `brew install terminal-notifier`.
   - For Linux: Ensure `notify-send` is available (e.g., `sudo apt install libnotify-bin` on Ubuntu/Debian).
2. Run the script with your desired options:
   ```bash
   ./reminder.py --title "Start building" --subtitle "github auth feat" --open "https://github.com/" --command 'echo hello' --timer 1h10m15s
   ```

### Features

- Parses `--timer` in a human-readable format (e.g., `1h10m15s`).
- Supports optional `--subtitle`, `--open`, and `--command`.
- Compatible with macOS and Linux.

---

Say thank you to past self.

> Thank you, past me.
>
> _Good job, future me._
>
> Well done, past me.
>
> And, thanks a lot.
