@echo off@echo off

title 7K Vault - Password Reset Tooltitle Password Reset - Secure Vault

cd /d "%~dp0"color 0A

echo.

echo.echo ============================================================

echo ================================================echo            PASSWORD RESET FOR SECURE VAULT

echo        7K Vault - Password Reset Toolecho ============================================================

echo ================================================echo.

echo.echo This will reset your master password.

echo WARNING: This will DELETE all vault data!echo Your encrypted files will remain safe.

echo Your encrypted files cannot be recovered.echo.

echo.pause

echo Press any key to continue or close this window to cancel...echo.

pause >nulpython -c "import json, hashlib, os; from pathlib import Path; app_dir = Path.home() / '.secure_vault'; config_file = app_dir / 'config.json'; new_pass = input('Enter NEW password: '); confirm = input('Confirm password: '); exit('Passwords do not match!') if new_pass != confirm else None; salt = os.urandom(16); hash_val = hashlib.sha256((new_pass + salt.hex()).encode()).hexdigest(); config = {'password_hash': hash_val, 'salt': salt.hex()}; open(config_file, 'w').write(__import__('json').dumps(config)); print('\n✅ SUCCESS! Your new password is:', new_pass, '\nWrite this down!')"

echo.

python reset_password.pyecho ============================================================

echo                   RESET COMPLETE!

pauseecho ============================================================

echo.
pause
