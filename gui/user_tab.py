import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from PIL import Image
import os

class UserTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        
        # Header
        header_f = ctk.CTkFrame(self, fg_color="transparent")
        header_f.pack(fill="x", padx=20, pady=(0, 20))
        
        self.header = ctk.CTkLabel(header_f, text="User Management", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.pack(side="left")
        
        self.stats_lbl = ctk.CTkLabel(header_f, text="Total Users: 0", font=ctk.CTkFont(size=14))
        self.stats_lbl.pack(side="right", padx=10)

        # Main scrollable area
        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=15, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.refresh_users()

    def refresh_users(self):
        # Clear existing cards
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        users = self.app.data_manager.load_users()
        self.stats_lbl.configure(text=f"Total Users: {len(users)}")
        
        for u in users:
            self._create_user_card(u)

    def _create_user_card(self, user):
        card = ctk.CTkFrame(self.scroll_frame, corner_radius=15, height=100)
        card.pack(fill="x", pady=10, padx=5)
        
        # User Info Left Side
        info_f = ctk.CTkFrame(card, fg_color="transparent")
        info_f.pack(side="left", padx=20, pady=15)
        
        # Avatar (Image or Initials)
        avatar_frame = ctk.CTkFrame(info_f, width=50, height=50, corner_radius=25, fg_color="transparent")
        avatar_frame.pack(side="left")
        avatar_frame.pack_propagate(False)
        
        has_img = False
        if hasattr(user, 'profile_image') and user.profile_image and os.path.exists(user.profile_image):
            try:
                from PIL import ImageOps, ImageDraw
                raw_img = Image.open(user.profile_image).convert("RGBA")
                
                # High quality circular masking (Antialiased)
                size = (50, 50)
                mask_multiplier = 4
                mask_size = (size[0] * mask_multiplier, size[1] * mask_multiplier)
                
                # Crop to square first
                raw_img = ImageOps.fit(raw_img, size, Image.Resampling.LANCZOS)
                
                # Create oversized mask
                mask = Image.new('L', mask_size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + mask_size, fill=255)
                
                # Downsample mask for smooth edges
                mask = mask.resize(size, Image.Resampling.LANCZOS)
                
                # Apply mask (circular crop)
                circular_img = Image.new('RGBA', size, (0, 0, 0, 0))
                circular_img.paste(raw_img, (0, 0), mask=mask)
                
                ctk_img = ctk.CTkImage(light_image=circular_img, dark_image=circular_img, size=size)
                lbl = ctk.CTkLabel(avatar_frame, image=ctk_img, text="", fg_color="transparent")
                lbl.image = ctk_img
                lbl.pack()
                has_img = True
            except:
                pass
        
        if not has_img:
            initials = (user.name[0] if user.name else "?").upper()
            ctk.CTkButton(avatar_frame, text=initials, width=50, height=50, corner_radius=25, 
                         fg_color="#3B8ED0" if user.role == "Admin" else "#28a745",
                         state="disabled", text_color="white", font=ctk.CTkFont(size=18, weight="bold")).pack()
        
        text_f = ctk.CTkFrame(info_f, fg_color="transparent")
        text_f.pack(side="left", padx=15)
        
        ctk.CTkLabel(text_f, text=user.name, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(text_f, text=user.email, font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w")
        
        # Role & Status Badges
        badge_f = ctk.CTkFrame(card, fg_color="transparent")
        badge_f.pack(side="left", padx=20)
        
        role_color = "#3B8ED0" if user.role == "Admin" else "gray40"
        ctk.CTkLabel(badge_f, text=user.role.upper(), fg_color=role_color, corner_radius=5, padx=8, font=ctk.CTkFont(size=10, weight="bold")).pack(side="left", padx=5)
        
        status_color = "#2fa572" if user.status == "Active" else "#dc3545"
        ctk.CTkLabel(badge_f, text=user.status.upper(), fg_color=status_color, corner_radius=5, padx=8, font=ctk.CTkFont(size=10, weight="bold")).pack(side="left", padx=5)

        # Actions Right Side
        act_f = ctk.CTkFrame(card, fg_color="transparent")
        act_f.pack(side="right", padx=20)
        
        # Block Button
        block_text = "🔓 Unblock" if user.status == "Blocked" else "🔒 Block"
        block_color = "#2fa572" if user.status == "Blocked" else "#e67e22"
        btn_block = ctk.CTkButton(act_f, text=block_text, width=100, fg_color=block_color, command=lambda u=user: self._toggle_block(u))
        btn_block.pack(side="left", padx=5)
        
        # Delete Button
        btn_del = ctk.CTkButton(act_f, text="🗑️ Delete", width=100, fg_color="#dc3545", hover_color="#c82333", command=lambda u=user: self._delete_user(u))
        btn_del.pack(side="left", padx=5)
        
        if user.user_id == self.app.current_user.user_id:
            btn_block.configure(state="disabled")
            btn_del.configure(state="disabled")

    def _toggle_block(self, user):
        all_users = self.app.data_manager.load_users()
        for u in all_users:
            if u.user_id == user.user_id:
                u.status = "Blocked" if u.status == "Active" else "Active"
                break
        self.app.data_manager.save_users(all_users)
        self.refresh_users()
        messagebox.showinfo("Success", f"User {user.name} status updated.")

    def _delete_user(self, user):
        if messagebox.askyesno("Confirm", f"Are you sure you want to PERMANENTLY delete {user.name}? This cannot be undone."):
            all_users = self.app.data_manager.load_users()
            all_users = [u for u in all_users if u.user_id != user.user_id]
            self.app.data_manager.save_users(all_users)
            self.refresh_users()
