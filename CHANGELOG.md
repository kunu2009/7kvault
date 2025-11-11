# Changelog

All notable changes to 7K Vault will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-11

### 🎉 Initial Release

#### Added
- **Military-grade encryption**: AES-256 with PBKDF2 key derivation (100,000 iterations)
- **Universal media support**: 33+ formats (12 image, 13 video, 8 audio)
- **Built-in media player**: VLC-powered video player with audio support
- **Folder organization**: Create custom albums to organize media
- **Auto-import folder**: Automatically encrypts files dropped into special folder
- **Keyboard shortcuts**: Full keyboard navigation (←→, Space, F, J/L, Esc)
- **Fullscreen mode**: Watch videos and view images in fullscreen
- **AutoPlay & Shuffle**: Slideshow mode with automatic advancement
- **Folder-aware navigation**: Navigate within specific folders
- **Export functionality**: Decrypt and save files anywhere
- **Secure deletion**: Automatically delete originals after encryption
- **Password protection**: Strong password with no recovery option
- **Emergency reset**: Password reset utility (deletes vault)
- **Background monitoring**: Auto-import folder watches for new files
- **iPhone photo support**: HEIC/HEIF format support
- **Modern dark UI**: Beautiful CustomTkinter interface
- **100% offline**: No internet connection required
- **Open source**: MIT licensed

#### Security Features
- AES-256 encryption for all files
- PBKDF2-HMAC-SHA256 key derivation
- SHA-256 password hashing
- Random salt per installation
- Encrypted file metadata
- UUID-based encrypted filenames
- No password storage (hash only)

#### Formats Supported
- **Images**: JPG, PNG, GIF, BMP, WebP, HEIC, HEIF, TIFF, ICO (12 total)
- **Videos**: MP4, AVI, MOV, MKV, WebM, FLV, M4V, WMV, 3GP, MPEG, VOB, OGV (13 total)
- **Audio**: MP3, WAV, FLAC, M4A, AAC, OGG, WMA, OPUS (8 total)

#### Keyboard Shortcuts
- `←` - Previous media
- `→` - Next media
- `Space` / `K` - Play/Pause video
- `J` - Rewind 10 seconds
- `L` - Forward 10 seconds
- `F` - Toggle fullscreen
- `Esc` - Close viewer / Exit fullscreen

### Technical Details
- Python 3.8+ required
- CustomTkinter for modern UI
- VLC for video playback
- pygame for audio playback
- Pillow + pillow-heif for image processing
- cryptography library for encryption
- opencv-python for video frame extraction

### Known Issues
- Video thumbnail generation can be slow (feature temporarily disabled for performance)
- Large video files may take time to decrypt for playback
- VLC must be installed separately for video playback

### Future Plans
- Compiled Windows executable (.exe)
- Video thumbnail caching
- Batch export functionality
- Search/filter functionality
- Tags and metadata
- Multiple vault support
- Dark/light theme toggle
- Mobile versions (Android/iOS)

---

## [Unreleased]

### Planned Features
- [ ] Windows installer (.msi)
- [ ] Portable executable (no installation)
- [ ] Video thumbnail generation (optimized)
- [ ] Batch export selected files
- [ ] Search functionality
- [ ] Tag system
- [ ] Favorites/starred media
- [ ] Recently viewed
- [ ] Trash/recycle bin
- [ ] Vault statistics
- [ ] Theme customization
- [ ] Slideshow settings (timing)
- [ ] Video playback speed control
- [ ] Screenshot protection
- [ ] Vault backup/restore
- [ ] Multiple vault profiles
- [ ] Import from cloud (Google Photos, etc.)

### Under Consideration
- [ ] Mobile app (Android)
- [ ] Mobile app (iOS)
- [ ] Linux support
- [ ] macOS support
- [ ] Cloud sync (encrypted)
- [ ] Browser extension
- [ ] Portable version (USB drive)

---

## Version History

- **1.0.0** (2025-12-11) - Initial release

---

## How to Update

### From Source
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### From Executable
Download the latest release from GitHub and replace the old executable.

---

## Breaking Changes

None yet! First release.

---

## Contributors

Thank you to all contributors! (List coming soon)

---

*For detailed commit history, see [GitHub commits](https://github.com/kunu2009/7kvault/commits/main)*
