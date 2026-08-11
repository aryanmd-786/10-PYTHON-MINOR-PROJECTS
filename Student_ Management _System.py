import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =========================
# DATABASE
# =========================

def connect_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            course TEXT NOT NULL,
            semester TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================
# ADD STUDENT
# =========================

def add_student():
    name = name_entry.get().strip()
    roll_no = roll_entry.get().strip()
    course = course_entry.get().strip()
    semester = semester_combo.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if name == "" or roll_no == "" or course == "" or semester == "":
        messagebox.showwarning(
            "Missing Information",
            "Please fill all required fields."
        )
        return

    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students
            (name, roll_no, course, semester, phone, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, roll_no, course, semester, phone, email))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Roll Number already exists."
        )


# =========================
# DISPLAY STUDENTS
# =========================

def display_students():
    for row in student_table.get_children():
        student_table.delete(row)

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    for student in students:
        student_table.insert("", tk.END, values=student)


# =========================
# SEARCH STUDENT
# =========================

def search_student():
    search_text = search_entry.get().strip()

    for row in student_table.get_children():
        student_table.delete(row)

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ?
        OR roll_no LIKE ?
        OR course LIKE ?
    """, (
        "%" + search_text + "%",
        "%" + search_text + "%",
        "%" + search_text + "%"
    ))

    students = cursor.fetchall()
    conn.close()

    for student in students:
        student_table.insert("", tk.END, values=student)


# =========================
# DELETE STUDENT
# =========================

def delete_student():
    selected = student_table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Student",
            "Please select a student first."
        )
        return

    student = student_table.item(selected[0])
    student_id = student["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Deleted",
            "Student deleted successfully!"
        )

        display_students()


# =========================
# SELECT STUDENT
# =========================

def select_student(event):
    selected = student_table.selection()

    if not selected:
        return

    student = student_table.item(selected[0])
    values = student["values"]

    clear_fields()

    name_entry.insert(0, values[1])
    roll_entry.insert(0, values[2])
    course_entry.insert(0, values[3])
    semester_combo.set(values[4])
    phone_entry.insert(0, values[5])
    email_entry.insert(0, values[6])


# =========================
# UPDATE STUDENT
# =========================

def update_student():
    selected = student_table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Student",
            "Please select a student first."
        )
        return

    student = student_table.item(selected[0])
    student_id = student["values"][0]

    name = name_entry.get().strip()
    roll_no = roll_entry.get().strip()
    course = course_entry.get().strip()
    semester = semester_combo.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if name == "" or roll_no == "" or course == "" or semester == "":
        messagebox.showwarning(
            "Missing Information",
            "Please fill all required fields."
        )
        return

    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE students
            SET name = ?,
                roll_no = ?,
                course = ?,
                semester = ?,
                phone = ?,
                email = ?
            WHERE id = ?
        """, (
            name,
            roll_no,
            course,
            semester,
            phone,
            email,
            student_id
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Student updated successfully!"
        )

        clear_fields()
        display_students()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Roll Number already exists."
        )


# =========================
# CLEAR FIELDS
# =========================

def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    semester_combo.set("")
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)


# =========================
# MAIN WINDOW
# =========================

connect_db()

root = tk.Tk()
root.title("Student Management System")
root.geometry("1100x650")
root.configure(bg="#f4f6f8")


# =========================
# TITLE
# =========================

title = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 24, "bold"),
    bg="#1f4e78",
    fg="white",
    pady=15
)

title.pack(fill=tk.X)


# =========================
# INPUT FRAME
# =========================

input_frame = tk.Frame(
    root,
    bg="white",
    padx=20,
    pady=15
)

input_frame.pack(
    fill=tk.X,
    padx=20,
    pady=15
)


# Name
tk.Label(
    input_frame,
    text="Student Name",
    bg="white",
    font=("Arial", 11, "bold")
).grid(row=0, column=0, padx=10, pady=8, sticky="w")

name_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 11)
)

name_entry.grid(row=0, column=1, padx=10)


# Roll Number
tk.Label(
    input_frame,
    text="Roll Number",
    bg="white",
    font=("Arial", 11, "bold")
).grid(row=0, column=2, padx=10, pady=8, sticky="w")

roll_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 11)
)

roll_entry.grid(row=0, column=3, padx=10)


# Course
tk.Label(
    input_frame,
    text="Course",
    bg="white",
    font=("Arial", 11, "bold")
).grid(row=1, column=0, padx=10, pady=8, sticky="w")

course_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 11)
)

course_entry.grid(row=1, column=1, padx=10)


# Semester
tk.Label(
    input_frame,
    text="Semester",
    bg="white",
    font=("Arial", 11, "bold")
).grid(row=1, column=2, padx=10, pady=8, sticky="w")

semester_combo = ttk.Combobox(
    input_frame,
    values=[
        "1st",
        "2nd",
        "3rd",
        "4th",
        "5th",
        "6th"
    ],
    width=23,
    state="readonly",
    font=("Arial", 11)
)

semester_combo.grid(row=1, column=3, padx=10)


# Phone
tk.Label(
    input_frame,
    text="Phone",
    bg="white",
    font=("Arial", 11, "bold")
).grid(row=2, column=0, padx=10, pady=8, sticky="w")

phone_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 11)
)

phone_entry.grid(row=2, column=1, padx=10)


# Email
tk.Label(
    input_frame,
    text="Email",
    bg="white",
    font=("Arial", 11, "bold")
).grid(row=2, column=2, padx=10, pady=8, sticky="w")

email_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 11)
)

email_entry.grid(row=2, column=3, padx=10)


# =========================
# BUTTONS
# =========================

button_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

button_frame.pack(pady=5)

tk.Button(
    button_frame,
    text="Add Student",
    command=add_student,
    width=15,
    bg="#198754",
    fg="white",
    font=("Arial", 10, "bold")
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Update",
    command=update_student,
    width=15,
    bg="#0d6efd",
    fg="white",
    font=("Arial", 10, "bold")
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Delete",
    command=delete_student,
    width=15,
    bg="#dc3545",
    fg="white",
    font=("Arial", 10, "bold")
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    width=15,
    bg="#6c757d",
    fg="white",
    font=("Arial", 10, "bold")
).grid(row=0, column=3, padx=5)


# =========================
# SEARCH
# =========================

search_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

search_frame.pack(
    fill=tk.X,
    padx=20,
    pady=10
)

tk.Label(
    search_frame,
    text="Search:",
    bg="#f4f6f8",
    font=("Arial", 11, "bold")
).pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(
    search_frame,
    width=40,
    font=("Arial", 11)
)

search_entry.pack(side=tk.LEFT, padx=5)

tk.Button(
    search_frame,
    text="Search",
    command=search_student,
    width=12,
    bg="#1f4e78",
    fg="white",
    font=("Arial", 10, "bold")
).pack(side=tk.LEFT, padx=5)

tk.Button(
    search_frame,
    text="Show All",
    command=display_students,
    width=12,
    bg="#495057",
    fg="white",
    font=("Arial", 10, "bold")
).pack(side=tk.LEFT, padx=5)


# =========================
# TABLE
# =========================

table_frame = tk.Frame(root)

table_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=20,
    pady=10
)

columns = (
    "ID",
    "Name",
    "Roll No",
    "Course",
    "Semester",
    "Phone",
    "Email"
)

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for column in columns:

    student_table.heading(
        column,
        text=column
    )

    student_table.column(
        column,
        width=130
    )


student_table.column(
    "ID",
    width=50
)

student_table.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)


# Scrollbar

scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.VERTICAL,
    command=student_table.yview
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)

student_table.configure(
    yscrollcommand=scrollbar.set
)


# Select student from table
student_table.bind(
    "<ButtonRelease-1>",
    select_student
)


# Load existing students
display_students()


# =========================
# START APPLICATION
# =========================

root.mainloop()