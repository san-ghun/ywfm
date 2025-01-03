#!/usr/bin/env python3
"""
- Python3 script file to execute and work as reminder, target OS for macOS and Linux.
- The program will use `terminal-notifier` for macOS and `notify-send` for Linux.
- The program will take options,
    - `--title <string>`
    - `--body <string>`
    - `--open <URL>`
    - `--command <string>`
    - `--timer <string>`
    - `--background`
    - `--show-progress`


- An example command would be like this:
    ```bash
    > reminder --title "Start building" --body "github auth feat" --open "https://github.com/" --command 'echo hello' --timer 1h10m15s --background
    > reminder --title "Break time" --body "10-minute break" --open "https://youtube.com/" --command 'echo yeah' --timer 10m --show-progress
    ```
"""
import argparse
import platform
import subprocess
import time
import re
import os
import sys
from tqdm import tqdm

def parse_timer(timer_str):
    """Parse the timer string (e.g., '1h10m15s') and convert to seconds."""
    pattern = r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?'
    match = re.fullmatch(pattern, timer_str)
    if not match:
        raise ValueError(f"Invalid timer format: {timer_str}")
    hours, minutes, seconds = (int(v) if v else 0 for v in match.groups())
    return hours * 3600 + minutes * 60 + seconds

def send_notification(title, body, open_url, os_name):
    """Send a notification using the appropriate tool for the OS."""
    if os_name == "Darwin": # macOS
        cmd = [
            "terminal-notifier",
            "-sound", "default",
            "-title", title,
            "-message", body
        ]
        if open_url:
            cmd.extend(["-open", open_url])
    elif os_name == "Linux":
        cmd = ["notify-send", title]
        if body:
            cmd.append(body)
        try:
            subprocess.run(cmd, check=True)
            if open_url:
                subprocess.run(["xdg-open", open_url], check=True)
        except FileNotFoundError as e:
            print(f"Notification tool or xdg-open not found: {e}. Please ensure notify-send and xdg-utils are installed.")
            sys.exit(1)
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

def run_reminder(title, body, open_url, command, timer, show_progress):
    msgs = [f"Well done!", f"You're welcome!"]
    os_name = platform.system()

    try:
        if timer:
            wait_time = parse_timer(timer)
        else:
            wait_time = 15 * 60
    except ValueError as e:
        print(e)
        sys.exit(1)

    if show_progress:
        print(f"Starting timer for {timer}...")
        for _ in tqdm(range(wait_time), desc="Progress", ncols=80, unit="s"):
            time.sleep(1)
        print(msgs[0] if wait_time % 2 else msgs[1])
    else:
        time.sleep(wait_time)

    send_notification(title, body or "", open_url, os_name)
    if command:
        execute_command(command)

def main():
    parser = argparse.ArgumentParser(description="CLI Reminder tool with notifications.")
    parser.add_argument("--title", required=True, help="Title for the reminder notification.")
    parser.add_argument("--body", help="Body for the reminder notification.")
    parser.add_argument("--open", help="URL to open with the notification.")
    parser.add_argument("--command", help="Command to exeute after the timer.")
    parser.add_argument("--timer", help="Timer duration (e.g., '1h10m15s').")
    parser.add_argument("--background", action="store_true", help="Run the reminder in the background.")
    parser.add_argument("--show-progress", action="store_true", help="Show a progress bar for the countdown.")

    args = parser.parse_args()

    if args.background:
        pid = os.fork()
        if pid > 0:
            print(f"Reminder running in background with PID {pid}.")
            sys.exit(0)

    run_reminder(args.title, args.body, args.open, args.command, args.timer, args.show_progress)

if __name__ == "__main__":
    main()
