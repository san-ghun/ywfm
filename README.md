# ywfm - "You're welcome, future me!"

> "Do something today that your future self will thank you for."

A simple Python3-based reminder tool for macOS and Linux that uses native notification systems to alert the user after a specified time. It also supports opening URLs and executing commands when the timer ends.

## Features

- **Cross-platform**: Works on macOS (using `terminal-notifier`) and Linux (using `notify-send`).
- **Customizable notifications**: Add a title, subtitle, URL to open, and a command to execute.
- **Timer support**: Specify the delay using a human-readable format like `1h10m15s`.
- **Background execution**: Option to run the reminder as a background process.

## Requirements

### macOS

- [`terminal-notifier`](https://github.com/julienXX/terminal-notifier): Install via Homebrew:
  ```bash
  brew install terminal-notifier
  ```

### Linux

- `notify-send`: Install via your package manager:
  ```bash
  sudo apt install libnotify-bin  # For Ubuntu/Debian
  ```
- `xdg-utils`: For opening URLs:
  ```bash
  sudo apt install xdg-utils  # For Ubuntu/Debian
  ```

### Python

- Python 3.6 or later.

## Installation

1. Clone this repository or download `reminder.py`.
2. Make the script executable:

   ```bash
   chmod +x reminder.py
   ```

## Usage

Run the script with the required options. Below are the available options:

```bash
./reminder.py --title <string> --subtitle <string> --open <URL> --command <string> --timer <string> [--background]
```

### Options

| Option         | Description                                                    |
| -------------- | -------------------------------------------------------------- |
| `--title`      | **Required**: Title for the reminder notification.             |
| `--subtitle`   | Optional: Subtitle for the notification.                       |
| `--open`       | Optional: URL to open when the notification is triggered.      |
| `--command`    | Optional: Command to execute after the timer ends.             |
| `--timer`      | **Required**: Timer duration (e.g., `1h10m15s`, `30m`, `10s`). |
| `--background` | Optional: Run the reminder as a background process.            |

### Examples

1. **Simple Reminder**:

   ```bash
   ./reminder.py --title "Time to Work" --subtitle "Start your project" --timer 30m
   ```

2. **Reminder with URL**:

   ```bash
   ./reminder.py --title "Check GitHub" --subtitle "Explore the repository" --open "https://github.com" --timer 10s
   ```

3. **Reminder with Command**:

   ```bash
   ./reminder.py --title "Hello World" --subtitle "Executing command" --command 'echo "Hello, World!"' --timer 1m
   ```

4. **Background Reminder**:

   ```bash
   ./reminder.py --title "Background Task" --subtitle "Running in background" --timer 2h --background
   ```

## Stopping a Background Reminder

If you start a reminder with the `--background` option, the script prints the process ID (PID). To stop it, use the `kill` command:

```bash
kill <PID>
```

## License

This project is licensed under the MIT License. See the [LICENSE](https://chatgpt.com/c/LICENSE) file for details.

## Author

Sanghun Park

---

Say thank you to past self.

> Thank you, past me.
>
> _Good job, future me._
>
> Well done, past me.
>
> And, thanks a lot.
