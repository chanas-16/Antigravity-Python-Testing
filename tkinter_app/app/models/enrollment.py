from app.utils.db import db

class Enrollment:
    def __init__(self, id=None, student_id=None, course_id=None, enrollment_date=None):
        self.id = id
        self.student_id = student_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date

    @staticmethod
    def get_by_student(student_id):
        query = """
            SELECT e.*, c.title as course_title 
            FROM Enrollments e
            JOIN Courses c ON e.course_id = c.id
            WHERE e.student_id = %s
        """
        return db.fetch_all(query, (student_id,))

    @staticmethod
    def get_by_course(course_id):
        query = """
            SELECT e.*, u.name as student_name, u.email as student_email
            FROM Enrollments e
            JOIN Users u ON e.student_id = u.id
            WHERE e.course_id = %s
        """
        return db.fetch_all(query, (course_id,))

    def save(self):
        # We don't typically update enrollments, just insert or delete
        if not self.id:
            query = "INSERT INTO Enrollments (student_id, course_id) VALUES (%s, %s)"
            self.id = db.execute_query(query, (self.student_id, self.course_id))
        return self.id

    def delete(self):
        if self.id:
            query = "DELETE FROM Enrollments WHERE id=%s"
            db.execute_query(query, (self.id,))
