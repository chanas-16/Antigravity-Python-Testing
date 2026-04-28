import tkinter as tk
from tkinter import ttk, messagebox
from app.services.course_service import CourseService
from app.services.auth import AuthService
from app.utils.style import *

class CourseView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, **get_frame_style())
        self.controller = controller

        tk.Label(self, text="Manage Courses", **get_label_style(FONT_TITLE)).pack(pady=20)

        # List Frame
        self.list_frame = tk.Frame(self, **get_frame_style())
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ('id', 'title', 'description', 'duration')
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show='headings')
        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='Title')
        self.tree.heading('description', text='Description')
        self.tree.heading('duration', text='Duration')
        
        self.tree.column('id', width=50)
        self.tree.column('title', width=200)
        self.tree.column('description', width=300)
        self.tree.column('duration', width=100)
        
        self.tree.pack(fill="both", expand=True)

        # Form Frame
        form_frame = tk.Frame(self, **get_frame_style())
        form_frame.pack(fill="x", padx=20, pady=20)

        tk.Label(form_frame, text="Title:", **get_label_style()).grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(form_frame, **get_entry_style())
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Description:", **get_label_style()).grid(row=0, column=2, padx=5, pady=5)
        self.desc_entry = tk.Entry(form_frame, **get_entry_style())
        self.desc_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Duration:", **get_label_style()).grid(row=0, column=4, padx=5, pady=5)
        self.duration_entry = tk.Entry(form_frame, **get_entry_style())
        self.duration_entry.grid(row=0, column=5, padx=5, pady=5)

        btn_frame = tk.Frame(self, **get_frame_style())
        btn_frame.pack(fill="x", padx=20, pady=10)

        tk.Button(btn_frame, text="Add Course", **get_button_style(), command=self.add_course).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Delete Selected", **get_button_style(bg=ERROR_COLOR), command=self.delete_course).pack(side="left", padx=10)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        user = AuthService.get_current_user()
        if user.role == 'admin':
            courses = CourseService.get_all_courses()
        else:
            courses = CourseService.get_courses_by_teacher(user.id)
            
        for course in courses:
            self.tree.insert('', tk.END, values=(course.id, course.title, course.description, course.duration))

    def add_course(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        duration = self.duration_entry.get()
        user = AuthService.get_current_user()

        if not title:
            messagebox.showerror("Error", "Title is required")
            return

        CourseService.create_course(title, desc, user.id, duration)
        messagebox.showinfo("Success", "Course added successfully")
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.refresh()

    def delete_course(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a course to delete")
            return
            
        course_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this course?"):
            CourseService.delete_course(course_id)
            self.refresh()
