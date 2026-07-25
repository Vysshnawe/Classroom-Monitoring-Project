import sqlite3

def setup_notes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Create a table that stores notes independently of specific video files
    cursor.execute('''CREATE TABLE IF NOT EXISTS faculty_journal (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        class_id INTEGER,
                        note_date TEXT,
                        note_time TEXT,
                        content TEXT,
                        FOREIGN KEY (class_id) REFERENCES classrooms (id))''')
    conn.commit()
    conn.close()
    print("Faculty Journal table created!")

if __name__ == '__main__':
    setup_notes()