import tkinter as tk
from tkinter import ttk, messagebox
from models.user import Admin, Customer

class ProfileTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self, text="User Profile", font=("Arial", 16, "bold")).pack(pady=10)
        
        form = ttk.Frame(self)
        form.pack(pady=10)
        
        ttk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar(value=self.app.current_user.name)
        ttk.Entry(form, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_var = tk.StringVar(value=self.app.current_user.email)
        ttk.Entry(form, textvariable=self.email_var).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form, text="Role:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(form, text=self.app.current_user.role, font=("Arial", 10, "italic")).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Button(form, text="Update Profile", command=self.update_profile).grid(row=3, column=0, columnspan=2, pady=10)
        
        if isinstance(self.app.current_user, Admin):
            self.setup_admin_tools()

    def setup_admin_tools(self):
        divider = ttk.Separator(self, orient='horizontal')
        divider.pack(fill='x', padx=50, pady=20)
        
        ttk.Label(self, text="Admin: User Management", font=("Arial", 14, "bold")).pack(pady=5)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="Add New Admin", command=self.add_new_admin).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View All Users", command=self.view_users).pack(side=tk.LEFT, padx=5)

    def update_profile(self):
        self.app.current_user.name = self.name_var.get()
        self.app.current_user.email = self.email_var.get()
        
        # Persist change to file
        all_users = self.app.data_manager.load_users()
        for i, u in enumerate(all_users):
            if u.user_id == self.app.current_user.user_id:
                all_users[i] = self.app.current_user
                break
        self.app.data_manager.save_users(all_users)
        
        messagebox.showinfo("Success", "Profile updated successfully.")

    def add_new_admin(self):
        win = tk.Toplevel(self)
        win.title("Create Admin Account")
        win.geometry("300x250")
        
        ttk.Label(win, text="Name:").pack(pady=2)
        name_v = tk.StringVar()
        ttk.Entry(win, textvariable=name_v).pack(pady=2)
        
        ttk.Label(win, text="Email:").pack(pady=2)
        email_v = tk.StringVar()
        ttk.Entry(win, textvariable=email_v).pack(pady=2)
        
        ttk.Label(win, text="Password:").pack(pady=2)
        pass_v = tk.StringVar()
        ttk.Entry(win, textvariable=pass_v, show="*").pack(pady=2)
        
        def save():
            users = self.app.data_manager.load_users()
            new_id = max([u.user_id for u in users], default=0) + 1
            new_admin = Admin(new_id, name_v.get(), email_v.get(), pass_v.get())
            users.append(new_admin)
            self.app.data_manager.save_users(users)
            messagebox.showinfo("Success", "New Admin created.")
            win.destroy()
            
        ttk.Button(win, text="Create Admin", command=save).pack(pady=10)

    def view_users(self):
        win = tk.Toplevel(self)
        win.title("All Users")
        win.geometry("500x400")
        
        cols = ("ID", "Name", "Email", "Role")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c)
        
        users = self.app.data_manager.load_users()
        for u in users:
            tree.insert("", tk.END, values=(u.user_id, u.name, u.email, u.role))
            
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
