from app.utils.db import db

class User:
    def __init__(self, id=None, name=None, email=None, password=None, role=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    @staticmethod
    def get_by_email(email):
        query = "SELECT * FROM Users WHERE email = %s"
        result = db.fetch_one(query, (email,))
        if result:
            return User(**result)
        return None

    @staticmethod
    def get_by_id(user_id):
        query = "SELECT * FROM Users WHERE id = %s"
        result = db.fetch_one(query, (user_id,))
        if result:
            return User(**result)
        return None

    @staticmethod
    def get_all_by_role(role):
        query = "SELECT * FROM Users WHERE role = %s"
        results = db.fetch_all(query, (role,))
        return [User(**row) for row in results]

    def save(self):
        if self.id:
            query = "UPDATE Users SET name=%s, email=%s, password=%s, role=%s WHERE id=%s"
            db.execute_query(query, (self.name, self.email, self.password, self.role, self.id))
        else:
            query = "INSERT INTO Users (name, email, password, role) VALUES (%s, %s, %s, %s)"
            self.id = db.execute_query(query, (self.name, self.email, self.password, self.role))
        return self.id
