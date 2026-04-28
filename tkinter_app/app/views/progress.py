import tkinter as tk
from tkinter import ttk
from app.services.enrollment_service import EnrollmentService
from app.services.auth import AuthService
from app.models.progress import Progress
from app.utils.style import *

class ProgressView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, **get_frame_style())
        self.controller = controller
        self.user = AuthService.get_current_user()

        tk.Label(self, text="My Progress", **get_label_style(FONT_TITLE)).pack(pady=20)

        self.progress_container = tk.Frame(self, **get_frame_style())
        self.progress_container.pack(fill="both", expand=True, padx=20, pady=10)

    def refresh(self):
        for widget in self.progress_container.winfo_children():
            widget.destroy()

        progress_records = Progress.get_by_student(self.user.id)
        
        if not progress_records:
            tk.Label(self.progress_container, text="You are not enrolled in any courses yet.", **get_label_style()).pack(pady=20)
            return

        for record in progress_records:
            frame = tk.Frame(self.progress_container, **get_frame_style())
            frame.pack(fill="x", pady=10)
            
            tk.Label(frame, text=record['course_title'], **get_label_style(FONT_HEADER)).pack(anchor="w")
            
            pb = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate")
            pb.pack(side="left", padx=10, pady=5)
            pb['value'] = record['completion_percentage']
            
            tk.Label(frame, text=f"{record['completion_percentage']}%", **get_label_style()).pack(side="left")
