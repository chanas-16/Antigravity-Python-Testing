from app.models.user import User

class AuthService:
    _current_user = None

    @classmethod
    def login(cls, email, password):
        user = User.get_by_email(email)
        if user and user.password == password:
            cls._current_user = user
            return True, "Login successful"
        return False, "Invalid email or password"

    @classmethod
    def logout(cls):
        cls._current_user = None

    @classmethod
    def get_current_user(cls):
        return cls._current_user

    @classmethod
    def register_user(cls, name, email, password, role):
        if User.get_by_email(email):
            return False, "Email already exists"
        user = User(name=name, email=email, password=password, role=role)
        user.save()
        return True, "Registration successful"
