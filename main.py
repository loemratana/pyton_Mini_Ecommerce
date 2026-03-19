import tkinter as tk
from data.data_manager import DataManager
from data.analytics import Analytics
from gui.app import ECommerceApp
from gui.auth_gui import AuthGUI

def main():
    root = tk.Tk()
    data_manager = DataManager()
    analytics = Analytics(data_manager)

    def start_main_app(user):
        # Once login is successful, launch the main application
        app = ECommerceApp(root, data_manager, analytics, user)

    # Start with the Authentication GUI
    auth = AuthGUI(root, data_manager, start_main_app)
    
    root.mainloop()

if __name__ == "__main__":
    main()
