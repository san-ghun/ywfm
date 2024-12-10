#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil

# Variables
HOME_PATH = os.path.expanduser("~")
INSTALL_DIR = os.path.join(HOME_PATH, ".local/bin")
SCRIPT_NAME = "reminder.py"
EXECUTABLE_NAME = "reminder"

def check_command(command):
    """Check if a command is available on the system."""
    return shutil.which(command) is not None

def install_dependencies():
    """Install platform-specific dependencies with error handling."""
    print("Checking dependencies...")
    try:
        if sys.platform == "darwin":  # macOS
            if not check_command("terminal-notifier"):
                if check_command("brew"):
                    print("Installing terminal-notifier via Homebrew...")
                    subprocess.run(["brew", "install", "terminal-notifier"], check=True)
                else:
                    print("Error: Homebrew is not installed. Please install Homebrew first from https://brew.sh/")
                    sys.exit(1)
            else:
                print("terminal-notifier is already installed.")
        elif sys.platform.startswith("linux"):  # Linux
            if not check_command("notify-send"):
                print("Installing notify-send...")
                if check_command("sudo"):
                    subprocess.run(["sudo", "apt", "update"], check=True)
                    subprocess.run(["sudo", "apt", "install", "-y", "libnotify-bin"], check=True)
                else:
                    print("Error: 'sudo' is required for apt installation. Please run this script as a privileged user.")
                    sys.exit(1)
            else:
                print("notify-send is already installed.")

            if not check_command("xdg-open"):
                print("Installing xdg-utils...")
                if check_command("sudo"):
                    subprocess.run(["sudo", "apt", "install", "-y", "xdg-utils"], check=True)
                else:
                    print("Error: 'sudo' is required for apt installation. Please run this script as a privileged user.")
                    sys.exit(1)
            else:
                print("xdg-utils is already installed.")
        else:
            print(f"Unsupported OS: {sys.platform}")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during dependency installation: {e}")
        sys.exit(1)

def install_script():
    """Install the reminder script to a directory in PATH."""
    script_path = os.path.join(os.getcwd(), SCRIPT_NAME)
    if not os.path.exists(script_path):
        print(f"Error: {SCRIPT_NAME} not found in the current directory.")
        sys.exit(1)

    destination = os.path.join(INSTALL_DIR, EXECUTABLE_NAME)
    print(f"Installing {SCRIPT_NAME} to {destination}...")

    # Ensure the install directory exists
    os.makedirs(INSTALL_DIR, exist_ok=True)

    # Make the script executable
    os.chmod(script_path, 0o755)

    # Copy the script to the target directory
    try:
        shutil.copy(script_path, destination)
        print(f"{EXECUTABLE_NAME} installed successfully to {INSTALL_DIR}.")
        print(f"Ensure {INSTALL_DIR} is in your PATH environment variable.")
    except PermissionError:
        print("Permission denied. Please ensure you have write permissions to the installation directory.")
        sys.exit(1)

def main():
    print("Reminder Installation Script")
    print("============================")

    # Check and install dependencies
    install_dependencies()

    # Install the script
    install_script()

    print("\nInstallation complete. You can now use the 'reminder' command!")

if __name__ == "__main__":
    main()
