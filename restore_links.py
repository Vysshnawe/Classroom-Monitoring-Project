import sqlite3
import os

def restore_links():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Check what folders actually exist in your VS Code project
    if os.path.exists('dataset'):
        folders = [f for f in os.listdir('dataset') if os.path.isdir(os.path.join('dataset', f))]
        for folder in folders:
            # Convert folder name back to class name (e.g., Class_A to Class A)
            class_name = folder.replace("_", " ")
            cursor.execute("INSERT OR IGNORE INTO classrooms (name) VALUES (?)", (class_name,))
            print(f"Connected: {class_name}")
            
    conn.commit()
    conn.close()

if __name__ == '__main__':
    restore_links()