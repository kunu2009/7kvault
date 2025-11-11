"""
Build script to create Windows executable for Secure Vault
"""
import PyInstaller.__main__
import os
from pathlib import Path

# Get the directory of this script
current_dir = Path(__file__).parent

# PyInstaller configuration
PyInstaller.__main__.run([
    str(current_dir / 'vault_app.py'),
    '--name=SecureVault',
    '--onefile',
    '--windowed',  # No console window
    '--icon=NONE',
    '--add-data', f'{current_dir};.',
    '--hidden-import=PIL._tkinter_finder',
    '--clean',
    '--noconfirm',
])

print("\n" + "="*60)
print("✅ Build Complete!")
print("="*60)
print(f"Executable location: {current_dir / 'dist' / 'SecureVault.exe'}")
print("\nYou can now:")
print("1. Run SecureVault.exe directly")
print("2. Create a desktop shortcut to SecureVault.exe")
print("3. Move it anywhere you want!")
print("="*60)
