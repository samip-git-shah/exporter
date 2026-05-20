#!/usr/bin/env python3
"""
Test Case Exporter - Universal Launcher
Platform-independent launcher that auto-installs dependencies and runs the application.
Supports: Windows, Linux, macOS

Usage: python launch.py (or python3 launch.py)
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
import urllib.request
import tempfile

# Configuration
APP_NAME = "TestCaseExporter"
VENV_DIR = ".venv"
REQUIRED_PACKAGES = [
    "customtkinter",
    "tkcalendar",
    "playwright",
    "python-docx",
    "reportlab"
]
MAIN_PY = "main.py"
REQUIRED_FILES = ["logo.png"]
REQUIREMENTS_TXT = "requirements.txt"

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color=Colors.OKGREEN):
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.ENDC}")

def print_header(message):
    """Print header message"""
    print_colored(f"\n{'='*60}", Colors.HEADER)
    print_colored(f"  {message}", Colors.HEADER + Colors.BOLD)
    print_colored(f"{'='*60}\n", Colors.HEADER)

def get_python_executable():
    """Get the appropriate Python executable for the current platform"""
    if platform.system() == "Windows":
        return "python"
    else:
        # Try python3 first, fallback to python
        if shutil.which("python3"):
            return "python3"
        return "python"

def get_venv_python():
    """Get the Python executable inside the virtual environment"""
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "python")

def get_venv_pip():
    """Get the pip executable inside the virtual environment"""
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    else:
        return os.path.join(VENV_DIR, "bin", "pip")

def check_python_version():
    """Check if Python version is compatible"""
    print_colored("🔍 Checking Python version...", Colors.OKBLUE)
    version = sys.version_info
    print_colored(f"   Python {version.major}.{version.minor}.{version.micro} detected", Colors.OKCYAN)

    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_colored("❌ Python 3.7 or higher is required!", Colors.FAIL)
        sys.exit(1)

    print_colored("✅ Python version compatible", Colors.OKGREEN)
    return True

def create_virtual_environment():
    """Create a virtual environment if it doesn't exist"""
    if os.path.exists(VENV_DIR):
        print_colored("✅ Virtual environment already exists", Colors.OKGREEN)
        return True

    print_colored("📦 Creating virtual environment...", Colors.OKBLUE)
    try:
        python_exe = get_python_executable()
        subprocess.check_call([python_exe, "-m", "venv", VENV_DIR])
        print_colored("✅ Virtual environment created successfully", Colors.OKGREEN)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Failed to create virtual environment: {e}", Colors.FAIL)
        return False
    except Exception as e:
        print_colored(f"❌ Unexpected error: {e}", Colors.FAIL)
        return False

def install_dependencies():
    """Install required dependencies in the virtual environment"""
    print_colored("📥 Installing dependencies...", Colors.OKBLUE)
    pip_exe = get_venv_pip()

    # Upgrade pip first
    try:
        print_colored("   Upgrading pip...", Colors.OKCYAN)
        subprocess.check_call([pip_exe, "install", "--upgrade", "pip"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass  # Non-critical if this fails

    # Install pinned versions from requirements.txt when available, else fall back
    # to installing each package by name.
    if os.path.exists(REQUIREMENTS_TXT):
        try:
            print_colored(f"   Installing from {REQUIREMENTS_TXT}...", Colors.OKCYAN)
            subprocess.check_call([pip_exe, "install", "-r", REQUIREMENTS_TXT],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print_colored(f"   ✅ Dependencies installed from {REQUIREMENTS_TXT}", Colors.OKGREEN)
        except subprocess.CalledProcessError:
            print_colored(f"   ❌ Failed to install from {REQUIREMENTS_TXT}", Colors.FAIL)
            return False
    else:
        for package in REQUIRED_PACKAGES:
            try:
                print_colored(f"   Installing {package}...", Colors.OKCYAN)
                subprocess.check_call([pip_exe, "install", package],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print_colored(f"   ✅ {package} installed", Colors.OKGREEN)
            except subprocess.CalledProcessError as e:
                print_colored(f"   ❌ Failed to install {package}", Colors.FAIL)
                return False

    # Install playwright browsers
    print_colored("   Installing Playwright browsers (this may take a few minutes)...", Colors.OKCYAN)
    try:
        venv_python = get_venv_python()
        subprocess.check_call([venv_python, "-m", "playwright", "install", "chromium"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_colored("   ✅ Playwright browsers installed", Colors.OKGREEN)
    except:
        print_colored("   ⚠️  Playwright browsers installation failed, but continuing...", Colors.WARNING)

    print_colored("✅ All dependencies installed successfully", Colors.OKGREEN)
    return True

def check_required_files():
    """Check if required application files exist"""
    print_colored("📁 Checking required files...", Colors.OKBLUE)

    if not os.path.exists(MAIN_PY):
        print_colored(f"❌ Required file '{MAIN_PY}' not found!", Colors.FAIL)
        print_colored(f"   Please ensure {MAIN_PY} is in the same directory as this launcher.", Colors.WARNING)
        return False

    print_colored(f"   ✅ {MAIN_PY} found", Colors.OKGREEN)

    # Check for resource files (non-critical)
    missing_files = []
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print_colored(f"   ✅ {file} found", Colors.OKGREEN)

    if missing_files:
        print_colored(f"   ⚠️  Optional files missing: {', '.join(missing_files)}", Colors.WARNING)
        print_colored(f"   The application may not work correctly without these files.", Colors.WARNING)

    return True

def check_dependencies_installed():
    """Check if dependencies are already installed in venv"""
    if not os.path.exists(VENV_DIR):
        return False

    pip_exe = get_venv_pip()
    try:
        # Check if all packages are installed
        result = subprocess.run([pip_exe, "list"], capture_output=True, text=True)
        installed_packages = result.stdout.lower()

        for package in REQUIRED_PACKAGES:
            if package.lower() not in installed_packages:
                return False
        return True
    except:
        return False

def run_application():
    """Run the main application"""
    print_colored("🚀 Launching Test Case Exporter...", Colors.OKBLUE)
    venv_python = get_venv_python()

    try:
        # Run the application
        subprocess.run([venv_python, MAIN_PY])
        print_colored("\n✅ Application closed successfully", Colors.OKGREEN)
    except KeyboardInterrupt:
        print_colored("\n⚠️  Application interrupted by user", Colors.WARNING)
    except Exception as e:
        print_colored(f"\n❌ Error running application: {e}", Colors.FAIL)
        sys.exit(1)

def main():
    """Main launcher function"""
    print_header(f"{APP_NAME} - Universal Launcher")
    print_colored(f"Platform: {platform.system()} {platform.release()}", Colors.OKCYAN)
    print_colored(f"Architecture: {platform.machine()}\n", Colors.OKCYAN)

    # Step 1: Check Python version
    check_python_version()

    # Step 2: Check required files
    if not check_required_files():
        print_colored("\n❌ Setup failed: Required files missing", Colors.FAIL)
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Step 3: Check if setup is needed
    needs_setup = not os.path.exists(VENV_DIR) or not check_dependencies_installed()

    if needs_setup:
        print_header("First-Time Setup")
        print_colored("This appears to be the first run. Setting up the environment...", Colors.WARNING)
        print_colored("This will take a few minutes, but only needs to be done once.\n", Colors.WARNING)

        # Create virtual environment
        if not create_virtual_environment():
            print_colored("\n❌ Setup failed: Could not create virtual environment", Colors.FAIL)
            input("\nPress Enter to exit...")
            sys.exit(1)

        # Install dependencies
        if not install_dependencies():
            print_colored("\n❌ Setup failed: Could not install dependencies", Colors.FAIL)
            input("\nPress Enter to exit...")
            sys.exit(1)

        print_header("Setup Complete!")
        print_colored("Environment is ready. Starting the application...\n", Colors.OKGREEN)
    else:
        print_colored("✅ Environment already configured", Colors.OKGREEN)

    # Step 4: Run the application
    run_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  Launcher interrupted by user", Colors.WARNING)
        sys.exit(0)
    except Exception as e:
        print_colored(f"\n\n❌ Unexpected error: {e}", Colors.FAIL)
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
