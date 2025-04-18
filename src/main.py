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
    - `--background`
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
from typing import Optional
from dataclasses import dataclass

@dataclass
class ReminderConfig:
    NAME = "ywfm"
    MIN_TIME = 15
    
    subject: str = None
    message: Optional[str] = None
    timer: Optional[str] = None
    open_url: Optional[str] = None
    command: Optional[str] = None
    show_progress: bool = False
    background: bool = False
    created_at: str = None
    trigger_at: str = None
    description: str = ""
    time_limit: bool = False

    def __post_init__(self):
        if self.subject is None:
            self.subject = self.NAME
        self.created_at = time.strftime("%Y-%m-%d_%H:%M:%S")
        self.trigger_at = time.strftime(
            "%Y-%m-%d_%H:%M:%S", 
            time.localtime(time.time() + self.wait_time)
        )

    @property
    def wait_time(self) -> int:
        if not self.timer:
            self.timer = f"{self.MIN_TIME}m"
        total_seconds = self.parse_timer(self.timer)
        if total_seconds < self.MIN_TIME:
            self.time_limit = True
            total_seconds = self.MIN_TIME
        return total_seconds

    @staticmethod
    def parse_timer(timer_str: str) -> int:
        pattern = r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?'
        match = re.fullmatch(pattern, timer_str)
        if not match:
            raise ValueError(f"Invalid timer format: {timer_str}")
        hours, minutes, seconds = (int(v) if v else 0 for v in match.groups())
        return hours * 3600 + minutes * 60 + seconds

class NotificationManager:
    def __init__(self, os_name: str):
        self.os_name = os_name
        if os_name not in ["Darwin", "Linux"]:
            raise OSError(f"Unsupported OS: {os_name}")

    def send(self, subject: str, message: str, open_url: Optional[str]):
        if self.os_name == "Darwin":
            self._send_macos(subject, message, open_url)
        else:
            self._send_linux(subject, message, open_url)

    def _send_macos(self, subject: str, message: str, open_url: Optional[str]):
        cmd = [
            "terminal-notifier",
            "-sound", "default",
            "-title", subject,
            "-message", message
        ]
        self._run_command(cmd)

        if open_url:
            self._run_command(["open", open_url])

    def _send_linux(self, subject: str, message: str, open_url: Optional[str]):
        cmd = ["notify-send", subject]
        if message:
            cmd.append(message)
        self._run_command(cmd)
        
        if open_url:
            self._run_command(["xdg-open", open_url])

    def _run_command(self, cmd: list):
        try:
            subprocess.run(cmd, check=True)
        except FileNotFoundError as e:
            print(f"Command not found: {e}", file=sys.stderr)
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}", file=sys.stderr)
            sys.exit(1)

class Reminder:
    def __init__(self, config: ReminderConfig):
        self.config = config
        self.os_name = platform.system()
        self.notifier = NotificationManager(self.os_name)
        self.messages = ["Well done!", "You're welcome!"]

    def run(self):
        info = ""
        if not self.config.message:
            self.config.message = self.messages[0] if self.config.wait_time % 2 else self.messages[1]
        if self.config.time_limit:
            info += f"[INFO] Given timer value is too small, applying MIN_TIME {self.config.MIN_TIME} seconds.\n"
            self.config.description += info

        if self.config.background:
            self._run_background()
        else:
            print(info, file=sys.stdout)
            self._run_foreground()

    def _run_background(self):
        log_dir = os.path.join(os.path.expanduser("~"), ".local", "state", self.config.NAME)
        os.makedirs(log_dir, exist_ok=True)
        stdout_path = os.path.join(log_dir, f"output_{self.config.created_at}.log")
        stderr_path = os.path.join(log_dir, f"error_{self.config.created_at}.log")
        
        if self.os_name in ["Linux", "Darwin"]:
            self.config.description += f"[INFO] Output and error message of background process are stored in '{log_dir}'.\n"
            self.daemonize()
            
            pid = str(os.getpid())
            pid_file = os.path.join(log_dir, "ywfm.pid")
            with open(pid_file, 'w') as f:
                f.write(pid)

            json_file = os.path.join(log_dir, f"{self.config.created_at}.json")
            with open(json_file, 'w') as f:
                f.write(json.dumps(self._json_output(os.getpid()), indent=4) + "\n")

            with open(stdout_path, 'w') as stdout_file:
                os.dup2(stdout_file.fileno(), sys.stdout.fileno())
                stdout_file.write(f"pid: {pid}\n")
                stdout_file.write("created_at: " + self.config.created_at + "\n")
                stdout_file.write("trigger_at: " + self.config.trigger_at + "\n")
                stdout_file.write("---\n")
            with open(stderr_path, 'w') as stderr_file:
                os.dup2(stderr_file.fileno(), sys.stderr.fileno())
                stderr_file.write(f"pid: {pid}\n")
                stderr_file.write("created_at: " + self.config.created_at + "\n")
                stderr_file.write("trigger_at: " + self.config.trigger_at + "\n")
                stderr_file.write("---\n")

            time.sleep(self.config.wait_time)
            self.notifier.send(self.config.subject, self.config.message, self.config.open_url)
            if self.config.command:
                self._execute_command()
        else:
            pass


    def _run_foreground(self):
        output = self._json_output(os.getpid())
        print(json.dumps(output, indent=4) + '\n')
        sys.stdout.flush()
        if self.config.show_progress:
            self._run_with_progress()
        else:
            time.sleep(self.config.wait_time)

        self.notifier.send(self.config.subject, self.config.message, self.config.open_url)
        if self.config.command:
            self._execute_command()

    def _run_with_progress(self):
        try:
            from tqdm import tqdm
        except ImportError:
            print("tqdm library required for progress bar. Install with 'pip install tqdm'", 
                  file=sys.stderr)
            sys.exit(1)

        print(f"Starting timer for {self.config.timer}...")
        for _ in tqdm(range(self.config.wait_time), desc="Progress", ncols=80, unit="s"):
            time.sleep(1)

    def _execute_command(self):
        try:
            subprocess.run(self.config.command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}", file=sys.stderr)
            sys.exit(1)

    def daemonize(self):
        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError as err:
            print(f'Fork #1 failed: {err}', file=sys.stderr)
            sys.exit(1)

        os.setsid()
        os.chdir('/')
        os.umask(0)

        try:
            pid = os.fork()
            if pid > 0:
                output = self._json_output(pid)
                print(json.dumps(output))
                sys.stdout.flush()
                sys.exit(0)
        except OSError as err:
            print(f'Fork #2 failed: {err}', file=sys.stderr)
            sys.exit(1)

        for fd in range(0, 1024):
            try:
                os.close(fd)
            except OSError:
                pass

        sys.stdout.flush()
        sys.stderr.flush()
        with open(os.devnull, 'r') as f:
            os.dup2(f.fileno(), sys.stdin.fileno())

    def _json_output(self, pid: int):
        data = {
            "pid": pid,
            "params": {
                "subject": self.config.subject,
                "message": self.config.message,
                "duration": self.config.timer,
                "url": self.config.open_url,
                "command": self.config.command,
                "show-progress": self.config.show_progress,
                "background": self.config.background,
            },
            "info": {
                "created_at": self.config.created_at,
                "trigger_at": self.config.trigger_at,
                "seconds": self.config.wait_time,
            },
            "extra": {
                "os_name": self.os_name,
                "machine": platform.machine(),
                "node": platform.node(),
                "platform": platform.platform(),
                "description": self.config.description,
            }
        }
        return data

def main():
    parser = argparse.ArgumentParser(description="CLI Reminder tool with notifications.")
    parser.add_argument("-s", "--subject", default="ywfm", help="Subject for the reminder notification.")
    parser.add_argument("-m", "--message", help="Message for the reminder notification.")
    parser.add_argument("-t", "--timer", required=True, help="Timer duration. (e.g., '1h10m15s')")
    parser.add_argument("-o", "--open-url", help="URL to open with the notification.")
    parser.add_argument("-c", "--command", help="Command to execute after the timer.")
    parser.add_argument("-p", "--show-progress", action="store_true", help="Show a progress bar.")
    parser.add_argument("-b", "--background", action="store_true", help="Run in background.")

    args = parser.parse_args()
    config = ReminderConfig(
        subject=args.subject,
        message=args.message,
        timer=args.timer,
        open_url=args.open_url,
        command=args.command,
        show_progress=args.show_progress,
        background=args.background
    )
    
    reminder = Reminder(config)
    reminder.run()

if __name__ == "__main__":
    main()
