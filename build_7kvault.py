# 7K Vault - Build Windows Executable
# This script creates a standalone .exe file

import os
import sys
import PyInstaller.__main__

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
app_file = os.path.join(script_dir, 'vault_app.py')

print("=" * 60)
print("Building 7K Vault Windows Executable")
print("=" * 60)
print()

# PyInstaller arguments
args = [
    app_file,
    '--onefile',              # Single executable file
    '--windowed',             # No console window
    '--name=7KVault',         # Name of the executable
    '--clean',                # Clean PyInstaller cache
    '--noconfirm',           # Replace output directory without asking
    # Add icon if available
    # '--icon=icon.ico',
    # Hidden imports for CustomTkinter
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=customtkinter',
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.ttk',
    '--hidden-import=tkinter.filedialog',
    '--hidden-import=tkinter.messagebox',
    # Hidden imports for other dependencies
    '--hidden-import=cryptography',
    '--hidden-import=cv2',
    '--hidden-import=pygame',
    '--hidden-import=vlc',
    '--hidden-import=pillow_heif',
    # Collect data files for CustomTkinter
    '--collect-all=customtkinter',
]

print("Building with PyInstaller...")
print()

try:
    PyInstaller.__main__.run(args)
    print()
    print("=" * 60)
    print("✅ BUILD SUCCESSFUL!")
    print("=" * 60)
    print()
    print(f"Executable location: {os.path.join(script_dir, 'dist', '7KVault.exe')}")
    print()
    print("You can now:")
    print("1. Test the executable: dist\\7KVault.exe")
    print("2. Share it with users")
    print("3. Upload to GitHub Releases")
    print()
except Exception as e:
    print()
    print("=" * 60)
    print("❌ BUILD FAILED!")
    print("=" * 60)
    print()
    print(f"Error: {e}")
    print()
    sys.exit(1)
