import getpass
import psycopg


def test_connection():
    password = getpass.getpass("Enter your PostgreSQL password: ")

    try:
        with psycopg.connect(
            host="localhost",
            port=5432,
            dbname="comp3005_assignment3",
            user="postgres",
            password=password,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT student_id, first_name, last_name FROM students ORDER BY student_id;")
                students = cursor.fetchall()
                print("Connection to PostgreSQL successful!")

                for student in students:
                    print(student)
    
    except psycopg.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")


if __name__ == "__main__":
    test_connection()