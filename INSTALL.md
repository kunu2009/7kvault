# Installation Guide

## Step-by-Step Installation for Windows

### 1. Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.8 or higher
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Click "Install Now"

### 2. Verify Python Installation

Open PowerShell or Command Prompt and run:
```bash
python --version
```

You should see something like: `Python 3.11.x`

### 3. Install Required Packages

Navigate to the folder containing the vault app:
```bash
cd C:\Desktop\locker
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Wait for all packages to install. You should see:
- cryptography
- Pillow
- customtkinter

### 4. Run the Application

```bash
python vault_app.py
```

### 5. First Time Setup

1. The app will open with a setup screen
2. Create a strong master password
3. Confirm your password
4. Click "Create Vault"
5. You're ready to use the vault!

## Quick Start (After Installation)

Simply run:
```bash
python vault_app.py
```

Or double-click `vault_app.py` if Python is associated with `.py` files.

## Creating a Desktop Shortcut (Optional)

### Method 1: Simple Shortcut

1. Right-click `vault_app.py`
2. Select "Create shortcut"
3. Move shortcut to Desktop
4. Right-click shortcut → Properties
5. Change "Target" to: `python "C:\Desktop\locker\vault_app.py"`

### Method 2: Create a Batch File

Create a file named `SecureVault.bat` with this content:
```batch
@echo off
cd /d "C:\Desktop\locker"
python vault_app.py
pause
```

Double-click this file to launch the app!

## Troubleshooting

### "Python is not recognized"
- Python is not in PATH
- Reinstall Python with "Add to PATH" checked
- Or use full path: `C:\Python311\python.exe vault_app.py`

### "No module named 'cryptography'"
- Dependencies not installed
- Run: `pip install -r requirements.txt`

### "pip is not recognized"
- Python installation issue
- Try: `python -m pip install -r requirements.txt`

### App won't start
- Make sure you're in the correct directory
- Check Python version: `python --version` (must be 3.8+)
- Try: `python -u vault_app.py` for verbose output

## System Requirements

- **OS**: Windows 10 or higher
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended for large images)
- **Disk Space**: Depends on media collection size

## Uninstallation

1. Delete the app folder: `C:\Desktop\locker`
2. Delete the vault data: `%USERPROFILE%\.secure_vault` (if you want to remove all encrypted data)
3. Uninstall Python packages (optional):
   ```bash
   pip uninstall cryptography Pillow customtkinter
   ```

---

**Need Help?** Check README.md for usage instructions!
