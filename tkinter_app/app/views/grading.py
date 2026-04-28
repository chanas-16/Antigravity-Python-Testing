import tkinter as tk
from tkinter import ttk, messagebox
from app.services.course_service import CourseService
from app.services.assignment_service import AssignmentService
from app.services.grading_service import GradingService
from app.services.auth import AuthService
from app.utils.style import *

class GradingView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, **get_frame_style())
        self.controller = controller
        self.user = AuthService.get_current_user()

        tk.Label(self, text="Grading", **get_label_style(FONT_TITLE)).pack(pady=20)

        # Filters Frame
        filter_frame = tk.Frame(self, **get_frame_style())
        filter_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(filter_frame, text="Course:", **get_label_style()).pack(side="left")
        self.course_var = tk.StringVar()
        self.course_dropdown = ttk.Combobox(filter_frame, textvariable=self.course_var, state="readonly")
        self.course_dropdown.pack(side="left", padx=5)
        self.course_dropdown.bind('<<ComboboxSelected>>', lambda e: self.load_assignments())

        tk.Label(filter_frame, text="Assignment:", **get_label_style()).pack(side="left", padx=(15, 0))
        self.assignment_var = tk.StringVar()
        self.assignment_dropdown = ttk.Combobox(filter_frame, textvariable=self.assignment_var, state="readonly")
        self.assignment_dropdown.pack(side="left", padx=5)
        self.assignment_dropdown.bind('<<ComboboxSelected>>', lambda e: self.refresh_submissions())

        # List Frame
        self.list_frame = tk.Frame(self, **get_frame_style())
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ('id', 'student_name', 'file_path', 'submission_date', 'grade')
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('student_name', text='Student')
        self.tree.heading('file_path', text='File Path')
        self.tree.heading('submission_date', text='Date')
        self.tree.heading('grade', text='Current Grade')
        self.tree.pack(fill="both", expand=True)

        # Grade Form
        grade_frame = tk.Frame(self, **get_frame_style())
        grade_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(grade_frame, text="Grade (0-100):", **get_label_style()).pack(side="left")
        self.grade_entry = tk.Entry(grade_frame, **get_entry_style(), width=10)
        self.grade_entry.pack(side="left", padx=5)
        tk.Button(grade_frame, text="Assign Grade", **get_button_style(bg=SUCCESS_COLOR), command=self.assign_grade).pack(side="left", padx=10)

    def refresh(self):
        courses = CourseService.get_courses_by_teacher(self.user.id) if self.user.role == 'teacher' else CourseService.get_all_courses()
        self.course_dict = {f"{c.id} - {c.title}": c.id for c in courses}
        self.course_dropdown['values'] = list(self.course_dict.keys())
        if self.course_dict:
            self.course_dropdown.current(0)
            self.load_assignments()

    def load_assignments(self):
        selection = self.course_var.get()
        if not selection:
            return
            
        course_id = self.course_dict[selection]
        assignments = AssignmentService.get_course_assignments(course_id)
        
        self.assign_dict = {f"{a.id} - {a.title}": a.id for a in assignments}
        self.assignment_dropdown['values'] = list(self.assign_dict.keys())
        if self.assign_dict:
            self.assignment_dropdown.current(0)
            self.refresh_submissions()
        else:
            self.assignment_dropdown.set('')
            for item in self.tree.get_children():
                self.tree.delete(item)

    def refresh_submissions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        selection = self.assignment_var.get()
        if not selection:
            return
            
        assignment_id = self.assign_dict[selection]
        submissions = AssignmentService.get_assignment_submissions(assignment_id)
        
        for s in submissions:
            grade = s['grade'] if s['grade'] is not None else "Not Graded"
            self.tree.insert('', tk.END, values=(s['id'], s['student_name'], s['file_path'], s['submission_date'], grade))

    def assign_grade(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a submission to grade")
            return
            
        try:
            grade = float(self.grade_entry.get())
            if grade < 0 or grade > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number between 0 and 100")
            return
            
        submission_id = self.tree.item(selected[0])['values'][0]
        
        success, message = GradingService.assign_grade(submission_id, grade)
        if success:
            messagebox.showinfo("Success", message)
            self.grade_entry.delete(0, tk.END)
            self.refresh_submissions()
        else:
            messagebox.showerror("Error", message)
