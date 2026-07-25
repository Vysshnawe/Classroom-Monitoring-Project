import sqlite3

def update_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        # This adds the missing 'faculty_notes' column to your sessions table
        cursor.execute('ALTER TABLE sessions ADD COLUMN faculty_notes TEXT;')
        conn.commit()
        print("Success: 'faculty_notes' column added to database.")
    except sqlite3.OperationalError:
        print("Note: The column might already exist.")
    finally:
        conn.close()

if __name__ == '__main__':
    update_database()