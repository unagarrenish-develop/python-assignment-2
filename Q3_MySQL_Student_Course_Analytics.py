"""Q3: Load CSV student/registration data into MySQL and query course analytics.
Install: pip install mysql-connector-python
CSV headers: student.csv: student_id,name,spi
registration.csv: student_id,course_id
"""
import csv
import getpass
import sys

def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))

def main():
    try:
        import mysql.connector
    except ImportError:
        print("Install dependency: pip install mysql-connector-python", file=sys.stderr)
        return
    host = input("MySQL host [localhost]: ").strip() or "localhost"
    user = input("MySQL user: ").strip()
    password = getpass.getpass("MySQL password: ")
    database = input("Database name: ").strip()
    student_file = input("Student CSV path: ").strip()
    registration_file = input("Registration CSV path: ").strip()
    course_id = input("Course ID: ").strip()
    try:
        threshold = float(input("SPI threshold: "))
        if not 0 <= threshold <= 10: raise ValueError("SPI threshold must be between 0 and 10")
        students, registrations = read_csv(student_file), read_csv(registration_file)
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Student (
            student_id VARCHAR(50) PRIMARY KEY, name VARCHAR(200) NOT NULL,
            spi DECIMAL(3,1) NOT NULL)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS CourseRegistration (
            student_id VARCHAR(50) NOT NULL, course_id VARCHAR(50) NOT NULL,
            PRIMARY KEY(student_id, course_id),
            FOREIGN KEY(student_id) REFERENCES Student(student_id))""")
        cursor.executemany("INSERT INTO Student(student_id,name,spi) VALUES(%s,%s,%s) "
                           "ON DUPLICATE KEY UPDATE name=VALUES(name), spi=VALUES(spi)",
                           [(r["student_id"], r["name"], float(r["spi"])) for r in students])
        cursor.executemany("INSERT IGNORE INTO CourseRegistration(student_id,course_id) VALUES(%s,%s)",
                           [(r["student_id"], r["course_id"]) for r in registrations])
        connection.commit()
        cursor.execute("""SELECT s.student_id, s.name, s.spi, r.course_id
            FROM Student s JOIN CourseRegistration r ON s.student_id=r.student_id
            WHERE r.course_id=%s AND s.spi>%s
            ORDER BY s.spi DESC, s.student_id ASC""", (course_id, threshold))
        for row in cursor.fetchall():
            print(row[0], row[1], f"{float(row[2]):g}", row[3])
        cursor.close(); connection.close()
    except (OSError, ValueError, KeyError, Exception) as exc:
        print(f"Database/input error: {exc}", file=sys.stderr)

if __name__ == "__main__":
    main()
