import customtkinter as ctk
from data.data_manager import DataManager
from data.analytics import Analytics
from gui.app import ECommerceApp
from gui.auth_gui import AuthGUI

def main():
    root = ctk.CTk()  # Use CustomTkinter root, not Tkinter
    root.title("Antigravity - E-Commerce Store")
    root.geometry("1300x800")
    root.withdraw()  # Hide initially for auth
    
    data_manager = DataManager()
    analytics = Analytics(data_manager)

    def logout_callback():
        # Clear root and restart auth
        for widget in root.winfo_children():
            widget.destroy()
        root.withdraw()
        start_auth()

    def start_main_app(user):
        # Once login is successful, launch the main application
        root.deiconify()  # Show root window
        root.update()  # Force update
        app = ECommerceApp(root, data_manager, analytics, user, logout_callback)

    def start_auth():
        auth = AuthGUI(root, data_manager, start_main_app)
    
    start_auth()
    root.mainloop()


if __name__ == "__main__":
    main()
