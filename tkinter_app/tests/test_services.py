import pytest
from unittest.mock import patch, MagicMock
from app.services.auth import AuthService
from app.services.course_service import CourseService
from app.services.enrollment_service import EnrollmentService
from app.services.assignment_service import AssignmentService
from app.services.grading_service import GradingService
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.assignment import Assignment
from app.models.submission import Submission

# 1. Test Auth Service
@patch('app.models.user.User.get_by_email')
def test_login_success(mock_get_by_email):
    mock_user = MagicMock()
    mock_user.password = "password123"
    mock_get_by_email.return_value = mock_user

    success, message = AuthService.login("test@example.com", "password123")
    assert success is True
    assert message == "Login successful"
    assert AuthService.get_current_user() == mock_user

# 2. Test Course Service
@patch('app.models.course.Course.save')
def test_create_course(mock_save):
    mock_save.return_value = 1
    course_id = CourseService.create_course("Math 101", "Basic Math", 1, "10 weeks")
    assert course_id == 1
    mock_save.assert_called_once()

# 3. Test Enrollment Service
@patch('app.models.enrollment.Enrollment.get_by_student')
@patch('app.models.enrollment.Enrollment.save')
@patch('app.models.progress.Progress.save')
def test_enroll_student_success(mock_progress_save, mock_enroll_save, mock_get_by_student):
    # Mock that student is not enrolled in course 2
    mock_get_by_student.return_value = [{'course_id': 1}]
    
    success, message = EnrollmentService.enroll_student(student_id=1, course_id=2)
    assert success is True
    assert message == "Enrolled successfully"
    mock_enroll_save.assert_called_once()
    mock_progress_save.assert_called_once()

# 4. Test Assignment Service
@patch('app.models.submission.Submission.get_by_student_and_assignment')
@patch('app.models.submission.Submission.save')
def test_submit_assignment_new(mock_save, mock_get_existing):
    mock_get_existing.return_value = None # No previous submission
    
    success, message = AssignmentService.submit_assignment(assignment_id=1, student_id=1, file_path="doc.pdf")
    assert success is True
    assert message == "Assignment submitted successfully"
    mock_save.assert_called_once()

# 5. Test Grading Service
@patch('app.utils.db.db.fetch_one')
@patch('app.models.submission.Submission.save')
@patch('app.services.grading_service.GradingService.update_student_progress')
def test_assign_grade(mock_update_progress, mock_save, mock_fetch_one):
    # Mock finding the submission
    mock_fetch_one.return_value = {
        'id': 1, 'assignment_id': 1, 'student_id': 1, 
        'file_path': 'doc.pdf', 'grade': None, 'submission_date': '2023-01-01'
    }
    
    success, message = GradingService.assign_grade(submission_id=1, grade=95.0)
    assert success is True
    assert message == "Grade assigned successfully"
    mock_save.assert_called_once()
    mock_update_progress.assert_called_once_with(1, 1)
