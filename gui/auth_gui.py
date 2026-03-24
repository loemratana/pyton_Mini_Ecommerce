import customtkinter as ctk
from tkinter import messagebox
from models.user import Customer, Admin
from gui.theme import ModernTheme

class AuthGUI:
    def __init__(self, root, data_manager, on_login_success):
        self.root = root
        
        # Initialize appearance after root exists
        ModernTheme.setup_appearance()
        self.data_manager = data_manager
        self.on_login_success = on_login_success
        self.users = self.data_manager.load_users()
        
        # Adjust root for customtkinter
        self.root.withdraw()
        self.main_window = ctk.CTkToplevel()
        self.main_window.title("Antigravity - Login")
        self.main_window.geometry("600x700")
        self.main_window.configure(fg_color=ModernTheme.BG_PRIMARY)
        self.main_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        
        # Center the window
        self._center_window(self.main_window, 600, 700)
        
        self.setup_login_screen()

    def _center_window(self, win, w, h):
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (w // 2)
        y = (screen_height // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    def clear_screen(self):
        for widget in self.main_window.winfo_children():
            widget.destroy()

    def setup_login_screen(self):
        self.clear_screen()
        self.main_window.title("Antigravity - Sign In")

        # Main outer frame with padding
        outer_frame = ctk.CTkFrame(self.main_window, fg_color="transparent")
        outer_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Main card frame
        main_frame = ModernTheme.create_modern_card(outer_frame, corner_radius=20)
        main_frame.pack(fill="both", expand=True)

        # Content padding frame
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=50)

        # Header
        header_label = ctk.CTkLabel(content_frame, text="✨ Welcome Back", 
                                    font=ModernTheme.get_header_font(),
                                    text_color=ModernTheme.PRIMARY)
        header_label.pack(pady=(0, 10))
        
        subheader_label = ctk.CTkLabel(content_frame, text="Sign in to your Antigravity account",
                                       font=ModernTheme.get_small_font(),
                                       text_color=ModernTheme.TEXT_SECONDARY)
        subheader_label.pack(pady=(0, 40))

        # Email field
        email_label = ctk.CTkLabel(content_frame, text="Email Address",
                                   font=ModernTheme.get_label_font(),
                                   text_color=ModernTheme.TEXT_PRIMARY)
        email_label.pack(anchor="w", pady=(15, 8))
        
        self.email_entry = ctk.CTkEntry(content_frame, width=300, height=50, 
                                         placeholder_text="you@example.com",
                                         fg_color=ModernTheme.SURFACE,
                                         border_color=ModernTheme.BORDER,
                                         border_width=1,
                                         text_color=ModernTheme.TEXT_PRIMARY)
        self.email_entry.pack(pady=(0, 20))

        # Password field
        pass_label = ctk.CTkLabel(content_frame, text="Password",
                                  font=ModernTheme.get_label_font(),
                                  text_color=ModernTheme.TEXT_PRIMARY)
        pass_label.pack(anchor="w", pady=(0, 8))
        
        self.pass_entry = ctk.CTkEntry(content_frame, width=300, height=50, 
                                        placeholder_text="Enter your password",
                                        show="•",
                                        fg_color=ModernTheme.SURFACE,
                                        border_color=ModernTheme.BORDER,
                                        border_width=1,
                                        text_color=ModernTheme.TEXT_PRIMARY)
        self.pass_entry.pack(pady=(0, 35))

        # Login button
        self.login_btn = ModernTheme.create_modern_button(content_frame, "Sign In", 
                                                          command=self.handle_login, 
                                                          color="primary", height=50, width=300)
        self.login_btn.pack(pady=(0, 20))

        # Register footer
        footer_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        footer_frame.pack(pady=(20, 0))
        
        no_account_label = ctk.CTkLabel(footer_frame, text="Don't have an account? ",
                                        font=ModernTheme.get_label_font(),
                                        text_color=ModernTheme.TEXT_SECONDARY)
        no_account_label.pack(side="left")
        
        register_link = ctk.CTkLabel(footer_frame, text="Create one",
                                     font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                                     text_color=ModernTheme.PRIMARY, cursor="hand2")
        register_link.pack(side="left")
        register_link.bind("<Button-1>", lambda e: self.setup_register_screen())

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get()
        
        if not email or not password:
            messagebox.showwarning("Missing Fields", "Please enter email and password.")
            return
        
        user = next((u for u in self.users if u.email == email and u.password == password), None)
        
        if user:
            if user.status == "Blocked":
                messagebox.showerror("Access Denied", "Your account has been suspended. Contact support.")
                return
            messagebox.showinfo("Success", f"Welcome back, {user.name}!")
            self.main_window.destroy()  # Destroy login window
            self.on_login_success(user)  # Show main app
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    def setup_register_screen(self):
        self.clear_screen()
        self.main_window.title("Antigravity - Create Account")

        # Main outer frame
        outer_frame = ctk.CTkFrame(self.main_window, fg_color="transparent")
        outer_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Main card frame
        main_frame = ModernTheme.create_modern_card(outer_frame, corner_radius=20)
        main_frame.pack(fill="both", expand=True)

        # Content padding frame
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=40, pady=40)

        # Header
        header_label = ctk.CTkLabel(content_frame, text="🚀 Join Us",
                                    font=ModernTheme.get_header_font(),
                                    text_color=ModernTheme.PRIMARY)
        header_label.pack(pady=(0, 10))
        
        subheader_label = ctk.CTkLabel(content_frame, text="Create your Antigravity account",
                                       font=ModernTheme.get_small_font(),
                                       text_color=ModernTheme.TEXT_SECONDARY)
        subheader_label.pack(pady=(0, 30))

        # Name field
        name_label = ctk.CTkLabel(content_frame, text="Full Name",
                                  font=ModernTheme.get_label_font(),
                                  text_color=ModernTheme.TEXT_PRIMARY)
        name_label.pack(anchor="w", pady=(10, 8))
        
        self.reg_name = ctk.CTkEntry(content_frame, width=300, height=45,
                                      placeholder_text="John Doe",
                                      fg_color=ModernTheme.SURFACE,
                                      border_color=ModernTheme.BORDER,
                                      border_width=1)
        self.reg_name.pack(pady=(0, 15))

        # Email field
        email_label = ctk.CTkLabel(content_frame, text="Email Address",
                                   font=ModernTheme.get_label_font(),
                                   text_color=ModernTheme.TEXT_PRIMARY)
        email_label.pack(anchor="w", pady=(0, 8))
        
        self.reg_email = ctk.CTkEntry(content_frame, width=300, height=45,
                                       placeholder_text="you@example.com",
                                       fg_color=ModernTheme.SURFACE,
                                       border_color=ModernTheme.BORDER,
                                       border_width=1)
        self.reg_email.pack(pady=(0, 15))

        # Password field
        pass_label = ctk.CTkLabel(content_frame, text="Password",
                                  font=ModernTheme.get_label_font(),
                                  text_color=ModernTheme.TEXT_PRIMARY)
        pass_label.pack(anchor="w", pady=(0, 8))
        
        self.reg_pass = ctk.CTkEntry(content_frame, width=300, height=45,
                                      placeholder_text="At least 8 characters",
                                      show="•",
                                      fg_color=ModernTheme.SURFACE,
                                      border_color=ModernTheme.BORDER,
                                      border_width=1)
        self.reg_pass.pack(pady=(0, 30))

        # Register button
        self.reg_btn = ModernTheme.create_modern_button(content_frame, "Create Account",
                                                        command=self.handle_register,
                                                        color="success", height=50, width=300)
        self.reg_btn.pack(pady=(0, 20))

        # Back link
        back_link = ctk.CTkLabel(content_frame, text="Already have an account? Sign in",
                                 font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
                                 text_color=ModernTheme.PRIMARY, cursor="hand2")
        back_link.pack()
        back_link.bind("<Button-1>", lambda e: self.setup_login_screen())

    def handle_register(self):
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_pass.get()

        if not name or not email or not password:
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        if len(password) < 6:
            messagebox.showwarning("Weak Password", "Password must be at least 6 characters.")
            return

        if any(u.email == email for u in self.users):
            messagebox.showerror("Email Exists", "This email is already registered.")
            return

        new_id = max([u.user_id for u in self.users], default=0) + 1
        new_user = Customer(new_id, name, email, password)
        
        self.users.append(new_user)
        self.data_manager.save_users(self.users)
        
        messagebox.showinfo("Success", "Account created! Please log in.")
        self.setup_login_screen()
