# 🧪 Testing Your Vault

## Test the Auto-Import Feature

1. **Launch the app** and unlock your vault

2. **Click the purple "📂 Auto-Import Folder" button** at the top

3. **The folder will open** - this is your auto-import folder

4. **Drag and drop ANY file** into this folder (try an image or video)

5. **Wait 2 seconds**

6. **Check your vault gallery** - the file should appear automatically!

7. **The original file in the folder is gone** - it's now encrypted in your vault

## Test the Video Player

1. **Add a video** to your vault (MP4, AVI, MOV, etc.)

2. **Find the video thumbnail** - it shows "▶ VIDEO"

3. **Click the big play button**

4. **Video player opens** with these controls:
   - ▶ Play - Start playback
   - ⏸ Pause - Pause playback
   - ⟲ Restart - Go back to start
   - 📤 Export - Save to computer
   - Close - Exit player

5. **Click Play** and watch your video!

## What Should Happen

### Auto-Import:
✅ Files dropped in auto-import folder disappear within 2 seconds
✅ They appear in your vault gallery automatically
✅ Gallery refreshes on its own (no need to close/reopen)
✅ Original files are deleted

### Video Player:
✅ Videos play smoothly frame-by-frame
✅ Progress bar shows current frame and percentage
✅ You can pause/resume anytime
✅ Videos loop when they reach the end
✅ Export still works from the player

## Troubleshooting

**Auto-import not working?**
- Make sure you're logged into the vault
- Check the console for any error messages
- Try with a small test file first
- The folder is at: `%USERPROFILE%\.secure_vault\auto_import\`

**Video won't play?**
- Make sure opencv-python is installed: `pip install opencv-python`
- Check if the video file is corrupted
- Try a different video format (MP4 is most reliable)
- Check console for error messages

**Gallery not refreshing?**
- The refresh happens after each file is processed
- If you drop multiple files, it refreshes after each one
- Give it 2-3 seconds per file

---

**Everything working? Enjoy your secure vault! 🔒🎉**
