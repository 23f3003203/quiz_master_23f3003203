import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash


faker = Faker()
db_path = "quiz_master.db"  # Change this to your actual database file path

# Establish connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Function to insert fake data
def seed_database():
    print("🌱 Seeding Database...")

    # Insert Users
    for _ in range(100):
        cursor.execute(
            "INSERT INTO user (username, password, full_name, qualification, dob) VALUES (?, ?, ?, ?, ?)",
            (faker.email(), generate_password_hash(str(1234567)), faker.name(), faker.job(), faker.date_of_birth(minimum_age=18, maximum_age=40).strftime('%Y-%m-%d'))
        )

    conn.commit()
    
    # Insert Subjects
    for _ in range(20):
        cursor.execute(
            "INSERT INTO subject (name, description) VALUES (?, ?)",
            (faker.word().capitalize(), faker.sentence())
        )
    
    conn.commit()

    # Get inserted subject IDs
    cursor.execute("SELECT id FROM subject")
    subject_ids = [row[0] for row in cursor.fetchall()]

    # Insert Chapters
    for i in range(50):
        cursor.execute(
            "INSERT INTO chapter (name, description, subject_id) VALUES (?, ?, ?)",
            (faker.word(), faker.sentence(), random.choice(subject_ids))
        )

    conn.commit()

    # Get inserted chapter IDs
    cursor.execute("SELECT id FROM chapter")
    chapter_ids = [row[0] for row in cursor.fetchall()]

    # Insert Quizzes
    for _ in range(200):
        cursor.execute(
            "INSERT INTO quiz (chapter_id, date_of_quiz, time_duration, remarks) VALUES (?, ?, ?, ?)",
            (random.choice(chapter_ids), faker.date_between(start_date="-1y", end_date="today").strftime('%Y-%m-%d'),
             f"{random.randint(10, 60)}:00", faker.sentence())
        )
    
    for _ in range(20):
        cursor.execute(
            "INSERT INTO quiz (chapter_id, date_of_quiz, time_duration, remarks) VALUES (?, ?, ?, ?)",
            (random.choice(chapter_ids), faker.date_between(start_date="today", end_date= "+1m").strftime('%Y-%m-%d'),
             f"{random.randint(10, 60)}:00", faker.sentence())
        )

    conn.commit()

    # Get inserted quiz IDs
    cursor.execute("SELECT id FROM quiz")
    quiz_ids = [row[0] for row in cursor.fetchall()]

    # Insert Questions
    for _ in range(1000):
        cursor.execute(
            "INSERT INTO question (quiz_id, chapter_id, question_statement, option1, option2, option3, option4, correct_option) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (random.choice(quiz_ids), random.choice(chapter_ids), faker.sentence(),
             faker.word(), faker.word(), faker.word(), faker.word(),
             random.choice(["option1", "option2", "option3", "option4"]))
        )

    conn.commit()

    # Get inserted user IDs
    cursor.execute("SELECT id FROM user")
    user_ids = [row[0] for row in cursor.fetchall()]

    # Insert Scores
    for _ in range(500):
        cursor.execute(
            "INSERT INTO score (quiz_id, user_id, time_stamp_of_attempt, total_scored) VALUES (?, ?, ?, ?)",
            (random.choice(quiz_ids), random.choice(user_ids),
             (datetime.utcnow() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S'),
             random.randint(0, 100))
        )

    conn.commit()
    print("✅ Database seeding completed successfully!")

# Run the seeding function

cursor.execute("SELECT id FROM subject")
subject_ids = [row[0] for row in cursor.fetchall()]

# Insert Chapters
for i in range(50):
    cursor.execute(
        "INSERT INTO chapter (name, description, subject_id) VALUES (?, ?, ?)",
        (faker.word(), faker.sentence(), random.choice(subject_ids))
    )

conn.commit()

# Close the connection
conn.close()
