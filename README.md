# ywfm - "You're welcome, future me!"

> "Do something today that your future self will thank you for."

A simple Python3-based reminder tool for macOS and Linux that uses native notification systems to alert the user after a specified time. It also supports opening URLs and executing commands when the timer ends.

## Features

- **Cross-platform**: Works on macOS (using `terminal-notifier`) and Linux (using `notify-send`).
- **Customizable notifications**: Add a title, body, URL to open, and a command to execute.
- **Timer support**: Specify the delay using a human-readable format like `1h10m15s`.
- **Background execution**: Option to run the reminder as a background process.
- **Visual feedback**: Option to run the reminder visually with a progress bar.

## Requirements

### Python

- Python 3.6 or later.

## Installation

### Prerequisites

Ensure you have Python 3 installed on your system.

- **macOS**:
  - Homebrew (for installing `terminal-notifier` if not already installed).
- **Linux**:
  - `notify-send` and `xdg-utils` packages.

<details>
  <summary><i>In case, installing all dependencies manually</i></summary>
    
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
  </details>

<details>
   <summary><i>Why Python Installation?</i></summary>

- **Consistency**: Ensures Python is set up correctly and used as a single installation environment.
- **Cross-Platform**: Adapts easily to macOS and Linux without relying on shell commands.
- **Extensibility**: Easy to enhance for additional features like user-specific installations.
</details>

### Library

- **Python**:
  - `tqdm` package(library) for a progress bar.

### Steps

1. Clone or download the repository containing `reminder.py` and `install.py`.
2. Run the installer:
   ```bash
   python3 install.py
   ```
3. Ensure `~/.local/bin` is in your `PATH`:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```
   Add the above line to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.) for persistence.

## Usage

Run the script with the required options. Below are the available options:

```bash
ywfm --title <string> --body <string> --open <URL> --command <string> --timer <string> [--background] [--show-progress]
```

### Options

| Option            | Description                                                      |
| ----------------- | ---------------------------------------------------------------- |
| `--title`         | **Required**: Title for the reminder notification.               |
| `--body`          | Optional: Body for the notification.                             |
| `--open`          | Optional: URL to open when the notification is triggered.        |
| `--command`       | Optional: Command to execute after the timer ends.               |
| `--timer`         | Optional: Timer duration, default 15m (e.g., `1h10m15s`, `10s`). |
| `--background`    | Optional: Run the reminder as a background process.              |
| `--show-progress` | Optional: Run the reminder visually with progress bar.           |

### Examples

1. **Simple Reminder**:

   ```bash
   ywfm --title "Time to Work" --body "Start your project" --timer 30m
   ```

2. **Reminder with URL**:

   ```bash
   ywfm --title "Check GitHub" --body "Explore the repository" --open "https://github.com" --timer 10s
   ```

3. **Reminder with Command**:

   ```bash
   ywfm --title "Hello World" --body "Executing command" --command 'echo "Hello, World!"' --timer 1m
   ```

4. **Background Reminder**:

   ```bash
   ywfm --title "Background Task" --body "Running in background" --timer 2h --background
   ```

5. **Progress bar**:

   ```bash
   ywfm --title "Break Time" --body "Take a 10-minute break" --timer 10m --show-progress
   ```

## Stopping a Background Reminder

If you start a reminder with the `--background` option, the script prints the process ID (PID). To stop it, use the `kill` command:

```bash
kill <PID>
```

## How It Works

1. **Timer**: The program calculates the delay based on the provided timer option and runs until triggered.
2. **Notifications**:
   - **macOS**: Uses `terminal-notifier` to display notifications and open URLs.
   - **Linux**: Uses `notify-send` to display notifications and `xdg-open` to open URLs.
3. **Custom Commands**: Executes shell commands as specified in the `--command` option.
4. **Visual feedback**: Uses `tqdm` Python package to show progress bar.

## Uninstallation

To remove the script:

1. Delete the installed script:

   ```bash
   rm ~/.local/bin/ywfm
   ```

2. Optionally, remove the dependencies (`terminal-notifier` or `libnotify-bin`).

## Contributing

Feel free to fork the repository and submit pull requests to improve the script or its documentation.

## License

This project is licensed under the MIT License.

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
> _Your welcome, future me._
>
> Thanks a lot.
