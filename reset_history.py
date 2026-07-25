import sqlite3

def clear_all_history():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        # 1. Clear the session records (The "History" list)
        cursor.execute('DELETE FROM sessions')
        
        # 2. Clear the faculty journal notes
        cursor.execute('DELETE FROM faculty_journal')
        
        conn.commit()
        print("✅ Success: All class history and journal entries have been removed.")
        print("Your Dashboard will now show 'No Data' until you upload a new video.")
        
    except sqlite3.Error as e:
        print(f"❌ An error occurred: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    clear_all_history()