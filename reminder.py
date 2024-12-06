#!/usr/bin/env python3
"""
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
"""
import argparse
import platform
import subprocess
import time
import re
import sys

def parse_timer(timer_str):
    """Parse the timer string (e.g., '1h10m15s') and convert to seconds."""
    pattern = r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?'
    match = re.fullmatch(pattern, timer_str)
    if not match:
        raise ValueError(f"Invalid timer format: {timer_str}")
    hours, minutes, seconds = (int(v) if v else 0 for v in match.groups())
    return hours * 3600 + minutes * 60 + seconds

def send_notification(title, subtitle, open_url, os_name):
    """Send a notification using the appropriate tool for the OS."""
    if os_name == "Darwin": # macOS
        cmd = [
            "terminal-notifier",
            "-title", title,
            "-message", subtitle
        ]
        if open_url:
            cmd.extend(["-open", open_url])
    elif os_name == "Linux":
        message = f"{title}\n{subtitle}" if subtitle else title
        cmd = ["notify-send", title, subtitle]
    else:
        raise OSError(f"Unsupported OS: {os_name}")
    
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError as e:
        print(f"Notification tool not found: {e}. Please ensure terminal-notifier or notify-send is installed.")
        sys.exit(1)

def execute_command(command):
    """Execute the specified command."""
    if command:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute command: {e}")

def main():
    parser = argparse.ArgumentParser(description="CLI Reminder tool with notifications.")
    parser.add_argument("--title", required=True, help="Title for the reminder notification.")
    parser.add_argument("--subtitle", help="Subtitle for the reminder notification.")
    parser.add_argument("--open", help="URL to open with the notification.")
    parser.add_argument("--command", help="Command to exeute after the timer.")
    parser.add_argument("--timer", help="Timer duration (e.g., '1h10m15s').")

    args = parser.parse_args()

    os_name = platform.system()

    try:
        if args.timer:
            wait_time = parse_timer(args.timer)
        else:
            wait_time = 15 * 60
    except ValueError as e:
        print(e)
        sys.exit(1)

    
    print(f"Reminder set! Waiting for {wait_time} seconds...")
    time.sleep(wait_time)

    send_notification(args.title, args.subtitle or "", args.open, os_name)
    if args.command:
        execute_command(args.command)

if __name__ == "__main__":
    main()
