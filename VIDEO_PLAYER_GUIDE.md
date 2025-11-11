# 🎬 Built-in Video Player Guide

## What's New

### ✨ Built-in Video Player
- **No more exporting to watch videos!**
- Click any video thumbnail to play it directly in the app
- Full playback controls: Play, Pause, Restart
- Real-time progress tracking
- Export option available while watching

### 🎮 How to Use

1. **Play Video**: Click the large "▶ VIDEO" button on any video thumbnail
2. **Controls**:
   - ▶ Play / ⏸ Pause - Start or pause playback
   - ⟲ Restart - Go back to beginning
   - 📤 Export - Save video to your computer
   - Close - Exit video player

3. **Features**:
   - Automatic frame-by-frame playback
   - Video loops when finished
   - Shows frame count and progress percentage
   - Maintains original video quality

### 📂 Auto-Import Fixed

The auto-import folder now **automatically refreshes** the gallery!

**How it works**:
1. Click the purple "📂 Auto-Import Folder" button at the top
2. Drop any image or video file into that folder
3. Within 2 seconds:
   - File is encrypted
   - Added to your vault
   - **Gallery refreshes automatically**
   - Original file is deleted

**Tips**:
- Create a desktop shortcut to the auto-import folder for easy access
- You can drop multiple files at once
- All file types are supported (images and videos)

### 🎥 Supported Video Formats
- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WebM (.webm)
- FLV (.flv)

### 🖼️ Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)

## Technical Details

- Uses **OpenCV** for high-quality video playback
- Videos are decrypted to temporary files during playback
- Temp files are automatically cleaned up when you close the player
- Background thread watches auto-import folder every 2 seconds
- Gallery refreshes automatically when new files are detected

## Security Notes

- Videos remain encrypted in the vault
- Only decrypted temporarily when playing
- Temp files are deleted immediately after closing the player
- Auto-imported files are encrypted with AES-256
- Original files are securely deleted after import

---

**Enjoy your fully encrypted, self-contained media vault! 🔒**
