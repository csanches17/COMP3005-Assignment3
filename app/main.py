import getpass
import psycopg
from datetime import date

db_password = None

# Establishes connection to the local PostgreSQL database using the provided password.
def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="comp3005_assignment3",
        user="postgres",
        password=db_password,
    )


# Retrieves and displays all students from the database.
def getAllStudents():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM students ORDER BY student_id;")
                students = cursor.fetchall()

                if not students:
                    print("No students found.")
                    return
                
                print("\nList of Students:")
                for student in students:
                    print(student)

    except psycopg.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")


# Adds a new student to the database with the provided details.
def addStudent(first_name, last_name, email, enrollment_date):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO students (
                    first_name, 
                    last_name, 
                    email, 
                    enrollment_date
                    ) VALUES (%s, %s, %s, %s) 
                    RETURNING student_id;
                    """,
                    (first_name, last_name, email, enrollment_date),
                )
                new_student_id = cursor.fetchone()[0]
                print(f"\nStudent added with ID: {new_student_id}")
    
    except psycopg.Error as e:
        print(f"DB error when adding: {e}")


# Updates the email of an existing student based on their student ID.
def updateStudentEmail(student_id, new_email):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE students 
                    SET email = %s 
                    WHERE student_id = %s;
                    """,
                    (new_email, student_id)
                )
                if cursor.rowcount == 0:
                    print(f"\nNo student found with ID: {student_id}")
                else:
                    print(f"\nStudent ID {student_id} email updated to {new_email}")

    except psycopg.Error as e:
        print(f"DB error when updating: {e}")


# Deletes a student from the database based on their student ID.
def deleteStudent(student_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM students 
                    WHERE student_id = %s;
                    """,
                    (student_id,)
                )
                if cursor.rowcount == 0:
                    print(f"\nNo student found with ID: {student_id}")
                else:
                    print(f"\nStudent ID {student_id} deleted successfully.")

    except psycopg.Error as e:
        print(f"DB error when deleting: {e}")

if __name__ == "__main__":
    db_password = getpass.getpass("Enter your PostgreSQL password: ")
    
    while True:
        print("\nStudent Management System")
        print("1. View all students")
        print("2. Add a new student")
        print("3. Update a student's email")
        print("4. Delete a student")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            getAllStudents()
        elif choice == "2":
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")

            # Validate date before inserting
            while True:
                date_input = input("Enter enrollment date (YYYY-MM-DD): ").strip()

                try:
                    enrollment_date = date.fromisoformat(date_input)

                    if enrollment_date.isoformat() != date_input:
                        print("Invalid date format. Please use YYYY-MM-DD.")
                        continue

                    # Check if the date is in the future
                    if enrollment_date > date.today():
                        print("Enrollment date cannot be in the future. Please enter a valid date.")
                        continue

                    break # Valid date
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")

            addStudent(first_name, last_name, email, enrollment_date)
        elif choice == "3":
            try:
                student_id = int(input("Enter student ID to update: "))
                new_email = input("Enter new email: ")
                updateStudentEmail(student_id, new_email)
            except ValueError:
                print("Student ID must be an integer.")
        elif choice == "4":
            try:
                student_id = int(input("Enter student ID to delete: "))
                deleteStudent(student_id)
            except ValueError:
                print("Student ID must be an integer.")
        elif choice == "5":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

