import sqlite3
import os

def init():
    # This deletes the old database so we can start fresh without errors
    if os.path.exists('database.db'):
        os.remove('database.db')
        print("Old database removed.")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # 1. Users
    cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')

    # 2. Classrooms
    cursor.execute('CREATE TABLE classrooms (id INTEGER PRIMARY KEY, name TEXT UNIQUE)')

    # 3. Sessions (with faculty_notes column)
    cursor.execute('''CREATE TABLE sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        class_id INTEGER, 
                        session_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        video_path TEXT,
                        avg_attentiveness REAL,
                        total_students INTEGER,
                        faculty_notes TEXT,
                        FOREIGN KEY(class_id) REFERENCES classrooms(id))''')

    # 4. Faculty Journal (Fixed structure)
    cursor.execute('''CREATE TABLE faculty_journal (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        class_id INTEGER,
                        note_date TEXT,
                        note_time TEXT,
                        content TEXT,
                        FOREIGN KEY (class_id) REFERENCES classrooms (id))''')

    # Add default data
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    cursor.execute("INSERT INTO classrooms (name) VALUES ('Class A')")
    cursor.execute("INSERT INTO classrooms (name) VALUES ('Class B')")

    conn.commit()
    conn.close()
    print("✅ Database initialized freshly!")

if __name__ == '__main__':
    init()