import os
import json
import hashlib
import base64
import time
import threading
import tempfile
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import io
import shutil
import cv2
import numpy as np

# Import HEIF support for iPhone photos
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIF_SUPPORT = True
except:
    HEIF_SUPPORT = False

# Import pygame for audio playback
try:
    import pygame
    pygame.mixer.init()
    AUDIO_SUPPORT = True
except:
    AUDIO_SUPPORT = False

# Import VLC for video playback with audio
try:
    import vlc
    VLC_SUPPORT = True
except:
    VLC_SUPPORT = False

class VaultApp:
    # Comprehensive format support
    IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif', '.ico', '.heic', '.heif'}
    VIDEO_FORMATS = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.m4v', '.wmv', '.3gp', '.mpeg', '.mpg', '.vob', '.ogv'}
    AUDIO_FORMATS = {'.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg', '.wma', '.opus'}
    
    def __init__(self):
        self.app_dir = Path.home() / ".secure_vault"
        self.vault_dir = self.app_dir / "vault"
        self.watched_dir = self.app_dir / "auto_import"
        self.config_file = self.app_dir / "config.json"
        self.media_index_file = self.app_dir / "media_index.enc"
        
        self.app_dir.mkdir(exist_ok=True)
        self.vault_dir.mkdir(exist_ok=True)
        self.watched_dir.mkdir(exist_ok=True)
        
        self.cipher = None
        self.media_items = []
        self.folders = []  # List of folder names
        self.current_folder = "All Media"  # Current selected folder
        self.current_index = 0
        self.watching = False
        self.watch_thread = None
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("7K Vault - Encrypted Gallery")
        self.root.geometry("1000x700")
        
        if not self.config_file.exists():
            self.show_setup_screen()
        else:
            self.show_login_screen()
    
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def save_config(self, password: str):
        """Save password hash and salt"""
        salt = os.urandom(16)
        password_hash = hashlib.sha256((password + salt.hex()).encode()).hexdigest()
        
        config = {
            "password_hash": password_hash,
            "salt": salt.hex()
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
        
        return salt
    
    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        
        salt = bytes.fromhex(config['salt'])
        password_hash = hashlib.sha256((password + salt.hex()).encode()).hexdigest()
        
        if password_hash == config['password_hash']:
            self.cipher = Fernet(self.derive_key(password, salt))
            return True
        return False
    
    def show_setup_screen(self):
        """Initial setup screen to create password"""
        self.clear_window()
        
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        title = ctk.CTkLabel(frame, text="🔒 7K Vault Setup", font=("Arial", 28, "bold"))
        title.pack(pady=30)
        
        subtitle = ctk.CTkLabel(frame, text="Create a master password to secure your media", font=("Arial", 14))
        subtitle.pack(pady=10)
        
        password_entry = ctk.CTkEntry(frame, placeholder_text="Enter Password", show="*", width=300, height=40)
        password_entry.pack(pady=15)
        
        confirm_entry = ctk.CTkEntry(frame, placeholder_text="Confirm Password", show="*", width=300, height=40)
        confirm_entry.pack(pady=15)
        
        def setup_vault():
            password = password_entry.get()
            confirm = confirm_entry.get()
            
            if not password or len(password) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters long")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            salt = self.save_config(password)
            self.cipher = Fernet(self.derive_key(password, salt))
            self.save_media_index()
            messagebox.showinfo("Success", "Vault created successfully!")
            self.show_main_screen()
        
        setup_btn = ctk.CTkButton(frame, text="Create Vault", command=setup_vault, width=200, height=45, font=("Arial", 16))
        setup_btn.pack(pady=30)
    
    def show_login_screen(self):
        """Login screen to unlock vault"""
        self.clear_window()
        
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        title = ctk.CTkLabel(frame, text="🔒 7K Vault", font=("Arial", 28, "bold"))
        title.pack(pady=30)
        
        subtitle = ctk.CTkLabel(frame, text="Enter your master password", font=("Arial", 14))
        subtitle.pack(pady=10)
        
        password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=300, height=40)
        password_entry.pack(pady=20)
        
        def unlock_vault():
            password = password_entry.get()
            
            if self.verify_password(password):
                self.load_media_index()
                self.start_watching()
                self.show_main_screen()
            else:
                messagebox.showerror("Error", "Incorrect password")
                password_entry.delete(0, 'end')
        
        password_entry.bind('<Return>', lambda e: unlock_vault())
        
        unlock_btn = ctk.CTkButton(frame, text="Unlock Vault", command=unlock_vault, width=200, height=45, font=("Arial", 16))
        unlock_btn.pack(pady=20)
    
    def show_main_screen(self):
        """Main gallery screen"""
        self.clear_window()
        
        # Top bar
        top_frame = ctk.CTkFrame(self.root, height=60)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        title = ctk.CTkLabel(top_frame, text="📁 7K Vault", font=("Arial", 20, "bold"))
        title.pack(side="left", padx=20, pady=10)
        
        # Auto-import folder button
        watch_info = ctk.CTkButton(
            top_frame,
            text="📂 Auto-Import Folder",
            command=self.show_watched_folder_info,
            width=160,
            fg_color="purple"
        )
        watch_info.pack(side="right", padx=5, pady=10)
        
        add_folder_btn = ctk.CTkButton(top_frame, text="📂 Add Folder", command=self.add_folder, width=120)
        add_folder_btn.pack(side="right", padx=5, pady=10)
        
        add_btn = ctk.CTkButton(top_frame, text="➕ Add Files", command=self.add_media, width=120)
        add_btn.pack(side="right", padx=5, pady=10)
        
        lock_btn = ctk.CTkButton(top_frame, text="🔒 Lock", command=self.lock_vault, width=100)
        lock_btn.pack(side="right", padx=10, pady=10)
        
        # Folder navigation bar
        folder_frame = ctk.CTkFrame(self.root)
        folder_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        folder_label = ctk.CTkLabel(folder_frame, text="📁 Folders:", font=("Arial", 14, "bold"))
        folder_label.pack(side="left", padx=10, pady=5)
        
        # All Media button
        all_btn = ctk.CTkButton(
            folder_frame,
            text="All Media",
            command=lambda: self.switch_folder("All Media"),
            width=100,
            fg_color="blue" if self.current_folder == "All Media" else "gray"
        )
        all_btn.pack(side="left", padx=5, pady=5)
        
        # Folder buttons
        for folder_name in self.folders:
            folder_btn = ctk.CTkButton(
                folder_frame,
                text=folder_name,
                command=lambda f=folder_name: self.switch_folder(f),
                width=120,
                fg_color="blue" if self.current_folder == folder_name else "gray"
            )
            folder_btn.pack(side="left", padx=5, pady=5)
        
        # Manage folders button
        manage_btn = ctk.CTkButton(
            folder_frame,
            text="➕ New Folder",
            command=self.create_new_folder,
            width=120,
            fg_color="green"
        )
        manage_btn.pack(side="left", padx=5, pady=5)
        
        # Main content area
        content_frame = ctk.CTkFrame(self.root)
        content_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Get filtered items for current folder
        filtered_items = self.get_filtered_items()
        
        if not filtered_items:
            empty_label = ctk.CTkLabel(content_frame, 
                text=f"No media in '{self.current_folder}'\nClick 'Add Files' or 'Add Folder' to import", 
                font=("Arial", 18), text_color="gray")
            empty_label.pack(expand=True)
        else:
            self.show_gallery(content_frame, filtered_items)
    
    def get_filtered_items(self):
        """Get media items filtered by current folder"""
        if self.current_folder == "All Media":
            return self.media_items
        else:
            return [item for item in self.media_items if item.get('folder') == self.current_folder]
    
    def switch_folder(self, folder_name):
        """Switch to a different folder"""
        self.current_folder = folder_name
        self.show_main_screen()
    
    def create_new_folder(self):
        """Create a new folder"""
        dialog = ctk.CTkInputDialog(text="Enter folder name:", title="Create New Folder")
        folder_name = dialog.get_input()
        
        if folder_name:
            if folder_name in self.folders:
                messagebox.showwarning("Duplicate", "Folder already exists")
            elif folder_name == "All Media":
                messagebox.showwarning("Invalid", "Cannot use 'All Media' as folder name")
            else:
                self.folders.append(folder_name)
                self.save_media_index()
                messagebox.showinfo("Success", f"Folder '{folder_name}' created!")
                self.show_main_screen()
    
    def delete_folder_dialog(self, folder_name):
        """Delete a folder and optionally its contents"""
        items_in_folder = [item for item in self.media_items if item.get('folder') == folder_name]
        
        if items_in_folder:
            response = messagebox.askyesnocancel(
                "Delete Folder",
                f"Folder '{folder_name}' contains {len(items_in_folder)} item(s).\n\n"
                "YES = Delete folder and move items to 'All Media'\n"
                "NO = Delete folder and all items in it\n"
                "Cancel = Keep folder"
            )
            
            if response is True:  # Move items
                for item in items_in_folder:
                    item['folder'] = None
                self.folders.remove(folder_name)
                self.save_media_index()
                self.current_folder = "All Media"
                self.show_main_screen()
            elif response is False:  # Delete items
                for item in items_in_folder:
                    self.media_items.remove(item)
                    try:
                        os.unlink(item['file_path'])
                    except:
                        pass
                self.folders.remove(folder_name)
                self.save_media_index()
                self.current_folder = "All Media"
                self.show_main_screen()
        else:
            if messagebox.askyesno("Delete Folder", f"Delete empty folder '{folder_name}'?"):
                self.folders.remove(folder_name)
                self.save_media_index()
                self.current_folder = "All Media"
                self.show_main_screen()
    
    def show_gallery(self, parent, items_to_show):
        """Display gallery with thumbnails"""
        # Create scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(parent)
        scroll_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Grid layout for thumbnails
        columns = 4
        for idx, item in enumerate(items_to_show):
            row = idx // columns
            col = idx % columns
            
            # Find the actual index in self.media_items
            actual_index = self.media_items.index(item)
            
            # Create thumbnail frame
            thumb_frame = ctk.CTkFrame(scroll_frame, width=200, height=200)
            thumb_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            thumb_frame.grid_propagate(False)
            
            try:
                # Check file type
                file_ext = Path(item['name']).suffix.lower()
                is_video = file_ext in self.VIDEO_FORMATS
                is_audio = file_ext in self.AUDIO_FORMATS
                is_image = file_ext in self.IMAGE_FORMATS
                
                if is_audio:
                    # Show audio icon
                    thumb_frame.configure(fg_color="gray20")
                    
                    audio_btn = ctk.CTkButton(
                        thumb_frame,
                        text="🎵\nAUDIO",
                        font=("Arial", 32, "bold"),
                        command=lambda i=actual_index: self.view_media(i),
                        fg_color="gray20",
                        hover_color="gray30",
                        height=150
                    )
                    audio_btn.pack(expand=True, fill="both")
                    
                    # Filename label
                    name_label = ctk.CTkLabel(thumb_frame, text=item['name'][:20], font=("Arial", 10))
                    name_label.pack()
                
                elif is_video:
                    # Show video icon (fast and lightweight)
                    thumb_frame.configure(fg_color="gray20")
                    
                    # Make entire frame clickable for video playback
                    play_btn = ctk.CTkButton(
                        thumb_frame,
                        text="▶\nVIDEO",
                        font=("Arial", 32, "bold"),
                        command=lambda i=actual_index: self.view_media(i),
                        fg_color="gray20",
                        hover_color="gray30",
                        height=150
                    )
                    play_btn.pack(expand=True, fill="both")
                    
                    # Filename label (longer name for better identification)
                    name_label = ctk.CTkLabel(thumb_frame, text=item['name'][:25], font=("Arial", 10))
                    name_label.pack()
                else:
                    # Load and decrypt thumbnail for images
                    encrypted_data = self.load_encrypted_file(item['file_path'])
                    decrypted_data = self.cipher.decrypt(encrypted_data)
                    
                    image = Image.open(io.BytesIO(decrypted_data))
                    image.thumbnail((180, 180))
                    photo = ctk.CTkImage(light_image=image, dark_image=image, size=(180, 180))
                    
                    # Create clickable thumbnail
                    btn = ctk.CTkButton(thumb_frame, image=photo, text="", fg_color="transparent",
                                       command=lambda i=actual_index: self.view_media(i))
                    btn.pack(expand=True, fill="both")
                    
                    # Filename label
                    name_label = ctk.CTkLabel(thumb_frame, text=item['name'][:20], font=("Arial", 10))
                    name_label.pack()
                
                # Button frame for actions
                btn_frame = ctk.CTkFrame(thumb_frame, fg_color="transparent")
                btn_frame.place(relx=0.5, rely=0.05, anchor="n")
                
                # Move to folder button
                move_btn = ctk.CTkButton(btn_frame, text="📁", width=30, height=30,
                                        command=lambda i=actual_index, it=item: self.move_to_folder_dialog(i, it), 
                                        fg_color="purple")
                move_btn.pack(side="left", padx=2)
                
                # Export button
                export_btn = ctk.CTkButton(btn_frame, text="📤", width=30, height=30,
                                          command=lambda i=actual_index: self.export_media(i), fg_color="green")
                export_btn.pack(side="left", padx=2)
                
                # Delete button
                del_btn = ctk.CTkButton(btn_frame, text="🗑", width=30, height=30,
                                       command=lambda i=actual_index: self.delete_media(i), fg_color="red")
                del_btn.pack(side="left", padx=2)
                
            except Exception as e:
                # Show error with more details
                print(f"Error loading thumbnail for {item['name']}: {str(e)}")
                error_label = ctk.CTkLabel(thumb_frame, text=f"Error loading\n{item['name'][:15]}", 
                                          text_color="red", font=("Arial", 10))
                error_label.pack(expand=True)
                
                # Still add action buttons even if thumbnail fails
                btn_frame = ctk.CTkFrame(thumb_frame, fg_color="transparent")
                btn_frame.place(relx=0.5, rely=0.05, anchor="n")
                
                move_btn = ctk.CTkButton(btn_frame, text="📁", width=30, height=30,
                                        command=lambda i=actual_index, it=item: self.move_to_folder_dialog(i, it), 
                                        fg_color="purple")
                move_btn.pack(side="left", padx=2)
                
                export_btn = ctk.CTkButton(btn_frame, text="📤", width=30, height=30,
                                          command=lambda i=actual_index: self.export_media(i), fg_color="green")
                export_btn.pack(side="left", padx=2)
                
                del_btn = ctk.CTkButton(btn_frame, text="🗑", width=30, height=30,
                                       command=lambda i=actual_index: self.delete_media(i), fg_color="red")
                del_btn.pack(side="left", padx=2)
        
        # Configure grid weights
        for i in range(columns):
            scroll_frame.grid_columnconfigure(i, weight=1)
    
    def play_video(self, index):
        """Play video with built-in player (VLC with audio!)"""
        if not VLC_SUPPORT:
            messagebox.showwarning("VLC Not Found", 
                "VLC media player is not installed.\n\n"
                "To watch videos with audio:\n"
                "1. Install VLC: https://www.videolan.org/\n"
                "2. Install python-vlc: pip install python-vlc\n\n"
                "Or use Export to watch externally.")
            return
        
        item = self.media_items[index]
        
        # Create video player window
        player_window = ctk.CTkToplevel(self.root)
        player_window.title(f"🎬 {item['name']}")
        player_window.geometry("1000x700")
        
        try:
            # Decrypt video to temporary file
            encrypted_data = self.load_encrypted_file(item['file_path'])
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Create temp file
            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=Path(item['name']).suffix)
            temp_video.write(decrypted_data)
            temp_video.close()
            
            # Create VLC instance
            vlc_instance = vlc.Instance('--no-xlib')
            media_player = vlc_instance.media_player_new()
            
            # Create frame for video
            video_frame = ctk.CTkFrame(player_window, fg_color="black")
            video_frame.pack(expand=True, fill="both", padx=10, pady=10)
            
            # Get the window ID for embedding VLC
            if os.name == 'nt':  # Windows
                media_player.set_hwnd(video_frame.winfo_id())
            else:  # Linux/Mac
                media_player.set_xwindow(video_frame.winfo_id())
            
            # Load media
            media = vlc_instance.media_new(temp_video.name)
            media_player.set_media(media)
            
            # Parse media to get duration (important!)
            media.parse()
            
            # Control frame
            control_frame = ctk.CTkFrame(player_window)
            control_frame.pack(fill="x", padx=10, pady=10)
            
            # Progress slider
            progress_frame = ctk.CTkFrame(control_frame)
            progress_frame.pack(fill="x", pady=5)
            
            time_label = ctk.CTkLabel(progress_frame, text="Loading...", width=120)
            time_label.pack(side="left", padx=5)
            
            progress_var = ctk.DoubleVar(value=0)
            progress_slider = ctk.CTkSlider(progress_frame, from_=0, to=100, variable=progress_var)
            progress_slider.pack(side="left", fill="x", expand=True, padx=5)
            
            # Playback state
            is_playing = {'state': False, 'seeking': False, 'update_id': None}
            
            def format_time(milliseconds):
                """Convert milliseconds to MM:SS format"""
                if milliseconds <= 0:
                    return "00:00"
                seconds = int(milliseconds / 1000)
                mins = seconds // 60
                secs = seconds % 60
                return f"{mins:02d}:{secs:02d}"
            
            def update_progress():
                """Update progress bar and time - runs continuously"""
                try:
                    # Always update if player exists, even if paused
                    state = media_player.get_state()
                    
                    # Get current position and length
                    length = media_player.get_length()
                    current = media_player.get_time()
                    
                    # Update time display
                    if length > 0 and current >= 0:
                        if not is_playing['seeking']:
                            position = (current / length) * 100
                            progress_var.set(position)
                        time_label.configure(text=f"{format_time(current)} / {format_time(length)}")
                    elif length > 0:
                        time_label.configure(text=f"00:00 / {format_time(length)}")
                    
                    # Check if video ended
                    if state == vlc.State.Ended:
                        is_playing['state'] = False
                        play_btn.configure(text="▶ Replay")
                        progress_var.set(100)
                    
                    # Continue updating
                    is_playing['update_id'] = player_window.after(200, update_progress)
                    
                except Exception as e:
                    print(f"Update error: {e}")
                    is_playing['update_id'] = player_window.after(200, update_progress)
            
            def toggle_play():
                """Play or pause video"""
                state = media_player.get_state()
                
                if state == vlc.State.Ended:
                    # Restart from beginning
                    media_player.stop()
                    media_player.play()
                    is_playing['state'] = True
                    play_btn.configure(text="⏸ Pause")
                elif media_player.is_playing():
                    media_player.pause()
                    is_playing['state'] = False
                    play_btn.configure(text="▶ Play")
                else:
                    media_player.play()
                    is_playing['state'] = True
                    play_btn.configure(text="⏸ Pause")
            
            def stop_video():
                """Stop video playback"""
                media_player.stop()
                is_playing['state'] = False
                play_btn.configure(text="▶ Play")
                progress_var.set(0)
            
            def on_seek_start(value):
                """Called when user starts dragging slider"""
                is_playing['seeking'] = True
            
            def on_seek_end(value):
                """Called when user releases slider"""
                is_playing['seeking'] = False
                seek_video(value)
            
            def seek_video(value):
                """Seek to position"""
                try:
                    position = float(value) / 100.0
                    media_player.set_position(position)
                    # Force immediate update
                    length = media_player.get_length()
                    if length > 0:
                        new_time = int(length * position)
                        time_label.configure(text=f"{format_time(new_time)} / {format_time(length)}")
                except Exception as e:
                    print(f"Seek error: {e}")
            
            def volume_change(value):
                """Change volume"""
                media_player.audio_set_volume(int(value))
                volume_label.configure(text=f"🔊 {int(value)}%")
            
            def export_current():
                self.export_media(index)
            
            def close_player():
                """Clean up and close"""
                # Stop update loop
                if is_playing['update_id']:
                    player_window.after_cancel(is_playing['update_id'])
                # Stop player
                media_player.stop()
                media_player.release()
                # Delete temp file
                try:
                    os.unlink(temp_video.name)
                except:
                    pass
                player_window.destroy()
            
            # Button frame
            button_frame = ctk.CTkFrame(control_frame)
            button_frame.pack(pady=5)
            
            # Playback buttons
            play_btn = ctk.CTkButton(button_frame, text="▶ Play", command=toggle_play, 
                                    width=100, height=35)
            play_btn.pack(side="left", padx=5)
            
            stop_btn = ctk.CTkButton(button_frame, text="⏹ Stop", command=stop_video, 
                                    width=100, height=35)
            stop_btn.pack(side="left", padx=5)
            
            # Volume control
            volume_label = ctk.CTkLabel(button_frame, text="🔊 50%", width=60)
            volume_label.pack(side="left", padx=5)
            
            volume_slider = ctk.CTkSlider(button_frame, from_=0, to=100, width=150, 
                                         command=volume_change)
            volume_slider.set(50)
            volume_slider.pack(side="left", padx=5)
            
            # Export button
            export_btn = ctk.CTkButton(button_frame, text="📤 Export", command=export_current, 
                                      width=100, height=35, fg_color="green")
            export_btn.pack(side="left", padx=5)
            
            # Close button
            close_btn = ctk.CTkButton(button_frame, text="Close", command=close_player, 
                                     width=100, height=35)
            close_btn.pack(side="left", padx=5)
            
            # Bind slider seeking with proper event handling
            def slider_clicked(event):
                on_seek_start(progress_var.get())
            
            def slider_released(event):
                on_seek_end(progress_var.get())
            
            # Bind mouse events to slider
            progress_slider.bind("<Button-1>", slider_clicked)
            progress_slider.bind("<ButtonRelease-1>", slider_released)
            progress_slider.configure(command=lambda v: seek_video(v) if not is_playing['seeking'] else None)
            
            # Info label
            info_label = ctk.CTkLabel(control_frame, 
                text="🎬 Full video player with audio! Use controls to play/pause/seek/adjust volume",
                font=("Arial", 10), text_color="gray")
            info_label.pack(pady=5)
            
            # Handle window close
            player_window.protocol("WM_DELETE_WINDOW", close_player)
            
            # Start progress update loop immediately
            update_progress()
            
            # Auto-play after window is ready
            def auto_play():
                try:
                    # Start playback
                    media_player.play()
                    is_playing['state'] = True
                    play_btn.configure(text="⏸ Pause")
                    
                    # Wait a moment for VLC to initialize, then check duration
                    def check_ready():
                        length = media_player.get_length()
                        if length > 0:
                            time_label.configure(text=f"00:00 / {format_time(length)}")
                        else:
                            player_window.after(200, check_ready)
                    
                    player_window.after(300, check_ready)
                except Exception as e:
                    print(f"Auto-play error: {e}")
            
            player_window.after(800, auto_play)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not play video: {str(e)}")
            try:
                os.unlink(temp_video.name)
            except:
                pass
            player_window.destroy()
    
    def play_audio(self, index):
        """Play audio file with built-in player"""
        if not AUDIO_SUPPORT:
            messagebox.showerror("Audio Not Supported", 
                "pygame is not installed. Install it with:\npip install pygame")
            return
        
        item = self.media_items[index]
        
        # Create audio player window
        player = ctk.CTkToplevel(self.root)
        player.title(f"🎵 {item['name']}")
        player.geometry("500x400")
        
        try:
            # Decrypt audio to temporary file
            encrypted_data = self.load_encrypted_file(item['file_path'])
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Create temp file
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=Path(item['name']).suffix)
            temp_audio.write(decrypted_data)
            temp_audio.close()
            
            # Audio display
            title_label = ctk.CTkLabel(player, text="🎵 Audio Player", font=("Arial", 24, "bold"))
            title_label.pack(pady=20)
            
            name_label = ctk.CTkLabel(player, text=item['name'], font=("Arial", 14), wraplength=450)
            name_label.pack(pady=10)
            
            # Status label
            status_label = ctk.CTkLabel(player, text="Ready to play", font=("Arial", 16))
            status_label.pack(pady=20)
            
            # Playback state
            playing_state = {'playing': False}
            
            def toggle_play():
                if not playing_state['playing']:
                    try:
                        pygame.mixer.music.load(temp_audio.name)
                        pygame.mixer.music.play()
                        playing_state['playing'] = True
                        play_btn.configure(text="⏸ Pause")
                        status_label.configure(text="♪ Playing... ♪")
                        check_playback()
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not play audio: {str(e)}")
                else:
                    pygame.mixer.music.pause()
                    playing_state['playing'] = False
                    play_btn.configure(text="▶ Play")
                    status_label.configure(text="Paused")
            
            def resume_play():
                if playing_state['playing']:
                    pygame.mixer.music.unpause()
                    status_label.configure(text="♪ Playing... ♪")
            
            def stop_audio():
                pygame.mixer.music.stop()
                playing_state['playing'] = False
                play_btn.configure(text="▶ Play")
                status_label.configure(text="Stopped")
            
            def check_playback():
                # Check if audio is still playing
                if playing_state['playing'] and not pygame.mixer.music.get_busy():
                    status_label.configure(text="Finished")
                    playing_state['playing'] = False
                    play_btn.configure(text="▶ Play")
                elif playing_state['playing']:
                    player.after(100, check_playback)
            
            def export_current():
                self.export_media(index)
            
            def close_player():
                pygame.mixer.music.stop()
                try:
                    os.unlink(temp_audio.name)
                except:
                    pass
                player.destroy()
            
            # Control frame
            control_frame = ctk.CTkFrame(player)
            control_frame.pack(pady=20)
            
            play_btn = ctk.CTkButton(control_frame, text="▶ Play", command=toggle_play, 
                                    width=120, height=40, font=("Arial", 14))
            play_btn.pack(pady=5)
            
            stop_btn = ctk.CTkButton(control_frame, text="⏹ Stop", command=stop_audio, 
                                    width=120, height=40)
            stop_btn.pack(pady=5)
            
            export_btn = ctk.CTkButton(control_frame, text="📤 Export", command=export_current, 
                                      width=120, height=40, fg_color="green")
            export_btn.pack(pady=5)
            
            close_btn = ctk.CTkButton(control_frame, text="Close", command=close_player, 
                                     width=120, height=40)
            close_btn.pack(pady=5)
            
            # Handle window close
            player.protocol("WM_DELETE_WINDOW", close_player)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load audio: {str(e)}")
            try:
                os.unlink(temp_audio.name)
            except:
                pass
            player.destroy()
    
    def view_video_info(self, index):
        """Show video info and export option"""
        item = self.media_items[index]
        
        info_window = ctk.CTkToplevel(self.root)
        info_window.title("Video Info")
        info_window.geometry("400x300")
        
        title_label = ctk.CTkLabel(info_window, text="🎬 Video File", font=("Arial", 20, "bold"))
        title_label.pack(pady=20)
        
        name_label = ctk.CTkLabel(info_window, text=f"Name: {item['name']}", font=("Arial", 14))
        name_label.pack(pady=10)
        
        info_text = ctk.CTkLabel(
            info_window,
            text="Click Play to watch the video\ninside the app!",
            font=("Arial", 12),
            text_color="gray"
        )
        info_text.pack(pady=10)
        
        play_btn = ctk.CTkButton(
            info_window,
            text="▶ Play Video",
            command=lambda: [info_window.destroy(), self.play_video(index)],
            width=200,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="purple"
        )
        play_btn.pack(pady=10)
        
        export_btn = ctk.CTkButton(
            info_window,
            text="📤 Export Video",
            command=lambda: [self.export_media(index), info_window.destroy()],
            width=200,
            height=40,
            fg_color="green"
        )
        export_btn.pack(pady=20)
        
        close_btn = ctk.CTkButton(info_window, text="Close", command=info_window.destroy)
        close_btn.pack(pady=10)
    
    def view_media(self, index):
        """Universal media viewer with keyboard navigation for images and videos"""
        self.open_universal_viewer(index)
    
    def open_universal_viewer(self, start_index):
        """Universal viewer that handles images, videos, and audio with keyboard shortcuts"""
        if start_index < 0 or start_index >= len(self.media_items):
            return
        
        self.current_index = start_index
        
        # Get filtered items based on current folder (folder-aware navigation)
        viewing_items = self.get_filtered_items()
        
        # Create viewer window
        viewer = ctk.CTkToplevel(self.root)
        viewer.title("Media Viewer")
        viewer.geometry("1200x800")
        viewer.focus()
        
        # Fullscreen state
        fullscreen_state = {'is_fullscreen': False}
        
        # Playback settings
        playback_settings = {
            'autoplay': True,
            'shuffle': False
        }
        
        # Store current media type and player references
        current_media = {
            'type': None,
            'vlc_instance': None,
            'media_player': None,
            'temp_file': None,
            'is_playing': False,
            'update_id': None
        }
        
        # Main container
        main_frame = ctk.CTkFrame(viewer)
        main_frame.pack(expand=True, fill="both")
        
        # Content frame (for image or video)
        content_frame = ctk.CTkFrame(main_frame, fg_color="black")
        content_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Control bar at bottom
        control_bar = ctk.CTkFrame(main_frame)
        control_bar.pack(fill="x", padx=10, pady=5)
        
        # Info label
        info_label = ctk.CTkLabel(control_bar, text="", font=("Arial", 12))
        info_label.pack(side="left", padx=10)
        
        # Playback settings frame
        settings_frame = ctk.CTkFrame(control_bar)
        settings_frame.pack(side="left", padx=10)
        
        # AutoPlay toggle
        autoplay_switch = ctk.CTkSwitch(settings_frame, text="AutoPlay", 
                                        command=lambda: toggle_setting('autoplay'))
        autoplay_switch.select()  # On by default
        autoplay_switch.pack(side="left", padx=5)
        
        # Shuffle toggle
        shuffle_switch = ctk.CTkSwitch(settings_frame, text="Shuffle", 
                                       command=lambda: toggle_setting('shuffle'))
        shuffle_switch.pack(side="left", padx=5)
        
        def toggle_setting(setting):
            """Toggle playback setting"""
            if setting == 'autoplay':
                playback_settings['autoplay'] = autoplay_switch.get()
            elif setting == 'shuffle':
                playback_settings['shuffle'] = shuffle_switch.get()
        
        # Media controls frame (for videos)
        media_controls = ctk.CTkFrame(control_bar)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(control_bar)
        nav_frame.pack(side="right", padx=10)
        
        def update_info():
            """Update info label with current media info"""
            item = self.media_items[self.current_index]
            file_ext = Path(item['name']).suffix.lower()
            media_type = "Image" if file_ext in self.IMAGE_FORMATS else "Video" if file_ext in self.VIDEO_FORMATS else "Audio"
            
            # Show position in filtered items, not all items
            current_pos = viewing_items.index(item) + 1 if item in viewing_items else 0
            folder_text = f" [{self.current_folder}]" if self.current_folder != "All Media" else ""
            info_label.configure(text=f"{media_type} {current_pos}/{len(viewing_items)}{folder_text}: {item['name']}")
        
        def cleanup_current_media():
            """Clean up current media resources"""
            if current_media['update_id']:
                viewer.after_cancel(current_media['update_id'])
                current_media['update_id'] = None
            
            if current_media['media_player']:
                try:
                    current_media['media_player'].stop()
                    current_media['media_player'].release()
                except:
                    pass
                current_media['media_player'] = None
            
            if current_media['vlc_instance']:
                try:
                    current_media['vlc_instance'].release()
                except:
                    pass
                current_media['vlc_instance'] = None
            
            if current_media['temp_file']:
                try:
                    os.unlink(current_media['temp_file'])
                except:
                    pass
                current_media['temp_file'] = None
            
            # Clear content frame
            for widget in content_frame.winfo_children():
                widget.destroy()
        
        def load_media(index):
            """Load and display media at given index"""
            if index < 0 or index >= len(self.media_items):
                return
            
            self.current_index = index
            cleanup_current_media()
            
            item = self.media_items[index]
            file_ext = Path(item['name']).suffix.lower()
            
            update_info()
            
            # Determine media type
            if file_ext in self.IMAGE_FORMATS:
                load_image(index)
                media_controls.pack_forget()
                # Auto-advance for images if autoplay is on
                if playback_settings['autoplay']:
                    viewer.after(3000, try_next_media)  # 3 seconds per image
            elif file_ext in self.VIDEO_FORMATS:
                load_video(index)
                media_controls.pack(side="left", fill="x", expand=True, padx=10)
            elif file_ext in self.AUDIO_FORMATS:
                load_audio_viewer(index)
                media_controls.pack(side="left", fill="x", expand=True, padx=10)
        
        def load_image(index):
            """Load and display image"""
            current_media['type'] = 'image'
            item = self.media_items[index]
            
            try:
                encrypted_data = self.load_encrypted_file(item['file_path'])
                decrypted_data = self.cipher.decrypt(encrypted_data)
                
                image = Image.open(io.BytesIO(decrypted_data))
                
                # Get content frame size
                viewer.update_idletasks()
                max_w = content_frame.winfo_width() - 20
                max_h = content_frame.winfo_height() - 20
                
                # Resize image to fit
                img_w, img_h = image.size
                scale = min(max_w/img_w, max_h/img_h, 1.0)
                new_w = int(img_w * scale)
                new_h = int(img_h * scale)
                
                photo = ctk.CTkImage(light_image=image, dark_image=image, size=(new_w, new_h))
                
                img_label = ctk.CTkLabel(content_frame, image=photo, text="")
                img_label.image = photo
                img_label.pack(expand=True)
                
            except Exception as e:
                error_label = ctk.CTkLabel(content_frame, text=f"Error loading image: {str(e)}", 
                                          text_color="red", font=("Arial", 14))
                error_label.pack(expand=True)
        
        def load_video(index):
            """Load and display video with VLC"""
            if not VLC_SUPPORT:
                error_label = ctk.CTkLabel(content_frame, 
                    text="VLC not available\nInstall from: https://www.videolan.org/", 
                    text_color="red", font=("Arial", 14))
                error_label.pack(expand=True)
                return
            
            current_media['type'] = 'video'
            item = self.media_items[index]
            
            try:
                # Decrypt video to temp file
                encrypted_data = self.load_encrypted_file(item['file_path'])
                decrypted_data = self.cipher.decrypt(encrypted_data)
                
                temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=Path(item['name']).suffix)
                temp_video.write(decrypted_data)
                temp_video.close()
                current_media['temp_file'] = temp_video.name
                
                # Create VLC player
                vlc_instance = vlc.Instance('--no-xlib')
                media_player = vlc_instance.media_player_new()
                current_media['vlc_instance'] = vlc_instance
                current_media['media_player'] = media_player
                
                # Embed in frame
                if os.name == 'nt':
                    media_player.set_hwnd(content_frame.winfo_id())
                else:
                    media_player.set_xwindow(content_frame.winfo_id())
                
                # Load media
                media = vlc_instance.media_new(temp_video.name)
                media_player.set_media(media)
                media.parse()
                
                # Setup video controls
                setup_video_controls()
                
                # Auto-play
                def auto_play():
                    media_player.play()
                    current_media['is_playing'] = True
                    play_pause_btn.configure(text="⏸")
                    update_video_progress()
                    # Start checking for video end
                    check_video_end()
                
                viewer.after(500, auto_play)
                
            except Exception as e:
                error_label = ctk.CTkLabel(content_frame, text=f"Error loading video: {str(e)}", 
                                          text_color="red", font=("Arial", 14))
                error_label.pack(expand=True)
        
        def load_audio_viewer(index):
            """Load audio with visual player"""
            current_media['type'] = 'audio'
            item = self.media_items[index]
            
            # Show audio icon
            audio_label = ctk.CTkLabel(content_frame, text="🎵\n\nAudio File", 
                                      font=("Arial", 48, "bold"))
            audio_label.pack(expand=True)
            
            name_label = ctk.CTkLabel(content_frame, text=item['name'], 
                                     font=("Arial", 16), wraplength=600)
            name_label.pack(pady=20)
            
            # Setup audio playback (simplified for now)
            # Could expand with pygame mixer here
        
        def format_time(ms):
            """Format milliseconds to MM:SS"""
            if ms <= 0:
                return "00:00"
            secs = int(ms / 1000)
            mins = secs // 60
            secs = secs % 60
            return f"{mins:02d}:{secs:02d}"
        
        def update_video_progress():
            """Update video progress - accessible from anywhere"""
            try:
                if current_media['media_player'] and 'progress_var' in current_media:
                    length = current_media['media_player'].get_length()
                    current_time = current_media['media_player'].get_time()
                    
                    if length > 0 and current_time >= 0:
                        pos = (current_time / length) * 100
                        current_media['progress_var'].set(pos)
                        current_media['time_label'].configure(
                            text=f"{format_time(current_time)} / {format_time(length)}"
                        )
                    
                    current_media['update_id'] = viewer.after(200, update_video_progress)
            except Exception as e:
                print(f"Progress update error: {e}")
        
        def setup_video_controls():
            """Setup video playback controls"""
            # Clear existing controls
            for widget in media_controls.winfo_children():
                widget.destroy()
            
            # Time label
            time_label = ctk.CTkLabel(media_controls, text="00:00 / 00:00", width=100)
            time_label.pack(side="left", padx=5)
            
            # Progress slider
            progress_var = ctk.DoubleVar(value=0)
            progress_slider = ctk.CTkSlider(media_controls, from_=0, to=100, variable=progress_var, width=300)
            progress_slider.pack(side="left", fill="x", expand=True, padx=5)
            
            # Playback buttons
            global play_pause_btn
            play_pause_btn = ctk.CTkButton(media_controls, text="⏸", width=40, 
                                          command=toggle_video_play)
            play_pause_btn.pack(side="left", padx=2)
            
            # Volume
            volume_var = ctk.DoubleVar(value=50)
            volume_slider = ctk.CTkSlider(media_controls, from_=0, to=100, variable=volume_var, 
                                         width=100, command=lambda v: set_volume(v))
            volume_slider.pack(side="left", padx=5)
            
            vol_label = ctk.CTkLabel(media_controls, text="🔊", width=30)
            vol_label.pack(side="left")
            
            def seek_video(value):
                if current_media['media_player']:
                    pos = float(value) / 100.0
                    current_media['media_player'].set_position(pos)
            
            def set_volume(value):
                if current_media['media_player']:
                    current_media['media_player'].audio_set_volume(int(value))
            
            progress_slider.configure(command=seek_video)
            
            # Store for keyboard shortcuts and updates
            current_media['time_label'] = time_label
            current_media['progress_var'] = progress_var
            current_media['progress_slider'] = progress_slider
        
        def toggle_video_play():
            """Toggle video play/pause"""
            if current_media['media_player']:
                if current_media['media_player'].is_playing():
                    current_media['media_player'].pause()
                    current_media['is_playing'] = False
                    play_pause_btn.configure(text="▶")
                else:
                    current_media['media_player'].play()
                    current_media['is_playing'] = True
                    play_pause_btn.configure(text="⏸")
        
        def skip_forward():
            """Skip forward 10 seconds"""
            if current_media['media_player']:
                current_time = current_media['media_player'].get_time()
                current_media['media_player'].set_time(current_time + 10000)
        
        def skip_backward():
            """Skip backward 10 seconds"""
            if current_media['media_player']:
                current_time = current_media['media_player'].get_time()
                new_time = max(0, current_time - 10000)
                current_media['media_player'].set_time(new_time)
        
        def toggle_fullscreen():
            """Toggle fullscreen mode"""
            if fullscreen_state['is_fullscreen']:
                viewer.attributes('-fullscreen', False)
                control_bar.pack(fill="x", padx=10, pady=5)
                fullscreen_state['is_fullscreen'] = False
                # Reload media to resize properly
                viewer.after(100, lambda: load_media(self.current_index))
            else:
                viewer.attributes('-fullscreen', True)
                control_bar.pack_forget()
                fullscreen_state['is_fullscreen'] = True
                # Reload media to resize properly
                viewer.after(100, lambda: load_media(self.current_index))
        
        def get_next_index():
            """Get next index based on folder-aware navigation and shuffle"""
            current_item = self.media_items[self.current_index]
            if current_item not in viewing_items:
                return self.current_index
            
            current_pos = viewing_items.index(current_item)
            
            if playback_settings['shuffle']:
                # Random shuffle (exclude current)
                import random
                available = [i for i in range(len(viewing_items)) if i != current_pos]
                if available:
                    next_pos = random.choice(available)
                    return self.media_items.index(viewing_items[next_pos])
                return self.current_index
            else:
                # Sequential next
                if current_pos < len(viewing_items) - 1:
                    return self.media_items.index(viewing_items[current_pos + 1])
                return self.current_index
        
        def get_previous_index():
            """Get previous index based on folder-aware navigation"""
            current_item = self.media_items[self.current_index]
            if current_item not in viewing_items:
                return self.current_index
            
            current_pos = viewing_items.index(current_item)
            if current_pos > 0:
                return self.media_items.index(viewing_items[current_pos - 1])
            return self.current_index
        
        def show_next():
            """Show next media (folder-aware)"""
            next_idx = get_next_index()
            if next_idx != self.current_index:
                load_media(next_idx)
        
        def show_previous():
            """Show previous media (folder-aware)"""
            prev_idx = get_previous_index()
            if prev_idx != self.current_index:
                load_media(prev_idx)
        
        def try_next_media():
            """Try to advance to next media if autoplay is on"""
            if playback_settings['autoplay']:
                show_next()
        
        def check_video_end():
            """Check if video ended and autoplay next"""
            if current_media['media_player'] and current_media['type'] == 'video':
                state = current_media['media_player'].get_state()
                # VLC state 6 = Ended
                if state == 6 and playback_settings['autoplay']:
                    viewer.after(500, show_next)
                elif state != 6:
                    viewer.after(1000, check_video_end)
        
        def export_current():
            """Export current media"""
            self.export_media(self.current_index)
        
        def close_viewer():
            """Close viewer and cleanup"""
            cleanup_current_media()
            viewer.destroy()
        
        # Keyboard shortcuts
        def on_key_press(event):
            key = event.keysym.lower()
            
            # Navigation
            if key == 'right':
                show_next()
            elif key == 'left':
                show_previous()
            
            # Video controls
            elif key == 'space':
                if current_media['type'] == 'video':
                    toggle_video_play()
            elif key == 'f':
                toggle_fullscreen()
            elif key == 'escape':
                if fullscreen_state['is_fullscreen']:
                    toggle_fullscreen()
                else:
                    close_viewer()
            
            # Video seeking
            elif current_media['type'] == 'video':
                if key == 'l':  # Forward
                    skip_forward()
                elif key == 'j':  # Backward
                    skip_backward()
                elif key == 'k':  # Pause
                    toggle_video_play()
            
            return "break"
        
        # Bind keyboard events
        viewer.bind('<Key>', on_key_press)
        viewer.bind('<Left>', on_key_press)
        viewer.bind('<Right>', on_key_press)
        viewer.bind('<space>', on_key_press)
        viewer.bind('<Escape>', on_key_press)
        
        # Navigation buttons
        prev_btn = ctk.CTkButton(nav_frame, text="◀ Previous (←)", command=show_previous, width=130)
        prev_btn.pack(side="left", padx=2)
        
        export_btn = ctk.CTkButton(nav_frame, text="📤 Export", command=export_current, 
                                   width=100, fg_color="green")
        export_btn.pack(side="left", padx=2)
        
        next_btn = ctk.CTkButton(nav_frame, text="Next (→) ▶", command=show_next, width=130)
        next_btn.pack(side="left", padx=2)
        
        fullscreen_btn = ctk.CTkButton(nav_frame, text="⛶ Fullscreen (F)", command=toggle_fullscreen, width=130)
        fullscreen_btn.pack(side="left", padx=2)
        
        close_btn = ctk.CTkButton(nav_frame, text="Close (Esc)", command=close_viewer, width=100)
        close_btn.pack(side="left", padx=2)
        
        # Shortcuts hint
        hint_label = ctk.CTkLabel(control_bar, 
            text="⌨️ Shortcuts: ←→ Navigate | Space: Play/Pause | J/L: ±10s | F: Fullscreen | Esc: Close",
            font=("Arial", 9), text_color="gray")
        hint_label.pack(side="bottom", pady=2)
        
        # Handle window close
        viewer.protocol("WM_DELETE_WINDOW", close_viewer)
        
        # Load initial media
        load_media(start_index)
    
    def add_folder(self):
        """Add entire folder to vault"""
        folder = filedialog.askdirectory(title="Select Folder to Import")
        
        if not folder:
            return
        
        folder_path = Path(folder)
        
        # Find all media files in folder and subfolders
        media_extensions = self.IMAGE_FORMATS | self.VIDEO_FORMATS | self.AUDIO_FORMATS
        files_to_add = []
        
        for root, dirs, files in os.walk(folder):
            for file in files:
                if Path(file).suffix.lower() in media_extensions:
                    files_to_add.append(os.path.join(root, file))
        
        if not files_to_add:
            messagebox.showinfo("No Media Found", "No media files found in the selected folder")
            return
        
        # Ask if they want to delete the entire folder
        response = messagebox.askyesno(
            "Import and Delete Folder?", 
            f"Found {len(files_to_add)} media file(s) in:\n{folder_path.name}\n\n" +
            "Do you want to:\n" +
            "✓ Import all media to vault\n" +
            "✓ DELETE the entire folder\n\n" +
            "YES = Import and delete folder\n" +
            "NO = Cancel",
            icon='warning'
        )
        
        if response:
            # Import files
            self.import_files(files_to_add, delete_original=False)  # We'll delete folder manually
            
            # Delete entire folder
            try:
                shutil.rmtree(folder)
                messagebox.showinfo("Success", 
                    f"Imported {len(files_to_add)} files\n" +
                    f"Deleted folder: {folder_path.name}")
            except Exception as e:
                messagebox.showwarning("Partial Success", 
                    f"Files imported but could not delete folder:\n{str(e)}")
            
            self.show_main_screen()
    
    def add_media(self):
        """Add media files to vault"""
        # Build file type strings
        image_types = " ".join([f"*{ext}" for ext in self.IMAGE_FORMATS])
        video_types = " ".join([f"*{ext}" for ext in self.VIDEO_FORMATS])
        audio_types = " ".join([f"*{ext}" for ext in self.AUDIO_FORMATS])
        
        files = filedialog.askopenfilenames(
            title="Select Media Files",
            filetypes=[
                ("All Media", f"{image_types} {video_types} {audio_types}"),
                ("Images", image_types), 
                ("Videos", video_types),
                ("Audio", audio_types),
                ("All Files", "*.*")
            ]
        )
        
        if not files:
            return
        
        # Ask user if they want to delete originals
        delete_original = messagebox.askyesno(
            "Delete Original Files?",
            "Do you want to DELETE the original files after importing?\n\n" +
            "YES = Move files (originals deleted)\n" +
            "NO = Copy files (originals kept)",
            icon='warning'
        )
        
        self.import_files(files, delete_original)
    
    def import_files(self, files, delete_original=False):
        """Import files into vault"""
        success_count = 0
        
        for file_path in files:
            try:
                # Read original file
                with open(file_path, 'rb') as f:
                    data = f.read()
                
                # Encrypt data
                encrypted_data = self.cipher.encrypt(data)
                
                # Generate unique filename
                file_id = hashlib.md5(os.urandom(16)).hexdigest()
                encrypted_path = self.vault_dir / f"{file_id}.enc"
                
                # Save encrypted file
                with open(encrypted_path, 'wb') as f:
                    f.write(encrypted_data)
                
                # Detect file type
                file_ext = Path(file_path).suffix.lower()
                if file_ext in self.IMAGE_FORMATS:
                    file_type = 'image'
                elif file_ext in self.VIDEO_FORMATS:
                    file_type = 'video'
                elif file_ext in self.AUDIO_FORMATS:
                    file_type = 'audio'
                else:
                    file_type = 'unknown'
                
                # Add to index
                self.media_items.append({
                    'name': Path(file_path).name,
                    'file_path': str(encrypted_path),
                    'type': file_type
                })
                
                # Delete original file if requested
                if delete_original:
                    try:
                        os.remove(file_path)
                    except Exception as del_error:
                        print(f"Could not delete original: {del_error}")
                
                success_count += 1
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not import {Path(file_path).name}: {str(e)}")
        
        self.save_media_index()
        
        if delete_original:
            messagebox.showinfo("Success", f"Moved {success_count} file(s) to vault\n(Originals deleted)")
        else:
            messagebox.showinfo("Success", f"Copied {success_count} file(s) to vault")
        
        self.show_main_screen()
    
    def export_media(self, index):
        """Export media from vault back to computer"""
        item = self.media_items[index]
        
        # Ask where to save
        file_path = filedialog.asksaveasfilename(
            title="Export File As",
            initialfile=item['name'],
            defaultextension=Path(item['name']).suffix,
            filetypes=[("All Files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Load and decrypt
            encrypted_data = self.load_encrypted_file(item['file_path'])
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Save to chosen location
            with open(file_path, 'wb') as f:
                f.write(decrypted_data)
            
            messagebox.showinfo("Success", f"Exported to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not export file:\n{str(e)}")
    
    def move_to_folder_dialog(self, index, item):
        """Show dialog to move item to a folder"""
        # Create dialog window
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Move to Folder")
        dialog.geometry("400x500")
        dialog.grab_set()  # Make it modal
        
        title = ctk.CTkLabel(dialog, text=f"Move '{item['name'][:30]}...'", 
                            font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(dialog, text="Select destination folder:", 
                               font=("Arial", 12))
        subtitle.pack(pady=10)
        
        # Scrollable frame for folder list
        scroll_frame = ctk.CTkScrollableFrame(dialog, width=350, height=250)
        scroll_frame.pack(pady=10, padx=20)
        
        current_folder = item.get('folder', None)
        
        # "No Folder" option
        no_folder_btn = ctk.CTkButton(
            scroll_frame,
            text="📂 No Folder (All Media)",
            command=lambda: move_and_close(None),
            width=300,
            fg_color="blue" if current_folder is None else "gray"
        )
        no_folder_btn.pack(pady=5)
        
        # Existing folders
        for folder in self.folders:
            folder_btn = ctk.CTkButton(
                scroll_frame,
                text=f"📁 {folder}",
                command=lambda f=folder: move_and_close(f),
                width=300,
                fg_color="blue" if current_folder == folder else "gray"
            )
            folder_btn.pack(pady=5)
        
        def move_and_close(target_folder):
            """Move item to folder and close dialog"""
            item['folder'] = target_folder
            self.save_media_index()
            dialog.destroy()
            self.show_main_screen()
        
        # Create new folder button
        new_folder_btn = ctk.CTkButton(
            dialog,
            text="➕ Create New Folder",
            command=lambda: create_folder_and_move(),
            width=200,
            fg_color="green"
        )
        new_folder_btn.pack(pady=10)
        
        def create_folder_and_move():
            """Create new folder and move item there"""
            input_dialog = ctk.CTkInputDialog(text="Enter new folder name:", title="Create Folder")
            folder_name = input_dialog.get_input()
            
            if folder_name:
                if folder_name not in self.folders and folder_name != "All Media":
                    self.folders.append(folder_name)
                    item['folder'] = folder_name
                    self.save_media_index()
                    dialog.destroy()
                    messagebox.showinfo("Success", f"Created folder '{folder_name}' and moved item")
                    self.show_main_screen()
                else:
                    messagebox.showwarning("Error", "Folder already exists or invalid name")
        
        # Cancel button
        cancel_btn = ctk.CTkButton(dialog, text="Cancel", command=dialog.destroy, width=150)
        cancel_btn.pack(pady=10)
    
    def delete_media(self, index):
        """Delete media from vault"""
        item = self.media_items[index]
        
        if messagebox.askyesno("Confirm Delete", 
            f"Delete '{item['name']}' from vault?\n\nThis cannot be undone!"):
            
            # Delete encrypted file
            try:
                Path(item['file_path']).unlink()
            except:
                pass
            
            # Remove from index
            self.media_items.pop(index)
            self.save_media_index()
            
            self.show_main_screen()
    
    def load_encrypted_file(self, file_path):
        """Load encrypted file"""
        with open(file_path, 'rb') as f:
            return f.read()
    
    def save_media_index(self):
        """Save encrypted media index with folders"""
        if self.cipher:
            vault_data = {
                'media_items': self.media_items,
                'folders': self.folders
            }
            index_data = json.dumps(vault_data).encode()
            encrypted_index = self.cipher.encrypt(index_data)
            
            with open(self.media_index_file, 'wb') as f:
                f.write(encrypted_index)
    
    def load_media_index(self):
        """Load and decrypt media index with folders"""
        if self.media_index_file.exists():
            try:
                with open(self.media_index_file, 'rb') as f:
                    encrypted_index = f.read()
                
                decrypted_index = self.cipher.decrypt(encrypted_index)
                vault_data = json.loads(decrypted_index.decode())
                
                # Support old format (just media_items) and new format (with folders)
                if isinstance(vault_data, list):
                    # Old format
                    self.media_items = vault_data
                    self.folders = []
                else:
                    # New format
                    self.media_items = vault_data.get('media_items', [])
                    self.folders = vault_data.get('folders', [])
            except:
                self.media_items = []
                self.folders = []
        else:
            self.media_items = []
            self.folders = []
    
    def show_watched_folder_info(self):
        """Show info about auto-import folder"""
        msg = f"📂 Auto-Import Folder:\n{self.watched_dir}\n\n" + \
              "📌 How it works:\n" + \
              "1. Drop ANY file into this folder\n" + \
              "2. It's automatically encrypted within 2 seconds\n" + \
              "3. Added to your vault\n" + \
              "4. Original file deleted\n\n" + \
              "💡 Tip: Create a desktop shortcut to this folder!"
        
        result = messagebox.askquestion(
            "Auto-Import Folder",
            msg + "\n\nOpen this folder now?",
            icon='info'
        )
        
        if result == 'yes':
            os.startfile(self.watched_dir)
    
    def start_watching(self):
        """Start watching the auto-import folder"""
        if self.watching:
            return
        
        self.watching = True
        self.watch_thread = threading.Thread(target=self.watch_folder, daemon=True)
        self.watch_thread.start()
    
    def watch_folder(self):
        """Watch folder for new files and auto-encrypt them"""
        processed_files = set()
        
        while self.watching:
            try:
                files = list(self.watched_dir.glob('*'))
                files_added = False
                
                for file_path in files:
                    if file_path.is_file() and str(file_path) not in processed_files:
                        time.sleep(1)
                        
                        try:
                            with open(file_path, 'rb') as f:
                                data = f.read()
                            
                            encrypted_data = self.cipher.encrypt(data)
                            
                            file_id = hashlib.md5(os.urandom(16)).hexdigest()
                            encrypted_path = self.vault_dir / f"{file_id}.enc"
                            
                            with open(encrypted_path, 'wb') as f:
                                f.write(encrypted_data)
                            
                            # Determine file type
                            file_ext = file_path.suffix.lower()
                            if file_ext in self.IMAGE_FORMATS:
                                file_type = 'image'
                            elif file_ext in self.VIDEO_FORMATS:
                                file_type = 'video'
                            elif file_ext in self.AUDIO_FORMATS:
                                file_type = 'audio'
                            else:
                                file_type = 'unknown'
                            
                            self.media_items.append({
                                'name': file_path.name,
                                'file_path': str(encrypted_path),
                                'type': file_type
                            })
                            
                            self.save_media_index()
                            
                            file_path.unlink()
                            
                            processed_files.add(str(file_path))
                            files_added = True
                            
                            print(f"✓ Auto-imported: {file_path.name}")
                            
                        except Exception as e:
                            print(f"Error processing {file_path}: {e}")
                
                # Refresh gallery if files were added
                if files_added:
                    try:
                        self.root.after(0, self.show_main_screen)
                    except:
                        pass
                
                time.sleep(2)
                
            except Exception as e:
                print(f"Watch error: {e}")
                time.sleep(5)
    
    def lock_vault(self):
        """Lock the vault and return to login screen"""
        self.watching = False
        self.cipher = None
        self.media_items = []
        self.show_login_screen()
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing"""
        self.watching = False
        self.root.destroy()

if __name__ == "__main__":
    app = VaultApp()
    app.run()
