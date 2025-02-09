import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("quiz_master.db")
cursor = conn.cursor()

# Run SQL commands
cursor.execute("ALTER TABLE question ADD COLUMN chapter_id INTEGER NOT NULL DEFAULT 1;")

# Commit and close the connection
conn.commit()
conn.close()
