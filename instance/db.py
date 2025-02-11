import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("quiz_master.db")
cursor = conn.cursor()

# Run SQL commands
cursor.execute("DELETE FROM score")

# Commit and close the connection
conn.commit()
conn.close()
