import sqlite3

def clear_only_history():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        # 1. Clear the session records (The Dashboard History list)
        cursor.execute('DELETE FROM sessions')
        
        # 2. Clear the faculty journal entries
        cursor.execute('DELETE FROM faculty_journal')
        
        conn.commit()
        print("✅ History and Journal cleared!")
        print("📁 Your 'dataset' folder and 'classrooms' table remain untouched.")
        
    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    clear_only_history()