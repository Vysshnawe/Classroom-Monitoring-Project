import sqlite3
import os

def restore_classes_from_folders():
    # Path to your dataset folder
    dataset_path = 'dataset'
    
    if not os.path.exists(dataset_path):
        print("❌ Dataset folder not found!")
        return

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Get all folder names in the dataset directory
    # These represent your classrooms
    folders = [f for f in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, f))]

    if not folders:
        print("Empty dataset folder. No classrooms to restore.")
        return

    for folder_name in folders:
        # Convert folder name back to a readable class name (e.g., Class_A -> Class A)
        display_name = folder_name.replace("_", " ")
        
        # Insert into database if it's missing
        cursor.execute("INSERT OR IGNORE INTO classrooms (name) VALUES (?)", (display_name,))
        print(f"✅ Restored classroom: {display_name}")

    conn.commit()
    conn.close()
    print("\nDone! Refresh your web app and check the Face Dataset page.")

if __name__ == '__main__':
    restore_classes_from_folders()