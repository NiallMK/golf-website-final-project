import sqlite3
from datetime import datetime, timedelta

DB_PATH = "golf-website.db"

START_TIME = 8    # 08:00
END_TIME = 16     # 16:00
INTERVAL = 10     # minutes
DAYS = 14

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Get all courses
cur.execute("SELECT id FROM courses")
courses = [row[0] for row in cur.fetchall()]

today = datetime.today().date()

for course_id in courses:
    for day in range(DAYS):
        date = today + timedelta(days=day)

        hour = START_TIME
        minute = 0

        while hour < END_TIME:
            time_str = f"{hour:02d}:{minute:02d}"

            cur.execute("""
                INSERT INTO tee_times (course_id, date, time, holes, is_booked)
                VALUES (?, ?, ?, 18, 0)
            """, (course_id, date.isoformat(), time_str))

            minute += INTERVAL
            if minute >= 60:
                minute = 0
                hour += 1

conn.commit()
conn.close()

print("Tee times seeded successfully")
