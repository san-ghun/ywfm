#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
from typing import Dict, List, Optional, Tuple

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

# Package manager configurations for Linux
PACKAGE_MANAGERS: Dict[str, Dict] = {
    "apt": {
        "check": "apt",
        "update": ["sudo", "apt", "update"],
        "install": ["sudo", "apt", "install", "-y"],
        "packages": {
            "notify-send": "libnotify-bin",
            "xdg-open": "xdg-utils"
        }
    },
    "dnf": {
        "check": "dnf",
        "update": None,
        "install": ["sudo", "dnf", "install", "-y"],
        "packages": {
            "notify-send": "libnotify",
            "xdg-open": "xdg-utils"
        }
    },
    "yum": {
        "check": "yum",
        "update": None,
        "install": ["sudo", "yum", "install", "-y"],
        "packages": {
            "notify-send": "libnotify",
            "xdg-open": "xdg-utils"
        }
    },
    "pacman": {
        "check": "pacman",
        "update": ["sudo", "pacman", "-Sy"],
        "install": ["sudo", "pacman", "-S", "--noconfirm"],
        "packages": {
            "notify-send": "libnotify",
            "xdg-open": "xdg-utils"
        }
    },
    "zypper": {
        "check": "zypper",
        "update": ["sudo", "zypper", "refresh"],
        "install": ["sudo", "zypper", "install", "-y"],
        "packages": {
            "notify-send": "libnotify-tools",
            "xdg-open": "xdg-utils"
        }
    },
}

# Manual installation instructions
MANUAL_INSTALL: Dict[str, Dict[str, str]] = {
    "notify-send": {
        "debian/ubuntu": "sudo apt install libnotify-bin",
        "fedora/rhel": "sudo dnf install libnotify",
        "arch": "sudo pacman -S libnotify",
        "opensuse": "sudo zypper install libnotify-tools",
    },
    "xdg-open": {
        "debian/ubuntu": "sudo apt install xdg-utils",
        "fedora/rhel": "sudo dnf install xdg-utils",
        "arch": "sudo pacman -S xdg-utils",
        "opensuse": "sudo zypper install xdg-utils",
    },
}

def check_command(command: str) -> bool:
    """Check if a command is available on the system."""
    return shutil.which(command) is not None


def detect_package_manager() -> Tuple[Optional[str], Optional[Dict]]:
    """Detect the system's package manager."""
    for pm_name, pm_config in PACKAGE_MANAGERS.items():
        if check_command(pm_config["check"]):
            return pm_name, pm_config
    return None, None


def show_manual_instructions(deps: List[str]) -> None:
    """Show manual installation instructions for missing dependencies."""
    print("\n" + "=" * 60)
    print("MANUAL INSTALLATION REQUIRED")
    print("=" * 60)
    print("\nCould not auto-install dependencies. Please install manually:\n")

    for dep in deps:
        if dep in MANUAL_INSTALL:
            print(f"  {dep}:")
            for distro, cmd in MANUAL_INSTALL[dep].items():
                print(f"    {distro:15} {cmd}")
            print()

    print("After installing, run this script again.")
    print("=" * 60 + "\n")


def is_package_installed(package_name: str) -> bool:
    """Check if a given package is installed in the system."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "show", package_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

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

def list_missing_packages():
    """List Python packages that are missing for the current platform."""
    missing_packages = []
    for pkg in PYTHON_REQUIREMENTS:
        if not is_package_installed(pkg):
            missing_packages.append(pkg)
    return missing_packages

def install_linux_dependency(dep: str, pm_name: str, pm_config: Dict) -> bool:
    """Install a single Linux dependency using the detected package manager."""
    package = pm_config["packages"].get(dep)
    if not package:
        print(f"  Unknown package mapping for '{dep}' on {pm_name}")
        return False

    print(f"  Installing {package} via {pm_name}...")

    try:
        # Update package list if needed
        if pm_config["update"]:
            subprocess.run(pm_config["update"], check=True)

        # Install package
        install_cmd = pm_config["install"] + [package]
        subprocess.run(install_cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Failed to install {package}: {e}")
        return False


def install_dependencies():
    """Install platform-specific dependencies with user confirmation."""
    print("Checking dependencies...")
    missing_deps = list_missing_dependencies()
    if not missing_deps:
        print("All required dependencies are already installed.")
        return

    print("\nThe following dependencies are missing:")
    for dep in missing_deps:
        print(f"  - {dep}")

    if sys.platform == "darwin":
        if not check_command("brew"):
            print("\nError: Homebrew is not installed.")
            print("Please install Homebrew first from https://brew.sh/")
            sys.exit(1)
        print("\nWill install via Homebrew.")

    elif sys.platform.startswith("linux"):
        pm_name, pm_config = detect_package_manager()
        if pm_name:
            print(f"\nDetected package manager: {pm_name}")
        else:
            print("\nCould not detect package manager.")
            show_manual_instructions(missing_deps)
            sys.exit(1)

        if not check_command("sudo"):
            print("\nError: 'sudo' is required for package installation.")
            show_manual_instructions(missing_deps)
            sys.exit(1)

    if not prompt_user("\nWould you like to proceed with the installation?"):
        print("Installation aborted by the user.")
        sys.exit(0)

    failed_deps = []

    try:
        if sys.platform == "darwin":
            for dep in missing_deps:
                if dep == "terminal-notifier":
                    print(f"\nInstalling {dep} via Homebrew...")
                    subprocess.run(["brew", "install", dep], check=True)

        elif sys.platform.startswith("linux"):
            pm_name, pm_config = detect_package_manager()
            for dep in missing_deps:
                print(f"\nInstalling {dep}...")
                if not install_linux_dependency(dep, pm_name, pm_config):
                    failed_deps.append(dep)

    except subprocess.CalledProcessError as e:
        print(f"\nError during installation: {e}")
        failed_deps = missing_deps

    if failed_deps:
        show_manual_instructions(failed_deps)
        sys.exit(1)

def install_python_libraries():
    """Install Python libraries required by the script."""
    print("Checking Python libraries...")
    missing_pkgs = list_missing_packages()
    if not missing_pkgs:
        print("All required Python libraries are already installed.")
        return

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
        print(f"Error occurred while installing Python libraries: {e}")
        sys.exit(1)

def install_script():
    """Install the reminder script to a directory in PATH."""
    script_path = os.path.join(os.getcwd(), f"src/{SCRIPT_NAME}")
    if not os.path.exists(script_path):
        print(f"Error: {SCRIPT_NAME} not found in the source directory.")
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
