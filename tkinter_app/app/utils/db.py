import sqlite3
import os

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'course_management.db')
            cls._instance.connection = None
            cls._instance.init_db()
        return cls._instance

    def init_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Enable foreign keys in SQLite
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            teacher_id INTEGER NOT NULL,
            duration VARCHAR(100),
            FOREIGN KEY (teacher_id) REFERENCES Users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            file_path VARCHAR(500),
            grade DECIMAL(5,2),
            submission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (student_id, assignment_id),
            FOREIGN KEY (assignment_id) REFERENCES Assignments(id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES Users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            completion_percentage INTEGER DEFAULT 0,
            UNIQUE (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES Users(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES Courses(id) ON DELETE CASCADE
        );
        """)
        
        # Insert default admin
        cursor.execute("INSERT OR IGNORE INTO Users (id, name, email, password, role) VALUES (1, 'Admin', 'admin@example.com', 'admin123', 'admin')")
        conn.commit()
        conn.close()

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_file)
            self.connection.row_factory = sqlite3.Row  # To return rows as dict-like objects
            self.connection.execute("PRAGMA foreign_keys = ON;")
        return self.connection

    def execute_query(self, query, params=None):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Replace MySQL %s with SQLite ?
                sqlite_query = query.replace('%s', '?')
                cursor.execute(sqlite_query, params or ())
                conn.commit()
                return cursor.lastrowid
            except sqlite3.Error as e:
                print(f"Error executing query: {e}")
                conn.rollback()
                return None
        return None

    def fetch_all(self, query, params=None):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sqlite_query = query.replace('%s', '?')
                cursor.execute(sqlite_query, params or ())
                rows = cursor.fetchall()
                # Convert sqlite3.Row objects to standard dicts
                return [dict(row) for row in rows]
            except sqlite3.Error as e:
                print(f"Error fetching data: {e}")
                return []
        return []

    def fetch_one(self, query, params=None):
        conn = self.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sqlite_query = query.replace('%s', '?')
                cursor.execute(sqlite_query, params or ())
                row = cursor.fetchone()
                return dict(row) if row else None
            except sqlite3.Error as e:
                print(f"Error fetching data: {e}")
                return None
        return None

db = Database()
