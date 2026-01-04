# Platform Limitation Improvements

> **Status: ✅ COMPLETED**
>
> Multi-distro support implemented in commit `528f72b`
> Supports: apt, dnf, yum, pacman, zypper

Installer improvements for broader Linux distribution support.

## Current Limitation

**Location:** `install.py:93-109`

**Problem:**
The installer assumes `apt` package manager for all Linux distributions:

```python
elif sys.platform.startswith("linux"):
    if "notify-send" in missing_deps:
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "libnotify-bin"], check=True)
```

This fails on:
- Fedora/RHEL/CentOS (`dnf`/`yum`)
- Arch Linux (`pacman`)
- openSUSE (`zypper`)
- Alpine (`apk`)
- Gentoo (`emerge`)

---

## Proposed Solution

### Option A: Detect Package Manager (Recommended)

```python
PACKAGE_MANAGERS = {
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
        "update": None,  # dnf auto-updates metadata
        "install": ["sudo", "dnf", "install", "-y"],
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
    }
}

def detect_package_manager():
    """Detect the system's package manager."""
    for pm_name, pm_config in PACKAGE_MANAGERS.items():
        if check_command(pm_config["check"]):
            return pm_name, pm_config
    return None, None

def install_linux_dependency(dep: str):
    """Install a dependency using the detected package manager."""
    pm_name, pm_config = detect_package_manager()

    if pm_name is None:
        print(f"Error: Could not detect package manager.")
        print(f"Please install '{dep}' manually.")
        return False

    package = pm_config["packages"].get(dep)
    if not package:
        print(f"Error: Unknown package for '{dep}' on {pm_name}")
        return False

    print(f"Installing {package} via {pm_name}...")

    # Update package list if needed
    if pm_config["update"]:
        subprocess.run(pm_config["update"], check=True)

    # Install package
    install_cmd = pm_config["install"] + [package]
    subprocess.run(install_cmd, check=True)

    return True
```

### Option B: Manual Installation Fallback

If package manager detection fails, provide clear instructions:

```python
MANUAL_INSTRUCTIONS = {
    "notify-send": {
        "debian": "sudo apt install libnotify-bin",
        "fedora": "sudo dnf install libnotify",
        "arch": "sudo pacman -S libnotify",
        "manual": "Install libnotify from your distribution's package manager"
    },
    "xdg-open": {
        "debian": "sudo apt install xdg-utils",
        "fedora": "sudo dnf install xdg-utils",
        "arch": "sudo pacman -S xdg-utils",
        "manual": "Install xdg-utils from your distribution's package manager"
    }
}

def show_manual_instructions(dep: str):
    """Show manual installation instructions."""
    print(f"\nCould not auto-install '{dep}'. Please install manually:")
    print("-" * 50)
    for distro, cmd in MANUAL_INSTRUCTIONS[dep].items():
        print(f"  {distro:10}: {cmd}")
    print("-" * 50)
```

---

## Implementation Steps

1. Add `PACKAGE_MANAGERS` dictionary with package manager configurations
2. Implement `detect_package_manager()` function
3. Refactor `install_dependencies()` to use new detection
4. Add fallback with manual instructions
5. Test on multiple distributions (Docker containers)

---

## Testing Matrix

| Distribution | Package Manager | notify-send package | xdg-utils package |
|--------------|-----------------|---------------------|-------------------|
| Ubuntu/Debian | apt | libnotify-bin | xdg-utils |
| Fedora | dnf | libnotify | xdg-utils |
| Arch | pacman | libnotify | xdg-utils |
| openSUSE | zypper | libnotify-tools | xdg-utils |
| Alpine | apk | libnotify | xdg-utils |

---

## Alternative: Remove Auto-Install

A simpler approach is to remove auto-installation entirely and only provide detection + instructions:

```python
def check_dependencies():
    """Check for required dependencies and provide installation guidance."""
    missing = list_missing_dependencies()

    if not missing:
        print("All dependencies satisfied.")
        return True

    print("Missing dependencies detected:")
    for dep in missing:
        print(f"  - {dep}")

    print("\nInstallation instructions:")
    show_manual_instructions_for_all(missing)

    return False
```

This approach:
- Avoids complexity of supporting many package managers
- Reduces risk of installation errors
- Gives users control over their system
- Works on any Linux distribution
