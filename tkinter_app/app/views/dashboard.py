import tkinter as tk
from app.services.auth import AuthService
from app.utils.style import *
from app.views.course import CourseView
from app.views.enrollment import EnrollmentView
from app.views.assignment import AssignmentView
from app.views.progress import ProgressView
from app.views.grading import GradingView

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, **get_frame_style())
        self.controller = controller
        
        self.sidebar = tk.Frame(self, bg=PRIMARY_COLOR, width=200)
        self.sidebar.pack(side="left", fill="y")
        
        self.content_area = tk.Frame(self, **get_frame_style())
        self.content_area.pack(side="right", fill="both", expand=True)

        self.current_view = None

    def refresh(self):
        user = AuthService.get_current_user()
        if not user:
            self.controller.show_login()
            return

        # Clear sidebar
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        # User Info
        tk.Label(self.sidebar, text=f"Welcome, {user.name}", bg=PRIMARY_COLOR, fg=PRIMARY_FG, font=FONT_HEADER).pack(pady=20, padx=10)
        tk.Label(self.sidebar, text=f"Role: {user.role.capitalize()}", bg=PRIMARY_COLOR, fg=PRIMARY_FG, font=FONT_NORMAL).pack(pady=5)

        # Navigation Buttons based on role
        if user.role in ['admin', 'teacher']:
            self.add_nav_button("Courses", lambda: self.show_view(CourseView))
            self.add_nav_button("Enrollments", lambda: self.show_view(EnrollmentView))
            self.add_nav_button("Assignments", lambda: self.show_view(AssignmentView))
            self.add_nav_button("Grading", lambda: self.show_view(GradingView))
        
        if user.role == 'student':
            self.add_nav_button("Available Courses", lambda: self.show_view(EnrollmentView))
            self.add_nav_button("My Assignments", lambda: self.show_view(AssignmentView))
            self.add_nav_button("My Progress", lambda: self.show_view(ProgressView))

        self.add_nav_button("Logout", self.logout, bg=ERROR_COLOR)

        # Show default view
        if user.role in ['admin', 'teacher']:
            self.show_view(CourseView)
        else:
            self.show_view(EnrollmentView)

    def add_nav_button(self, text, command, bg=PRIMARY_COLOR):
        btn = tk.Button(self.sidebar, text=text, command=command, bg=bg, fg=PRIMARY_FG, 
                        font=FONT_NORMAL, relief="flat", activebackground="#004494", 
                        activeforeground=PRIMARY_FG, pady=10)
        btn.pack(fill="x", pady=2)

    def show_view(self, view_class):
        if self.current_view:
            self.current_view.destroy()
        
        self.current_view = view_class(self.content_area, self.controller)
        self.current_view.pack(fill="both", expand=True)
        # Call refresh if the view has it to load data
        if hasattr(self.current_view, 'refresh'):
            self.current_view.refresh()

    def logout(self):
        AuthService.logout()
        self.controller.show_login()
