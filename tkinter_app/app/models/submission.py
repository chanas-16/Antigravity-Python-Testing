from app.utils.db import db

class Submission:
    def __init__(self, id=None, assignment_id=None, student_id=None, file_path=None, grade=None, submission_date=None):
        self.id = id
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.file_path = file_path
        self.grade = grade
        self.submission_date = submission_date

    @staticmethod
    def get_by_assignment(assignment_id):
        query = """
            SELECT s.*, u.name as student_name 
            FROM Submissions s
            JOIN Users u ON s.student_id = u.id
            WHERE s.assignment_id = %s
        """
        results = db.fetch_all(query, (assignment_id,))
        # Returning raw dicts here for easier UI integration since it joins with User
        return results

    @staticmethod
    def get_by_student_and_assignment(student_id, assignment_id):
        query = "SELECT * FROM Submissions WHERE student_id = %s AND assignment_id = %s"
        result = db.fetch_one(query, (student_id, assignment_id))
        if result:
            return Submission(**result)
        return None
        
    @staticmethod
    def get_by_student_and_course(student_id, course_id):
        query = """
            SELECT s.*, a.title as assignment_title
            FROM Submissions s
            JOIN Assignments a ON s.assignment_id = a.id
            WHERE s.student_id = %s AND a.course_id = %s
        """
        return db.fetch_all(query, (student_id, course_id))

    def save(self):
        if self.id:
            query = "UPDATE Submissions SET assignment_id=%s, student_id=%s, file_path=%s, grade=%s WHERE id=%s"
            db.execute_query(query, (self.assignment_id, self.student_id, self.file_path, self.grade, self.id))
        else:
            query = "INSERT INTO Submissions (assignment_id, student_id, file_path, grade) VALUES (%s, %s, %s, %s)"
            self.id = db.execute_query(query, (self.assignment_id, self.student_id, self.file_path, self.grade))
        return self.id
