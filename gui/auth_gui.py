import tkinter as tk
from tkinter import ttk, messagebox
from models.user import Customer, Admin

class AuthGUI:
    def __init__(self, root, data_manager, on_login_success):
        self.root = root
        self.data_manager = data_manager
        self.on_login_success = on_login_success
        self.users = self.data_manager.load_users()
        
        self.setup_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_login_screen(self):
        self.clear_screen()
        self.root.title("E-Commerce - Login")
        self.root.geometry("400x300")

        frame = ttk.Frame(self.root, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(frame, text="E-Commerce Login", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.pass_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.pass_var, show="*", width=30).grid(row=2, column=1, pady=5)

        ttk.Button(frame, text="Login", command=self.handle_login).grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.EW)
        
        ttk.Label(frame, text="Don't have an account?").grid(row=4, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(frame, text="Register Now", command=self.setup_register_screen).grid(row=5, column=0, columnspan=2, pady=5, sticky=tk.EW)

    def handle_login(self):
        email = self.email_var.get()
        password = self.pass_var.get()
        
        user = next((u for u in self.users if u.email == email and u.password == password), None)
        
        if user:
            messagebox.showinfo("Success", f"Welcome back, {user.name}!")
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    def setup_register_screen(self):
        self.clear_screen()
        self.root.title("E-Commerce - Register")
        
        frame = ttk.Frame(self.root, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(frame, text="Create Account", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Full Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_name = tk.StringVar()
        ttk.Entry(frame, textvariable=self.reg_name, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reg_email = tk.StringVar()
        ttk.Entry(frame, textvariable=self.reg_email, width=30).grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.reg_pass = tk.StringVar()
        ttk.Entry(frame, textvariable=self.reg_pass, show="*", width=30).grid(row=3, column=1, pady=5)

        ttk.Button(frame, text="Register", command=self.handle_register).grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.EW)
        ttk.Button(frame, text="Back to Login", command=self.setup_login_screen).grid(row=5, column=0, columnspan=2, pady=5, sticky=tk.EW)

    def handle_register(self):
        name = self.reg_name.get()
        email = self.reg_email.get()
        password = self.reg_pass.get()

        if not name or not email or not password:
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        if any(u.email == email for u in self.users):
            messagebox.showerror("Error", "Email already registered.")
            return

        new_id = max([u.user_id for u in self.users], default=0) + 1
        new_user = Customer(new_id, name, email, password)
        
        self.users.append(new_user)
        self.data_manager.save_users(self.users)
        
        messagebox.showinfo("Success", "Account created successfully! Please login.")
        self.setup_login_screen()
