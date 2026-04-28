from app.utils.db import db

class Progress:
    def __init__(self, id=None, student_id=None, course_id=None, completion_percentage=0):
        self.id = id
        self.student_id = student_id
        self.course_id = course_id
        self.completion_percentage = completion_percentage

    @staticmethod
    def get_by_student_and_course(student_id, course_id):
        query = "SELECT * FROM Progress WHERE student_id = %s AND course_id = %s"
        result = db.fetch_one(query, (student_id, course_id))
        if result:
            return Progress(**result)
        return None

    @staticmethod
    def get_by_student(student_id):
        query = """
            SELECT p.*, c.title as course_title 
            FROM Progress p
            JOIN Courses c ON p.course_id = c.id
            WHERE p.student_id = %s
        """
        return db.fetch_all(query, (student_id,))

    def save(self):
        if self.id:
            query = "UPDATE Progress SET completion_percentage=%s WHERE id=%s"
            db.execute_query(query, (self.completion_percentage, self.id))
        else:
            query = "INSERT INTO Progress (student_id, course_id, completion_percentage) VALUES (%s, %s, %s)"
            self.id = db.execute_query(query, (self.student_id, self.course_id, self.completion_percentage))
        return self.id
