import tkinter as tk
from tkinter import messagebox
import sys
import os

# Ensure the root directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.db import db
from app.utils.style import configure_window
from app.views.login import LoginView
from app.views.dashboard import DashboardView

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Online Course Management System")
        self.geometry("900x600")
        configure_window(self)

        # Check DB Connection
        conn = db.get_connection()
        if not conn:
            messagebox.showerror("Database Error", "Could not connect to the database. Please check your MySQL server and app/utils/db.py config.")
            self.destroy()
            return
            
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.current_view = None
        self.show_login()

    def show_login(self):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = LoginView(self.container, self)
        self.current_view.pack(fill="both", expand=True)

    def show_dashboard(self):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = DashboardView(self.container, self)
        self.current_view.pack(fill="both", expand=True)
        self.current_view.refresh()

if __name__ == "__main__":
    app = App()
    app.mainloop()
