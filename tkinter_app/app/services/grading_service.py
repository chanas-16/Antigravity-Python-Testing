from app.models.submission import Submission
from app.models.progress import Progress
from app.models.assignment import Assignment

class GradingService:
    @staticmethod
    def assign_grade(submission_id, grade):
        # Fetch the submission directly using a query since we didn't add get_by_id in Submission
        from app.utils.db import db
        query = "SELECT * FROM Submissions WHERE id = %s"
        result = db.fetch_one(query, (submission_id,))
        if not result:
            return False, "Submission not found"
            
        submission = Submission(**result)
        submission.grade = grade
        submission.save()
        
        # Update progress after grading
        GradingService.update_student_progress(submission.student_id, submission.assignment_id)
        return True, "Grade assigned successfully"

    @staticmethod
    def update_student_progress(student_id, assignment_id):
        # Find course ID from assignment
        assignment = Assignment.get_by_id(assignment_id)
        if not assignment:
            return
            
        course_id = assignment.course_id
        
        # Count total assignments for course
        all_assignments = Assignment.get_by_course(course_id)
        total = len(all_assignments)
        
        if total == 0:
            return
            
        # Count graded submissions for this student in this course
        from app.utils.db import db
        query = """
            SELECT COUNT(*) as count
            FROM Submissions s
            JOIN Assignments a ON s.assignment_id = a.id
            WHERE s.student_id = %s AND a.course_id = %s AND s.grade IS NOT NULL
        """
        result = db.fetch_one(query, (student_id, course_id))
        completed = result['count'] if result else 0
        
        # Calculate percentage
        percentage = int((completed / total) * 100)
        
        # Update progress table
        progress = Progress.get_by_student_and_course(student_id, course_id)
        if progress:
            progress.completion_percentage = percentage
            progress.save()
        else:
            progress = Progress(student_id=student_id, course_id=course_id, completion_percentage=percentage)
            progress.save()
