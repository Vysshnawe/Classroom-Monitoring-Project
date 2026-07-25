

import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 1. CREATE the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# 2. List of new users to add
new_users = [
    ('admin', 'admin123'),
    ('admin2', 'admin123'),
    ('admin3', 'admin123'),
    ('admin4', 'admin123'),
    ('admin5', 'admin123')
]

# 3. Insert users
try:
    cursor.executemany("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", new_users)
    conn.commit()
    print("Successfully initialized database and added users!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()