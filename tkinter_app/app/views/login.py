import tkinter as tk
from tkinter import messagebox
from app.services.auth import AuthService
from app.utils.style import *

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, **get_frame_style())
        self.controller = controller

        # Title
        tk.Label(self, text="Course Management System", **get_label_style(FONT_TITLE)).pack(pady=40)

        # Login Frame
        login_frame = tk.Frame(self, **get_frame_style())
        login_frame.pack(pady=20)

        tk.Label(login_frame, text="Email:", **get_label_style()).grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.email_entry = tk.Entry(login_frame, **get_entry_style(), width=30)
        self.email_entry.grid(row=0, column=1, pady=10, padx=10)
        # Default value for testing
        self.email_entry.insert(0, "admin@example.com")

        tk.Label(login_frame, text="Password:", **get_label_style()).grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.password_entry = tk.Entry(login_frame, **get_entry_style(), show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        # Default value for testing
        self.password_entry.insert(0, "admin123")

        tk.Button(login_frame, text="Login", **get_button_style(), command=self.handle_login).grid(row=2, column=0, pady=20, padx=5)
        tk.Button(login_frame, text="Register Student", **get_button_style(bg=SUCCESS_COLOR), command=self.handle_register).grid(row=2, column=1, pady=20, padx=5)

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return

        success, message = AuthService.login(email, password)
        if success:
            self.controller.show_dashboard()
        else:
            messagebox.showerror("Login Failed", message)

    def handle_register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password to register")
            return
            
        success, message = AuthService.register_user(name=email.split('@')[0], email=email, password=password, role='student')
        if success:
            messagebox.showinfo("Success", "Registered as a student! You can now login.")
        else:
            messagebox.showerror("Registration Failed", message)
