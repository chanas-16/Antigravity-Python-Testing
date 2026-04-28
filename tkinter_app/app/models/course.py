from app.utils.db import db

class Course:
    def __init__(self, id=None, title=None, description=None, teacher_id=None, duration=None):
        self.id = id
        self.title = title
        self.description = description
        self.teacher_id = teacher_id
        self.duration = duration

    @staticmethod
    def get_by_id(course_id):
        query = "SELECT * FROM Courses WHERE id = %s"
        result = db.fetch_one(query, (course_id,))
        if result:
            return Course(**result)
        return None

    @staticmethod
    def get_all():
        query = "SELECT * FROM Courses"
        results = db.fetch_all(query)
        return [Course(**row) for row in results]
        
    @staticmethod
    def get_by_teacher(teacher_id):
        query = "SELECT * FROM Courses WHERE teacher_id = %s"
        results = db.fetch_all(query, (teacher_id,))
        return [Course(**row) for row in results]

    def save(self):
        if self.id:
            query = "UPDATE Courses SET title=%s, description=%s, teacher_id=%s, duration=%s WHERE id=%s"
            db.execute_query(query, (self.title, self.description, self.teacher_id, self.duration, self.id))
        else:
            query = "INSERT INTO Courses (title, description, teacher_id, duration) VALUES (%s, %s, %s, %s)"
            self.id = db.execute_query(query, (self.title, self.description, self.teacher_id, self.duration))
        return self.id

    def delete(self):
        if self.id:
            query = "DELETE FROM Courses WHERE id=%s"
            db.execute_query(query, (self.id,))
