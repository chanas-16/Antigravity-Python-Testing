import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from app.services.assignment_service import AssignmentService
from app.services.course_service import CourseService
from app.services.auth import AuthService
from app.utils.style import *

class AssignmentView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, **get_frame_style())
        self.controller = controller
        self.user = AuthService.get_current_user()

        tk.Label(self, text="Assignments", **get_label_style(FONT_TITLE)).pack(pady=20)

        # Selection Frame
        select_frame = tk.Frame(self, **get_frame_style())
        select_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(select_frame, text="Select Course:", **get_label_style()).pack(side="left")
        self.course_var = tk.StringVar()
        self.course_dropdown = ttk.Combobox(select_frame, textvariable=self.course_var, state="readonly")
        self.course_dropdown.pack(side="left", padx=10)
        self.course_dropdown.bind('<<ComboboxSelected>>', lambda e: self.refresh_assignments())

        # List Frame
        self.list_frame = tk.Frame(self, **get_frame_style())
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if self.user.role == 'student':
            columns = ('id', 'title', 'description', 'status', 'grade')
            self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')
            self.tree.heading('id', text='ID')
            self.tree.heading('title', text='Title')
            self.tree.heading('description', text='Description')
            self.tree.heading('status', text='Status')
            self.tree.heading('grade', text='Grade')
            
            # Submission Frame
            sub_frame = tk.Frame(self, **get_frame_style())
            sub_frame.pack(fill="x", padx=20, pady=10)
            self.file_path_var = tk.StringVar()
            tk.Entry(sub_frame, textvariable=self.file_path_var, width=40, state='readonly', **get_entry_style()).pack(side="left", padx=5)
            tk.Button(sub_frame, text="Browse...", **get_button_style(), command=self.browse_file).pack(side="left", padx=5)
            tk.Button(sub_frame, text="Submit", **get_button_style(bg=SUCCESS_COLOR), command=self.submit_assignment).pack(side="left", padx=5)

        else:
            columns = ('id', 'title', 'description')
            self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')
            self.tree.heading('id', text='ID')
            self.tree.heading('title', text='Title')
            self.tree.heading('description', text='Description')
            
            # Add Assignment Frame
            add_frame = tk.Frame(self, **get_frame_style())
            add_frame.pack(fill="x", padx=20, pady=10)
            tk.Label(add_frame, text="Title:", **get_label_style()).pack(side="left")
            self.title_entry = tk.Entry(add_frame, **get_entry_style())
            self.title_entry.pack(side="left", padx=5)
            tk.Label(add_frame, text="Description:", **get_label_style()).pack(side="left")
            self.desc_entry = tk.Entry(add_frame, **get_entry_style())
            self.desc_entry.pack(side="left", padx=5)
            tk.Button(add_frame, text="Add Assignment", **get_button_style(), command=self.add_assignment).pack(side="left", padx=5)

        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        courses = CourseService.get_courses_by_teacher(self.user.id) if self.user.role == 'teacher' else CourseService.get_all_courses()
        self.course_dict = {f"{c.id} - {c.title}": c.id for c in courses}
        self.course_dropdown['values'] = list(self.course_dict.keys())
        if self.course_dict:
            self.course_dropdown.current(0)
            self.refresh_assignments()

    def refresh_assignments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        selection = self.course_var.get()
        if not selection:
            return
            
        course_id = self.course_dict[selection]
        assignments = AssignmentService.get_course_assignments(course_id)
        
        if self.user.role == 'student':
            submissions = AssignmentService.get_student_submissions_for_course(self.user.id, course_id)
            sub_dict = {s['assignment_id']: s for s in submissions}
            
            for a in assignments:
                sub = sub_dict.get(a.id)
                status = "Submitted" if sub else "Pending"
                grade = sub['grade'] if sub and sub['grade'] is not None else "N/A"
                self.tree.insert('', tk.END, values=(a.id, a.title, a.description, status, grade))
        else:
            for a in assignments:
                self.tree.insert('', tk.END, values=(a.id, a.title, a.description))

    def add_assignment(self):
        selection = self.course_var.get()
        if not selection:
            messagebox.showwarning("Warning", "Please select a course")
            return
            
        course_id = self.course_dict[selection]
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        
        if not title:
            messagebox.showerror("Error", "Title is required")
            return
            
        AssignmentService.create_assignment(course_id, title, desc)
        messagebox.showinfo("Success", "Assignment created")
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.refresh_assignments()

    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.file_path_var.set(filename)

    def submit_assignment(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an assignment to submit")
            return
            
        assignment_id = self.tree.item(selected[0])['values'][0]
        file_path = self.file_path_var.get()
        
        if not file_path:
            messagebox.showwarning("Warning", "Please select a file to submit")
            return
            
        success, message = AssignmentService.submit_assignment(assignment_id, self.user.id, file_path)
        if success:
            messagebox.showinfo("Success", message)
            self.file_path_var.set("")
            self.refresh_assignments()
        else:
            messagebox.showerror("Error", message)
