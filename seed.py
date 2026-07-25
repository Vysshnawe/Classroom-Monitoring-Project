import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
# Add initial classrooms
cursor.execute("INSERT OR IGNORE INTO classrooms (name) VALUES ('Class A')")
cursor.execute("INSERT OR IGNORE INTO classrooms (name) VALUES ('Class B')")
conn.commit()
conn.close()
print("Classrooms added successfully!")