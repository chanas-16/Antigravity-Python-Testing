from app.models.enrollment import Enrollment
from app.models.progress import Progress

class EnrollmentService:
    @staticmethod
    def enroll_student(student_id, course_id):
        # Check if already enrolled
        existing = Enrollment.get_by_student(student_id)
        for e in existing:
            if e['course_id'] == course_id:
                return False, "Already enrolled in this course"
        
        enrollment = Enrollment(student_id=student_id, course_id=course_id)
        enrollment.save()
        
        # Initialize progress
        progress = Progress(student_id=student_id, course_id=course_id, completion_percentage=0)
        progress.save()
        
        return True, "Enrolled successfully"

    @staticmethod
    def get_student_enrollments(student_id):
        return Enrollment.get_by_student(student_id)

    @staticmethod
    def get_course_students(course_id):
        return Enrollment.get_by_course(course_id)

    @staticmethod
    def unenroll_student(enrollment_id):
        enrollment = Enrollment()
        enrollment.id = enrollment_id
        enrollment.delete()
        return True
