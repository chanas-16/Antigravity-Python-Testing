from app.models.assignment import Assignment
from app.models.submission import Submission

class AssignmentService:
    @staticmethod
    def create_assignment(course_id, title, description):
        assignment = Assignment(course_id=course_id, title=title, description=description)
        return assignment.save()

    @staticmethod
    def get_course_assignments(course_id):
        return Assignment.get_by_course(course_id)

    @staticmethod
    def submit_assignment(assignment_id, student_id, file_path):
        # Check if already submitted
        existing = Submission.get_by_student_and_assignment(student_id, assignment_id)
        if existing:
            existing.file_path = file_path
            existing.save()
            return True, "Submission updated"
        else:
            submission = Submission(assignment_id=assignment_id, student_id=student_id, file_path=file_path)
            submission.save()
            return True, "Assignment submitted successfully"

    @staticmethod
    def get_student_submissions_for_course(student_id, course_id):
        return Submission.get_by_student_and_course(student_id, course_id)
        
    @staticmethod
    def get_assignment_submissions(assignment_id):
        return Submission.get_by_assignment(assignment_id)
