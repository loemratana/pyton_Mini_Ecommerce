import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from models.user import Admin, Customer
from gui.theme import ModernTheme
from PIL import Image
import os
import shutil

class ProfileTab(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.profile_dir = os.path.join("assets", "profile_images")
        os.makedirs(self.profile_dir, exist_ok=True)
        
        # Header
        self.header = ctk.CTkLabel(self, text="Account Settings", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.pack(anchor="w", padx=20, pady=(0, 20))

        # Main Layout: Profile Pic on left, info on right
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20)

        # Profile Image Section (Left)
        img_section = ctk.CTkFrame(self.main_container, fg_color="transparent")
        img_section.pack(side="left", padx=(0, 30), anchor="n")
        
        # Card for image (Square for circle masking)
        img_card = ModernTheme.create_modern_card(img_section, corner_radius=100) 
        img_card.pack(pady=10)
        
        # Label with transparent background to allow the circle to show correctly
        self.image_label = ctk.CTkLabel(img_card, text="", font=("Arial", 60), fg_color="transparent")
        self.image_label.pack(padx=5, pady=5) # Reduced padding to fit 160x160 images better
        
        self.selected_img_path = tk.StringVar(value=self.app.current_user.profile_image or "")
        self._load_current_image()
        
        upload_btn = ctk.CTkButton(img_section, text="Upload Photo", 
                                  command=self._pick_profile_image,
                                  fg_color=ModernTheme.BG_SECONDARY,
                                  text_color=ModernTheme.TEXT_PRIMARY,
                                  hover_color=ModernTheme.BG_TERTIARY,
                                  width=150)
        upload_btn.pack(pady=10)

        # Profile Information Card (Right)
        self.profile_card = ctk.CTkFrame(self.main_container, corner_radius=15)
        self.profile_card.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(self.profile_card, text="Personal Information", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10), padx=20, anchor="w")
        
        # Name
        ctk.CTkLabel(self.profile_card, text="Full Name:").pack(padx=20, anchor="w")
        self.name_entry = ctk.CTkEntry(self.profile_card, width=400)
        self.name_entry.insert(0, self.app.current_user.name)
        self.name_entry.pack(pady=(5, 15), padx=20, anchor="w")
        
        # Email
        ctk.CTkLabel(self.profile_card, text="Email Address:").pack(padx=20, anchor="w")
        self.email_entry = ctk.CTkEntry(self.profile_card, width=400)
        self.email_entry.insert(0, self.app.current_user.email)
        self.email_entry.pack(pady=(5, 15), padx=20, anchor="w")
        
        # Role Badge
        role_color = ModernTheme.PRIMARY if self.app.current_user.role == "Admin" else ModernTheme.SUCCESS
        role_frame = ctk.CTkFrame(self.profile_card, fg_color=role_color, corner_radius=20)
        role_frame.pack(padx=20, pady=(0, 20), anchor="w")
        ctk.CTkLabel(role_frame, text=f"Role: {self.app.current_user.role.upper()}", font=ctk.CTkFont(size=12, weight="bold"), text_color="white").pack(padx=15, pady=5)

        # Update Button
        self.upd_btn = ctk.CTkButton(self.profile_card, text="💾 Save Changes", width=200, height=40, font=ctk.CTkFont(weight="bold"), command=self.update_profile)
        self.upd_btn.pack(pady=10, padx=20, anchor="w")

        # --- Password Change Section ---
        ctk.CTkLabel(self.profile_card, text="Security & Password", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10), padx=20, anchor="w")
        
        # New Password
        ctk.CTkLabel(self.profile_card, text="New Password:").pack(padx=20, anchor="w")
        self.pass_entry = ctk.CTkEntry(self.profile_card, width=400, show="*")
        self.pass_entry.pack(pady=(5, 10), padx=20, anchor="w")
        
        # Confirm Password
        ctk.CTkLabel(self.profile_card, text="Confirm New Password:").pack(padx=20, anchor="w")
        self.confirm_pass_entry = ctk.CTkEntry(self.profile_card, width=400, show="*")
        self.confirm_pass_entry.pack(pady=(5, 10), padx=20, anchor="w")

        # Password Update Button
        self.pass_upd_btn = ctk.CTkButton(self.profile_card, text="🔐 Update Password", width=200, height=40, 
                                          fg_color=ModernTheme.INFO, hover_color=ModernTheme.PRIMARY,
                                          font=ctk.CTkFont(weight="bold"), command=self.change_password)
        self.pass_upd_btn.pack(pady=(10, 20), padx=20, anchor="w")
        
        if isinstance(self.app.current_user, Admin):
            self.setup_admin_tools()

    def _load_current_image(self):
        img_path = self.app.current_user.profile_image
        if img_path and os.path.exists(img_path):
            try:
                self._display_circle_image(img_path)
            except: pass

    def _display_circle_image(self, path):
        from PIL import ImageOps, ImageDraw, Image
        raw_img = Image.open(path).convert("RGBA")
        
        # High quality circular masking (Antialiased)
        size = (160, 160)
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
        
        # Apply mask
        circular_img = Image.new('RGBA', size, (0, 0, 0, 0))
        circular_img.paste(raw_img, (0, 0), mask=mask)
        
        ctk_img = ctk.CTkImage(light_image=circular_img, dark_image=circular_img, size=size)
        self.image_label.configure(image=ctk_img, text="")
        self.image_label.image = ctk_img

    def _pick_profile_image(self):
        file = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.gif")])
        if file:
            self.selected_img_path.set(file)
            # Preview immediately
            try:
                self._display_circle_image(file)
            except:
                messagebox.showerror("Error", "Could not load selected image.")

    def setup_admin_tools(self):
        # Admin Tools Section
        admin_section = ctk.CTkFrame(self, corner_radius=15)
        admin_section.pack(pady=30, padx=20, fill="x")
        
        ctk.CTkLabel(admin_section, text="Administrative Controls", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20, padx=20, anchor="w")
        
        btn_container = ctk.CTkFrame(admin_section, fg_color="transparent")
        btn_container.pack(pady=(0, 25), padx=20, anchor="w")
        
        ctk.CTkButton(btn_container, text="Invite New Admin", command=self.add_new_admin, height=45).pack(side="left", padx=5)

    def update_profile(self):
        new_name = self.name_entry.get()
        new_email = self.email_entry.get()
        
        if not new_name or not new_email:
            messagebox.showwarning("Incomplete", "Name and email cannot be empty.")
            return

        # Handle Image Saving
        if self.selected_img_path.get() and self.selected_img_path.get() != self.app.current_user.profile_image:
            if os.path.exists(self.selected_img_path.get()):
                dest_name = f"user_{self.app.current_user.user_id}.jpg"
                dest_path = os.path.join(self.profile_dir, dest_name)
                shutil.copy(self.selected_img_path.get(), dest_path)
                self.app.current_user.profile_image = dest_path

        self.app.current_user.name = new_name
        self.app.current_user.email = new_email
        
        # Persist change to file
        all_users = self.app.data_manager.load_users()
        for i, u in enumerate(all_users):
            if u.user_id == self.app.current_user.user_id:
                all_users[i] = self.app.current_user
                break
        self.app.data_manager.save_users(all_users)
        
        messagebox.showinfo("Success", "Your profile has been updated successfully.")

    def change_password(self):
        new_pass = self.pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()
        
        if not new_pass:
            messagebox.showwarning("Incomplete", "Please enter a new password.")
            return
            
        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match.")
            return
            
        if len(new_pass) < 4:
            messagebox.showwarning("Weak Password", "Password must be at least 4 characters long.")
            return

        self.app.current_user.password = new_pass
        
        # Persist change to file
        all_users = self.app.data_manager.load_users()
        for i, u in enumerate(all_users):
            if u.user_id == self.app.current_user.user_id:
                all_users[i] = self.app.current_user
                break
        self.app.data_manager.save_users(all_users)
        
        self.pass_entry.delete(0, 'end')
        self.confirm_pass_entry.delete(0, 'end')
        messagebox.showinfo("Success", "Password updated successfully.")

    def add_new_admin(self):
        win = ctk.CTkToplevel(self)
        win.title("Create Admin Account")
        win.geometry("400x450")
        win.attributes("-topmost", True)
        
        ctk.CTkLabel(win, text="New Admin Account", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        # Fields
        ctk.CTkLabel(win, text="Full Name:").pack(pady=(10, 0))
        name_v = ctk.CTkEntry(win, width=300)
        name_v.pack(pady=5)
        
        ctk.CTkLabel(win, text="Email Address:").pack(pady=(10, 0))
        email_v = ctk.CTkEntry(win, width=300)
        email_v.pack(pady=5)
        
        ctk.CTkLabel(win, text="Security Password:").pack(pady=(10, 0))
        pass_v = ctk.CTkEntry(win, width=300, show="*")
        pass_v.pack(pady=5)
        
        def save():
            name = name_v.get()
            email = email_v.get()
            password = pass_v.get()
            
            if not name or not email or not password:
                return messagebox.showwarning("Missing Fields", "Please populate all fields.")
            
            users = self.app.data_manager.load_users()
            new_id = max([u.user_id for u in users], default=0) + 1
            new_admin = Admin(new_id, name, email, password)
            users.append(new_admin)
            self.app.data_manager.save_users(users)
            messagebox.showinfo("Success", "New Administrator successfully registered.")
            win.destroy()
            
        ctk.CTkButton(win, text="Register Administrator", command=save, height=45, font=ctk.CTkFont(weight="bold")).pack(pady=30)
