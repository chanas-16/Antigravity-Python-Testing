from app.models.course import Course

class CourseService:
    @staticmethod
    def create_course(title, description, teacher_id, duration):
        course = Course(title=title, description=description, teacher_id=teacher_id, duration=duration)
        return course.save()

    @staticmethod
    def get_all_courses():
        return Course.get_all()

    @staticmethod
    def get_courses_by_teacher(teacher_id):
        return Course.get_by_teacher(teacher_id)

    @staticmethod
    def update_course(course_id, title, description, duration):
        course = Course.get_by_id(course_id)
        if course:
            course.title = title
            course.description = description
            course.duration = duration
            course.save()
            return True
        return False

    @staticmethod
    def delete_course(course_id):
        course = Course.get_by_id(course_id)
        if course:
            course.delete()
            return True
        return False
