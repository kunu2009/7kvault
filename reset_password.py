"""
Emergency Password Reset for Secure Vault
WARNING: This will reset your password. Your encrypted files will remain safe.
"""

import json
import hashlib
import os
from pathlib import Path

def reset_password():
    app_dir = Path.home() / ".secure_vault"
    config_file = app_dir / "config.json"
    
    if not config_file.exists():
        print("❌ No vault found. Nothing to reset.")
        return
    
    print("=" * 60)
    print("🔓 EMERGENCY PASSWORD RESET")
    print("=" * 60)
    print()
    print("⚠️  WARNING: This will reset your master password.")
    print("Your encrypted files will remain intact and safe.")
    print()
    
    confirm = input("Type 'RESET' to continue: ")
    
    if confirm != "RESET":
        print("\n❌ Reset cancelled.")
        return
    
    print()
    new_password = input("Enter NEW password: ")
    
    if len(new_password) < 4:
        print("❌ Password must be at least 4 characters long.")
        return
    
    confirm_password = input("Confirm NEW password: ")
    
    if new_password != confirm_password:
        print("❌ Passwords do not match!")
        return
    
    # Generate new salt and hash
    salt = os.urandom(16)
    password_hash = hashlib.sha256((new_password + salt.hex()).encode()).hexdigest()
    
    # Save new config
    config = {
        "password_hash": password_hash,
        "salt": salt.hex()
    }
    
    with open(config_file, 'w') as f:
        json.dump(config, f)
    
    print()
    print("=" * 60)
    print("✅ PASSWORD RESET SUCCESSFUL!")
    print("=" * 60)
    print()
    print(f"Your new password is: {new_password}")
    print()
    print("⚠️  IMPORTANT: Write this down somewhere safe!")
    print()
    print("You can now launch the vault and use your new password.")
    print("All your encrypted files are safe and unchanged.")
    print("=" * 60)

if __name__ == "__main__":
    try:
        reset_password()
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    input("\nPress Enter to exit...")
