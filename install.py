#!/usr/bin/env python3

import os
import sys
import subprocess
import shutil

# Variables
HOME_PATH = os.path.expanduser("~")
INSTALL_DIR = os.path.join(HOME_PATH, ".local/bin")
SCRIPT_NAME = "main.py"
EXECUTABLE_NAME = "ywfm"
PYTHON_REQUIREMENTS = ["tqdm"]

DEPENDENCIES = {
    "darwin": ["terminal-notifier"],
    "linux": ["notify-send", "xdg-open"]
}

def check_command(command):
    """Check if a command is available on the system."""
    return shutil.which(command) is not None

def prompt_user(message):
    """Prompt the user with a yes/no question."""
    while True:
        response = input(f"{message} [y/n]: ").strip().lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def list_missing_dependencies():
    """List dependencies that are missing for the current platform."""
    os_type = sys.platform
    missing_dependencies = []
    if os_type == "darwin":
        for dep in DEPENDENCIES["darwin"]:
            if not check_command(dep):
                missing_dependencies.append(dep)
    elif os_type.startswith("linux"):
        for dep in DEPENDENCIES["linux"]:
            if not check_command(dep):
                missing_dependencies.append(dep)
    else:
        print(f"Unsupported OS: {sys.platform}")
        sys.exit(1)
    return missing_dependencies

def install_dependencies():
    """Install platform-specific dependencies with user confirmation."""
    print("Checking dependencies...")
    missing_deps = list_missing_dependencies()
    if not missing_deps:
        print("All required dependencies are already installed.")
        return
    
    print("The following dependencies are missing and will be installed:")
    for dep in missing_deps:
        print(f"- {dep}")
    
    if not prompt_user("Would you like to proceed with the installation?"):
        print("Installation aborted by the user.")
        sys.exit(0)

    try:
        if sys.platform == "darwin":  # macOS
            if "terminal-notifier" in missing_deps:
                if check_command("brew"):
                    print("Installing terminal-notifier via Homebrew...")
                    subprocess.run(["brew", "install", "terminal-notifier"], check=True)
                else:
                    print("Error: Homebrew is not installed. Please install Homebrew first from https://brew.sh/")
                    sys.exit(1)
        elif sys.platform.startswith("linux"):  # Linux
            if "notify-send" in missing_deps:
                print("Installing notify-send...")
                if check_command("sudo"):
                    subprocess.run(["sudo", "apt", "update"], check=True)
                    subprocess.run(["sudo", "apt", "install", "-y", "libnotify-bin"], check=True)
                else:
                    print("Error: 'sudo' is required for apt installation. Please run this script as a privileged user.")
                    sys.exit(1)

            if "xdg-open" in missing_deps:
                print("Installing xdg-utils...")
                if check_command("sudo"):
                    subprocess.run(["sudo", "apt", "install", "-y", "xdg-utils"], check=True)
                else:
                    print("Error: 'sudo' is required for apt installation. Please run this script as a privileged user.")
                    sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during dependency installation: {e}")
        sys.exit(1)

def install_python_libraries():
    """Install Python libraries required by the script."""
    print("Checking Python libraries...")
    print("The following Python libraries are required:")
    for lib in PYTHON_REQUIREMENTS:
        print(f"- {lib}")

    if not prompt_user("Would you like to install these libraries?"):
        print("Python library installation aborted by the user.")
        return

    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--user"] + PYTHON_REQUIREMENTS, check=True)
        print("Python libraries installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installiing Python libraries: {e}")
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
        print(f"Ensure the following directory is in your PATH environment variable:")
        print(f"\t{INSTALL_DIR}")
        print(f"if not, you can do by adding the following line of code into your .bashrc or .zshrc file:")
        print(f"\texport PATH=\"$HOME/.local/bin:$PATH\"")
    except PermissionError:
        print("Permission denied. Please ensure you have write permissions to the installation directory.")
        sys.exit(1)

def main():
    print("'ywfm' Installation Script")
    print("============================")

    # Check and install platform-specific dependencies
    install_dependencies()

    # Check and install Python libraries
    install_python_libraries()

    # Install the script
    install_script()

    print("\nInstallation complete. You can now use the 'ywfm' command!")

if __name__ == "__main__":
    main()
