import tkinter as tk
from tkinter import ttk, messagebox
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.services.auth import AuthService
from app.utils.style import *

class EnrollmentView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, **get_frame_style())
        self.controller = controller
        self.user = AuthService.get_current_user()

        title = "Available Courses" if self.user.role == 'student' else "Course Enrollments"
        tk.Label(self, text=title, **get_label_style(FONT_TITLE)).pack(pady=20)

        # List Frame
        self.list_frame = tk.Frame(self, **get_frame_style())
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if self.user.role == 'student':
            columns = ('id', 'title', 'description', 'status')
            self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')
            self.tree.heading('id', text='ID')
            self.tree.heading('title', text='Course Title')
            self.tree.heading('description', text='Description')
            self.tree.heading('status', text='Status')
            
            tk.Button(self, text="Enroll", **get_button_style(bg=SUCCESS_COLOR), command=self.enroll).pack(pady=10)
        else:
            columns = ('id', 'student_name', 'student_email', 'enrollment_date')
            self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')
            self.tree.heading('id', text='ID')
            self.tree.heading('student_name', text='Student Name')
            self.tree.heading('student_email', text='Email')
            self.tree.heading('enrollment_date', text='Enrollment Date')
            
            # Course selector for teachers
            select_frame = tk.Frame(self, **get_frame_style())
            select_frame.pack(fill="x", padx=20, pady=10)
            tk.Label(select_frame, text="Select Course:", **get_label_style()).pack(side="left")
            self.course_var = tk.StringVar()
            self.course_dropdown = ttk.Combobox(select_frame, textvariable=self.course_var, state="readonly")
            self.course_dropdown.pack(side="left", padx=10)
            self.course_dropdown.bind('<<ComboboxSelected>>', lambda e: self.refresh_teacher_view())

        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        if self.user.role == 'student':
            self.refresh_student_view()
        else:
            self.load_courses_for_dropdown()

    def refresh_student_view(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        all_courses = CourseService.get_all_courses()
        my_enrollments = EnrollmentService.get_student_enrollments(self.user.id)
        enrolled_course_ids = [e['course_id'] for e in my_enrollments]
        
        for course in all_courses:
            status = "Enrolled" if course.id in enrolled_course_ids else "Not Enrolled"
            self.tree.insert('', tk.END, values=(course.id, course.title, course.description, status))

    def load_courses_for_dropdown(self):
        courses = CourseService.get_courses_by_teacher(self.user.id) if self.user.role == 'teacher' else CourseService.get_all_courses()
        self.course_dict = {f"{c.id} - {c.title}": c.id for c in courses}
        self.course_dropdown['values'] = list(self.course_dict.keys())
        if self.course_dict:
            self.course_dropdown.current(0)
            self.refresh_teacher_view()

    def refresh_teacher_view(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        selection = self.course_var.get()
        if not selection:
            return
            
        course_id = self.course_dict[selection]
        enrollments = EnrollmentService.get_course_students(course_id)
        
        for e in enrollments:
            self.tree.insert('', tk.END, values=(e['id'], e['student_name'], e['student_email'], e['enrollment_date']))

    def enroll(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to enroll in")
            return
            
        item_values = self.tree.item(selected[0])['values']
        course_id = item_values[0]
        status = item_values[3]
        
        if status == "Enrolled":
            messagebox.showinfo("Info", "You are already enrolled in this course")
            return
            
        success, message = EnrollmentService.enroll_student(self.user.id, course_id)
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_student_view()
        else:
            messagebox.showerror("Error", message)
