import mysql.connector
from datetime import date

# -------- DATABASE CONNECTION --------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="library_db"
)

cursor = db.cursor()


# -------- BOOK FUNCTIONS --------

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author: ")
    quantity = int(input("Enter quantity: "))

    cursor.execute(
        "INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)",
        (title, author, quantity)
    )
    db.commit()
    print("Book added successfully!\n")


def search_book():
    keyword = input("Enter title keyword to search: ")

    cursor.execute(
        "SELECT * FROM books WHERE title LIKE %s",
        ('%' + keyword + '%',)
    )

    results = cursor.fetchall()

    if results:
        for row in results:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Quantity: {row[3]}")
    else:
        print("No matching books found.\n")


def view_books():
    cursor.execute("SELECT * FROM books")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Quantity: {row[3]}")


# -------- STUDENT FUNCTIONS --------

def add_student():
    name = input("Enter student name: ")
    student_class = input("Enter class: ")

    cursor.execute(
        "INSERT INTO students (name, class) VALUES (%s, %s)",
        (name, student_class)
    )
    db.commit()
    print("Student added successfully!\n")


def view_students():
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Name: {row[1]}, Class: {row[2]}")


# -------- ISSUE & RETURN --------

def issue_book():
    student_id = int(input("Enter Student ID: "))
    book_id = int(input("Enter Book ID: "))

    cursor.execute("SELECT quantity FROM books WHERE id = %s", (book_id,))
    result = cursor.fetchone()

    if result and result[0] > 0:
        new_quantity = result[0] - 1

        cursor.execute(
            "UPDATE books SET quantity = %s WHERE id = %s",
            (new_quantity, book_id)
        )

        cursor.execute(
            "INSERT INTO issue_records (student_id, book_id, issue_date, return_date) VALUES (%s, %s, %s, %s)",
            (student_id, book_id, date.today(), None)
        )

        db.commit()
        print("Book issued successfully!\n")
    else:
        print("Book not available.\n")


def return_book():
    issue_id = int(input("Enter Issue ID: "))

    cursor.execute(
        "SELECT book_id FROM issue_records WHERE issue_id = %s AND return_date IS NULL",
        (issue_id,)
    )

    result = cursor.fetchone()

    if result:
        book_id = result[0]

        cursor.execute(
            "UPDATE issue_records SET return_date = %s WHERE issue_id = %s",
            (date.today(), issue_id)
        )

        cursor.execute(
            "UPDATE books SET quantity = quantity + 1 WHERE id = %s",
            (book_id,)
        )

        db.commit()
        print("Book returned successfully!\n")
    else:
        print("Invalid Issue ID or already returned.\n")


def view_issued_books():
    cursor.execute("""
        SELECT issue_records.issue_id, students.name, books.title,
               issue_records.issue_date, issue_records.return_date
        FROM issue_records
        JOIN students ON issue_records.student_id = students.id
        JOIN books ON issue_records.book_id = books.id
    """)

    records = cursor.fetchall()

    for row in records:
        print(f"IssueID: {row[0]}, Student: {row[1]}, Book: {row[2]}, Issued: {row[3]}, Returned: {row[4]}")


# -------- MAIN MENU --------

while True:
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Add Student")
    print("5. View Students")
    print("6. Issue Book")
    print("7. Return Book")
    print("8. View Issue Records")
    print("9. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        view_books()
    elif choice == "3":
        search_book()
    elif choice == "4":
        add_student()
    elif choice == "5":
        view_students()
    elif choice == "6":
        issue_book()
    elif choice == "7":
        return_book()
    elif choice == "8":
        view_issued_books()
    elif choice == "9":
        break
    else:
        print("Invalid choice!")

cursor.close()
db.close()
