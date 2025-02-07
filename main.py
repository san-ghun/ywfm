#!/usr/bin/env python3
"""
- Python3 script file to execute and work as reminder, target OS for macOS and Linux.
- The program will use `terminal-notifier` for macOS and `notify-send` for Linux.
- The program will take options,
    - `--subject <string>`
    - `--message <string>`
    - `--timer <string>`
    - `--open-url <URL>`
    - `--command <string>`
    - `--background` or simply `&`
    - `--show-progress`


- An example command would be like this:
    ```bash
    > reminder --subject "Start building" --message "github auth feat" --open-url "https://github.com/" --command 'echo hello' --timer 1h10m15s --background
    > reminder --subject "Break time" --message "10-minute break" --open-url "https://youtube.com/" --command 'echo yeah' --timer 10m --show-progress
    ```
"""
import argparse
import platform
import subprocess
import time
import re
import os
import sys
import json

NAME = f"ywfm"
TIME = 15

def parse_timer(timer_str):
    """Parse the timer string (e.g., '1h10m15s') and convert to seconds."""
    pattern = r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?'
    match = re.fullmatch(pattern, timer_str)
    if not match:
        raise ValueError(f"Invalid timer format: {timer_str}")
    hours, minutes, seconds = (int(v) if v else 0 for v in match.groups())
    return hours * 3600 + minutes * 60 + seconds

def send_notification(subject, message, open_url, os_name):
    """Send a notification using the appropriate tool for the OS."""
    if os_name == "Darwin": # macOS
        cmd = [
            "terminal-notifier",
            "-sound", "default",
            "-title", subject,
            "-message", message
        ]
        if open_url:
            cmd.extend(["-open", open_url])
        try:
            subprocess.run(cmd, check=True)
        except FileNotFoundError as e:
            print(f"Notification tool not found: {e}. Please ensure terminal-notifier is installed.")
            sys.exit(1)
    elif os_name == "Linux":
        cmd = ["notify-send", subject]
        if message:
            cmd.append(message)
        try:
            subprocess.run(cmd, check=True)
        except FileNotFoundError as e:
            print(f"Notification tool not found: {e}. Please ensure notify-send is installed.")
            sys.exit(1)
        if open_url:
            try:
                subprocess.run(["xdg-open", open_url], check=True)
            except FileNotFoundError as e:
                print(f"Notification tool or xdg-open not found: {e}. Please ensure xdg-utils is installed.")
                sys.exit(1)
    else:
        raise OSError(f"Unsupported OS: {os_name}")

def execute_command(command):
    """Execute the specified command."""
    if command:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute command: {e}")

def run_reminder(subject, message, timer, open_url, command, show_progress, background):
    os_name = platform.system()
    description = f""
    if not timer:
        timer = f"{TIME}m"
        description = f"[ERROR] No timer value provided\n"
    try:
        wait_time = parse_timer(timer)
    except ValueError as e:
        print(e)
        sys.exit(1)

    msgs = [f"Well done!", f"You're welcome!"]
    msg = msgs[0] if wait_time % 2 else msgs[1]
    if not message:
        message = msg

    if background:
        pid = os.fork()
        if pid > 0:
            description += f"[INFO] Reminder running in background with PID: {pid}\n"
            print(json.dumps(
                {
                    "pid": pid, 
                    "main": {
                        "subject": subject, "message": message,
                        "duration": timer, "url": open_url, "command": command,
                        "show-progress": show_progress, "background": background,
                    },
                    "extra": {
                        "os_name": os_name, "seconds": wait_time,
                        "description": description,
                    },
                },
                indent=None
            ))
            sys.exit(0)

    if show_progress and not background:
        try:
            from tqdm import tqdm
        except ImportError:
            print(f"The tqdm library is required for progress bar functionality. Install it using 'pip install tqdm'.")
            print(f"\tYou can run the \"{NAME}\" without '--show-progress' option.")
            sys.exit(1)
        print(f"Starting timer for {timer}...")
        for _ in tqdm(range(wait_time), desc="Progress", ncols=80, unit="s"):
            time.sleep(1)
        print(msg)
    else:
        time.sleep(wait_time)

    send_notification(subject, message, open_url, os_name)
    if command:
        execute_command(command)

def main():
    parser = argparse.ArgumentParser(description="CLI Reminder tool with notifications.")
    parser.add_argument("-s", "--subject", default=NAME, help="Subject for the reminder notification.")
    parser.add_argument("-m", "--message", help="Message for the reminder notification.")
    parser.add_argument("-t", "--timer", required=True, help="Timer duration. (e.g., '1h10m15s')")
    parser.add_argument("-o", "--open-url", help="URL to open with the notification.")
    parser.add_argument("-c", "--command", help="Command to exeute after the timer.")
    parser.add_argument("-p", "--show-progress", action="store_true", help="Show a progress bar for the countdown.")
    parser.add_argument("-b", "--background", action="store_true", help="Run the reminder in the background.")

    args = parser.parse_args()
    run_reminder(args.subject, args.message, args.timer, args.open_url, args.command, args.show_progress, args.background)

if __name__ == "__main__":
    main()
