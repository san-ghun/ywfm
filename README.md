# ywfm - "You're welcome, future me!"

> "Do something today that your future self will thank you for."

A simple Python3-based reminder tool for macOS and Linux that uses native notification systems to alert the user after a specified time. It also supports opening URLs and executing commands when the timer ends.

- [한국어](/readme/kor.md)

## Features

- **Cross-platform**: Works on macOS (using `terminal-notifier`) and Linux (using `notify-send`).
- **Customizable notifications**: Add a subject, message, URL to open, and a command to execute.
- **Timer support**: Specify the delay using a human-readable format like `1h10m15s`.
- **Visual feedback**: Option to run the reminder visually with a progress bar.
- **Background execution**: Option to run the reminder as a background process with logging.
- **JSON output**: Outputs reminder details in JSON format when running in background.
- **Minimum time limit**: Enforces a minimum time of 15 seconds for all reminders.
- **Default messages**: Provides friendly default messages if none specified.
- **Logging**: Stores background process logs in `~/.local/state/ywfm/`.

## Requirements

### Python

- Python 3.6 or later
- `tqdm` package for progress bar visualization

### System Dependencies

- **macOS**:
  - `terminal-notifier` for notifications
  - Homebrew (recommended for installing dependencies)
- **Linux**:
  - `notify-send` (libnotify-bin) for notifications
  - `xdg-utils` for opening URLs

## Installation

### Automated Installation

The installer script (`install.py`) handles all dependencies and setup:

1. Clone or download the repository
2. Run the installer:

   ```bash
   python3 install.py
   ```

   The installer will:

   - Check for missing system dependencies
   - Prompt before installing any missing dependencies
   - Install required Python packages
   - Set up the executable in your PATH

   Note: You may need:

   - macOS: Homebrew installed (https://brew.sh)
   - Linux: sudo privileges for package installation

3. The installer will guide you through adding the following to your PATH:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```
   Add this to your shell config file (`~/.bashrc`, `~/.zshrc`, etc.) for persistence.

### Manual Installation

<details>
  <summary>Click to expand manual installation steps</summary>

#### Prerequisites Check

1. Check system dependencies:

   - macOS: `which terminal-notifier`
   - Linux: `which notify-send xdg-open`

2. Check Python packages:
   ```bash
   python3 -m pip show tqdm
   ```

#### System Dependencies

1. macOS:

   ```bash
   brew install terminal-notifier
   ```

2. Linux:
   ```bash
   sudo apt update
   sudo apt install -y libnotify-bin xdg-utils
   ```

#### Python Dependencies

1. Install required package:
   ```bash
   python3 -m pip install --user tqdm
   ```

#### Script Installation

1. Create installation directory:

   ```bash
   mkdir -p ~/.local/bin
   ```

2. Make script executable and install:

   ```bash
   chmod +x main.py
   cp main.py ~/.local/bin/ywfm
   ```

3. Add to PATH (if not already added):
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # or ~/.zshrc
   source ~/.bashrc  # or ~/.zshrc
   ```
   </details>

## Usage

```bash
ywfm [-h] [-s SUBJECT] [-m MESSAGE] -t TIMER [-o OPEN_URL] [-c COMMAND] [-p] [-b]
```

### Options

| Option                 | Description                              | Default      |
| ---------------------- | ---------------------------------------- | ------------ |
| `-s` `--subject`       | Subject for the reminder notification    | "ywfm"       |
| `-m` `--message`       | Message for the notification             | Random\*     |
| `-t` `--timer`         | Timer duration (e.g., `1h10m15s`, `10s`) | **Required** |
| `-o` `--open-url`      | URL to open when notification triggers   | None         |
| `-c` `--command`       | Command to execute after timer ends      | None         |
| `-p` `--show-progress` | Show progress bar                        | False        |
| `-b` `--background`    | Run as background process                | False        |

\* Default messages alternate between "Well done!" and "You're welcome!"

### Examples

1. **Simple Reminder**:

   ```bash
   ywfm -t 30m -s "Time to Work" -m "Start your project"
   ```

2. **Open URL on Timer**:

   ```bash
   ywfm -t 10s -s "Check GitHub" -m "Review PRs" -o "https://github.com"
   ```

3. **Execute Command**:

   ```bash
   ywfm -t 1m -s "Build" -c 'make clean && make'
   ```

4. **Background Process with Logging**:

   ```bash
   ywfm -t 2h -s "Long Task" -b
   ```

   Output:

   ```json
   {
     "pid": 12345,
     "main": {
       "subject": "Long Task",
       "message": "Well done!",
       "duration": "2h",
       "url": null,
       "command": null,
       "show-progress": false,
       "background": true,
       "created_at": "2024-03-21_14:30:00",
       "trigger_at": "2024-03-21_16:30:00"
     },
     "extra": {
       "os_name": "Darwin",
       "machine": "x86_64",
       "node": "Sanghun.local",
       "platform": "macOS-14.7-x86_64-i386-64bit",
       "seconds": 7200,
       "description": "[INFO] Output and error message of background process are stored in '~/.local/state/ywfm'."
     }
   }
   ```

5. **Progress Bar**:
   ```bash
   ywfm -t 10m -s "Break" -m "Coffee time!" -p
   ```

## Background Process Management

When running in background mode (`-b`):

- Process ID (PID) is output in JSON format
- Logs are stored in `~/.local/state/ywfm/`:
  - `output_[timestamp].log`: Standard output
  - `error_[timestamp].log`: Error messages
  - `ywfm.pid`: Current process PID

To stop a background reminder:

```bash
kill $(cat ~/.local/state/ywfm/ywfm.pid)
```

## Uninstallation

1. Remove the executable:

   ```bash
   rm ~/.local/bin/ywfm
   ```

2. Optional: Remove log directory:

   ```bash
   rm -rf ~/.local/state/ywfm
   ```

3. Optional: Remove dependencies:
   - macOS: `brew uninstall terminal-notifier`
   - Linux: `sudo apt remove libnotify-bin xdg-utils`

## Contributing

Feel free to fork the repository and submit pull requests for improvements.

## License

This project is licensed under the MIT License.

## Author

Sanghun Park

---

> Thank you, past me.
>
> _Good job, future me._
>
> Well done, past me.
>
> _You're welcome, future me._
>
> Thanks a lot.
