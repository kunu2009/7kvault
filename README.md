# 🔒 7K Vault - Free Encrypted Gallery for Windows# 🔒 Secure Vault - Encrypted Gallery App for Windows



[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)A fully encrypted gallery vault application for Windows, similar to Android vault apps. Securely store and view your photos and videos with military-grade encryption.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)## Features



**The ultimate FREE encrypted media vault for Windows** - Hide and protect your photos, videos, and audio files with military-grade AES-256 encryption!### 🔐 Security

- ✅ **Strong Encryption**: AES-256 encryption using Fernet (symmetric encryption)

🌐 **Website**: [https://kunu2009.github.io/7kvault](https://kunu2009.github.io/7kvault)- ✅ **Password Protected**: Master password with PBKDF2 key derivation (100,000 iterations)

- ✅ **Auto-Encrypt Folder**: Drop files into a special folder - they're automatically encrypted!

## ✨ Features- ✅ **Offline**: Works completely offline, no internet required



### 🔐 Military-Grade Security### 📁 Organization

- **AES-256 encryption** using Fernet (cryptography library)- ✅ **Albums/Folders**: Create albums to organize your media inside the app

- **PBKDF2 key derivation** with 100,000 iterations- ✅ **Move to Albums**: Easily move items between albums

- **Password-protected** vault with SHA-256 hashing- ✅ **Auto-Imported Album**: Files from auto-encrypt folder go to special album

- **Emergency password reset** utility included

### 🎬 Media Support

### 🖼️ Universal Media Support- ✅ **Images**: JPG, PNG, GIF, BMP, WEBP - view with arrow key navigation

**33+ formats supported:**- ✅ **Videos**: MP4, AVI, MOV, MKV, WEBM, FLV - **BUILT-IN VIDEO PLAYER!**

- **Images** (12): JPG, PNG, GIF, BMP, WebP, HEIC/HEIF (iPhone), TIFF, ICO- ✅ **Thumbnail Gallery**: Scroll through all your images in a grid layout

- **Videos** (13): MP4, AVI, MOV, MKV, WebM, FLV, M4V, WMV, 3GP, MPEG, VOB, OGV- ✅ **Full-Screen Viewer**: Click any image to view in full size

- **Audio** (8): MP3, WAV, FLAC, M4A, AAC, OGG, WMA, OPUS- ✅ **Video Player**: Play videos directly in the app with playback controls

- ✅ **Keyboard Navigation**: Use ← → arrow keys to browse through images

### 🎬 Advanced Media Player

- **Universal viewer** for all media types### 📤 Import/Export

- **VLC-powered video player** with smooth playback and audio- ✅ **Import Files**: Add individual photos and videos

- **Keyboard shortcuts**: Arrow keys, Space, F (fullscreen), J/L (±10s)- ✅ **Import Folders**: Add entire folders - they disappear from your computer!

- **Fullscreen mode** with proper resizing- ✅ **Auto-Import Folder**: Special folder that auto-encrypts anything you drop in

- **AutoPlay & Shuffle** modes- ✅ **Export Anytime**: Get your files back out when needed (📤 button)

- **Folder-aware navigation** - navigate within specific albums- ✅ **Move or Copy**: Choose to delete originals (move) or keep them (copy)



### 📁 Folder Organization## Installation

- Create **custom folders/albums** to organize your vault

- Move media between folders### Quick Start (Easiest Method):

- Filter view by folder1. **Double-click** `LaunchVault.bat` 

- Clean, intuitive interface2. That's it! The app launches automatically

3. Create a desktop shortcut for easy access (see BUILD_INSTRUCTIONS.md)

### ⚡ Smart Features

- **Drag & drop** file import### Manual Method:

- **Auto-import folder** - automatically encrypts files dropped there1. **Install Python 3.8 or higher** (if not already installed)

- **Bulk operations** - import entire folders at once   - Download from [python.org](https://www.python.org/downloads/)

- **Secure deletion** - automatically delete originals after encryption

- **Export** - decrypt and save files anywhere2. **Install dependencies**:

- **Background monitoring** - auto-import folder watches for new files   ```bash

   pip install -r requirements.txt

## 🚀 Quick Start   ```



### Option 1: Windows Executable (Easiest)3. **Run the application**:

1. Download `7KVault-Setup.exe` from [Releases](https://github.com/kunu2009/7kvault/releases)   ```bash

2. Run the installer   python vault_app.py

3. Launch 7K Vault from desktop shortcut   ```

4. Create your master password

5. Start adding files!### Build Windows EXE (Optional):

See `BUILD_INSTRUCTIONS.md` for creating a standalone executable

### Option 2: Run from Source

1. **Install Python 3.8+** from [python.org](https://www.python.org/downloads/)2. **First Time Setup**:

2. **Clone the repository:**   - Create a master password (remember this - it cannot be recovered!)

   ```bash   - Your password should be at least 4 characters (longer is more secure)

   git clone https://github.com/kunu2009/7kvault.git

   cd 7kvault3. **Add Media**:

   ```   

3. **Install dependencies:**   **Option A - Add Individual Files**:

   ```bash   - Click "➕ Add Files" button

   pip install -r requirements.txt   - Select photos or videos from your computer

   ```   - Choose whether to MOVE (delete originals) or COPY (keep originals)

4. **Install VLC Media Player** (for video playback):   - Files are automatically encrypted and stored securely

   - Download from [videolan.org](https://www.videolan.org/)   

5. **Run the app:**   **Option B - Add Entire Folder**:

   ```bash   - Click "📂 Add Folder" button

   python vault_app.py   - Select a folder (all media files including subfolders will be imported)

   ```   - Confirms deletion of the ENTIRE folder (not just files!)

   Or double-click `LaunchVault.bat`   - Great for importing entire photo albums and making them disappear!



## 📖 How to Use4. **View Media**:

   

### First Time Setup   **Images**:

1. Launch 7K Vault   - Click any image thumbnail to view full size

2. Create a **strong master password** (you'll need this every time!)   - Use **← Left Arrow** to go to previous image

3. Your vault is now ready!   - Use **→ Right Arrow** to go to next image

   - Press **Esc** to close viewer and return to gallery

### Adding Files   - Or use the on-screen buttons

- **Method 1**: Click "➕ Add Files" button   

- **Method 2**: Click "📁 Add Folder" to import entire folders   **Videos**:

- **Method 3**: Use "💜 Auto-Import Folder" - drop files there and they auto-encrypt!   - Click the "▶ VIDEO" button on any video thumbnail

   - **Built-in video player** opens with full controls

### Organizing Media   - Play, Pause, Restart - all inside the app!

- Click "➕ New Folder" to create albums (e.g., "Vacation", "Family")   - No need to export just to watch

- Click the 📁 button on any media to move it to a folder   - Export option available if needed

- Click folder names to view that folder's contents

5. **Export Media**:

### Viewing Media   - Click the 📤 (green export button) on any thumbnail

- Click any thumbnail to open the universal viewer   - Choose where to save the decrypted file

- Use **Arrow keys** (←→) to navigate   - File is exported back to normal format

- Press **Space** to play/pause videos   - Also available in the image viewer

- Press **F** for fullscreen

- Press **J/L** to skip ±10 seconds in videos6. **Delete Media**:

- Toggle **AutoPlay** to auto-advance through media   - Click the 🗑 button on any thumbnail

- Toggle **Shuffle** for random playback   - Confirm deletion (WARNING: Cannot be recovered!)



### Managing Files7. **Lock Vault**:

- **📤 Export**: Decrypt and save file anywhere   - Click "🔒 Lock" to secure your vault

- **🗑️ Delete**: Remove from vault permanently   - You'll need to enter your password again to unlock

- **🔒 Lock**: Close vault and return to password screen

## Security Features

## ⌨️ Keyboard Shortcuts

### Encryption

| Key | Action |- **Algorithm**: AES-256 in CBC mode (Fernet)

|-----|--------|- **Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations

| **←** | Previous media |- **Random Salt**: Unique salt for each vault installation

| **→** | Next media |- **Encrypted Storage**: All media files are encrypted before storage

| **Space** / **K** | Play/Pause video |- **Encrypted Index**: Even the file index is encrypted

| **J** | Rewind 10 seconds |

| **L** | Forward 10 seconds |### Password Protection

| **F** | Toggle fullscreen |- Master password never stored in plain text

| **Esc** | Close viewer / Exit fullscreen |- Password hash uses SHA-256 with salt

- Strong key derivation prevents brute force attacks

## 🔧 Technical Details

### Privacy

### Security- All data stored locally in `%USERPROFILE%\.secure_vault`

- **Encryption**: AES-256 via Fernet (symmetric encryption)- No cloud sync or internet connection required

- **Key Derivation**: PBKDF2-HMAC-SHA256 (100,000 iterations)- Files are only decrypted in memory when viewing

- **Password Storage**: SHA-256 hash only (password never stored)

- **Data Location**: `%USERPROFILE%\.secure_vault\`## File Structure



### Architecture```

- **Language**: Python 3.8+%USERPROFILE%\.secure_vault/

- **GUI**: CustomTkinter (modern dark theme)├── config.json          # Password hash and salt

- **Image Processing**: Pillow + pillow-heif├── media_index.enc      # Encrypted media index

- **Video Playback**: VLC (python-vlc)└── vault/              # Encrypted media files

- **Audio Playback**: pygame    ├── abc123...enc

- **Encryption**: cryptography library    ├── def456...enc

    └── ...

## 🛡️ Privacy & Security```



✅ **100% Offline** - No internet connection required  ## Supported File Types

✅ **No telemetry** - Zero data collection  

✅ **No cloud** - Everything stored locally on your PC  - **Images**: JPG, JPEG, PNG, GIF, BMP

✅ **Open source** - Audit the code yourself  - **Videos**: MP4, AVI, MOV, MKV, WEBM, FLV (with built-in video player!)

✅ **Your password never leaves your computer**  

## Tips

> ⚠️ **IMPORTANT**: If you forget your master password, your files are **unrecoverable**. Use the password reset tool only in emergencies (it creates a new vault).

- **Strong Password**: Use a strong, memorable password

## 🐛 Troubleshooting- **Move vs Copy**: When adding files, choose "Yes" to delete originals (more secure), "No" to keep copies

- **Folder Import**: Perfect for moving entire photo/video collections into the vault

### Videos not playing or no audio- **Arrow Keys**: Use ← → keys to quickly browse through your images

- Install **VLC Media Player** from [videolan.org](https://www.videolan.org/)- **Backup**: Keep backups of the `.secure_vault` folder (but keep password safe!)

- Restart 7K Vault after installing VLC- **Performance**: Large files may take a moment to encrypt/decrypt

- **RAM**: Full-size images are loaded into memory when viewing

### "Module not found" errors

```bash## Troubleshooting

pip install -r requirements.txt --upgrade

```**Q: I forgot my password!**

A: Unfortunately, there's no way to recover your password. You'll need to delete the vault and start fresh. This is by design for maximum security.

### Forgot password?

1. Run `ResetPassword.bat` or `python reset_password.py`**Q: What happens to my original files?**

2. This will **delete all vault data** and let you start freshA: When adding files individually, you choose. When adding a folder, originals are automatically deleted. The encrypted files are stored in `%USERPROFILE%\.secure_vault\vault\`

3. **Your encrypted files are unrecoverable without the password**

**Q: Can I get my original files back?**

### App not respondingA: No, if you chose to delete originals (or used folder import), they're permanently deleted. Only the encrypted versions exist in the vault. This is for security!

- Close and reopen the app

- Check `%USERPROFILE%\.secure_vault\` folder size**Q: App is slow with many images**

- Consider organizing into multiple foldersA: The app decrypts images on-the-fly. This is normal for encrypted storage. Consider organizing media into multiple vaults.



## 📦 Building from Source**Q: Can I move the vault to another computer?**

A: Yes! Copy the entire `.secure_vault` folder and use the same password on the new computer.

### Create Windows Executable

```bash## Technical Details

pip install pyinstaller

pyinstaller --onefile --windowed --icon=icon.ico --name="7KVault" vault_app.py- **GUI Framework**: CustomTkinter (modern, dark theme)

```- **Encryption**: cryptography library (Fernet)

- **Image Processing**: Pillow (PIL)

## 🤝 Contributing- **Language**: Python 3.8+



Contributions are welcome! Please:## License

1. Fork the repository

2. Create a feature branch (`git checkout -b feature/AmazingFeature`)Free to use for personal purposes.

3. Commit changes (`git commit -m 'Add AmazingFeature'`)

4. Push to branch (`git push origin feature/AmazingFeature`)## Warning

5. Open a Pull Request

⚠️ **IMPORTANT**: 

## 📝 License- Never forget your master password

- Keep backups of your vault folder

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.- This is a basic vault - not audited for high-security use cases

- Test with non-critical files first

## 🙏 Acknowledgments

---

- **CustomTkinter** - Modern UI framework

- **VLC Media Player** - Video playback engine**Made with ❤️ for privacy-conscious users**

- **Cryptography** - Encryption library
- All contributors and users!

## ⭐ Support

If you find 7K Vault useful, please:
- ⭐ **Star this repository**
- 🐛 **Report bugs** via Issues
- 💡 **Suggest features** via Issues
- 📢 **Share with friends** who need privacy

## 📞 Contact

- **GitHub**: [@kunu2009](https://github.com/kunu2009)
- **Issues**: [Report a bug](https://github.com/kunu2009/7kvault/issues)

---

**Made with 💜 for privacy-conscious users**

*7K Vault - Your media, your privacy, your control.*
