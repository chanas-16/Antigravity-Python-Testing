from app.utils.db import db

class Assignment:
    def __init__(self, id=None, course_id=None, title=None, description=None):
        self.id = id
        self.course_id = course_id
        self.title = title
        self.description = description

    @staticmethod
    def get_by_course(course_id):
        query = "SELECT * FROM Assignments WHERE course_id = %s"
        results = db.fetch_all(query, (course_id,))
        return [Assignment(**row) for row in results]

    @staticmethod
    def get_by_id(assignment_id):
        query = "SELECT * FROM Assignments WHERE id = %s"
        result = db.fetch_one(query, (assignment_id,))
        if result:
            return Assignment(**result)
        return None

    def save(self):
        if self.id:
            query = "UPDATE Assignments SET course_id=%s, title=%s, description=%s WHERE id=%s"
            db.execute_query(query, (self.course_id, self.title, self.description, self.id))
        else:
            query = "INSERT INTO Assignments (course_id, title, description) VALUES (%s, %s, %s)"
            self.id = db.execute_query(query, (self.course_id, self.title, self.description))
        return self.id

    def delete(self):
        if self.id:
            query = "DELETE FROM Assignments WHERE id=%s"
            db.execute_query(query, (self.id,))
