# How to Create Windows Executable

## Option 1: Use the Batch File Launcher (EASIEST - No Build Needed!)

**This is the simplest way to use the app like a Windows application:**

1. **Double-click** `LaunchVault.bat`
2. That's it! The app will launch automatically
3. **Create Desktop Shortcut**:
   - Right-click `LaunchVault.bat`
   - Select "Create shortcut"
   - Drag shortcut to Desktop
   - Rename to "Secure Vault"
   - Now you can double-click the desktop icon to launch!

**Advantages:**
- No build process needed
- Works immediately
- Easy to update (just replace vault_app.py)
- Smaller file size

---

## Option 2: Build Standalone EXE (Advanced)

**This creates a single `.exe` file that doesn't need Python installed:**

### Step 1: Install PyInstaller
```bash
pip install -r requirements_build.txt
```

### Step 2: Build the Executable
```bash
python build_exe.py
```

### Step 3: Find Your EXE
The executable will be created at:
```
C:\Desktop\locker\dist\SecureVault.exe
```

### Step 4: Use It!
- Double-click `SecureVault.exe` to run
- Copy it anywhere on your computer
- Create desktop shortcuts
- No Python needed on other computers!

**Advantages:**
- Single file - no Python installation needed
- Can share with others
- Professional appearance

**Disadvantages:**
- Larger file size (~50-100 MB)
- Takes time to build
- Harder to update

---

## Recommended Approach

**For Personal Use:** Use `LaunchVault.bat` (Option 1)
- Fastest to setup
- Easy to maintain
- Works perfectly

**For Sharing:** Build EXE (Option 2)
- Share with friends/family who don't have Python
- More "app-like" experience

---

## Creating a Desktop Shortcut

### For LaunchVault.bat:
1. Right-click `LaunchVault.bat`
2. Create shortcut
3. Move to Desktop
4. Rename to "Secure Vault"
5. (Optional) Right-click shortcut → Properties → Change Icon

### For SecureVault.exe:
1. Navigate to `dist\SecureVault.exe`
2. Right-click → Send to → Desktop (create shortcut)
3. Done!

---

## Troubleshooting

**LaunchVault.bat says Python not found:**
- Install Python from python.org
- During installation, check "Add Python to PATH"

**Build fails with PyInstaller:**
- Make sure all dependencies installed: `pip install -r requirements_build.txt`
- Try running as Administrator

**EXE is too large:**
- This is normal! The exe includes Python and all libraries
- Typical size: 50-100 MB

**Want a custom icon:**
- Find a `.ico` file you like
- Edit `build_exe.py`, change `'--icon=NONE'` to `'--icon=path/to/icon.ico'`
- Rebuild

---

## Quick Start Summary

**Easiest way to use:**
```
1. Double-click LaunchVault.bat
2. Create desktop shortcut
3. Done!
```

**To build EXE:**
```
pip install pyinstaller
python build_exe.py
```

That's it! Enjoy your Secure Vault! 🔒
