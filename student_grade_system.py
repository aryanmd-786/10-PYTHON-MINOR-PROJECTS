"""
Student Grade System
A simple command-line application to manage student grades.
Features:
- Add a new student
- Add a grade (subject and score) for an existing student
- Calculate average grade for a student
- Determine letter grade (A-F) based on average
- Display all students and their grades
- Exit the program
"""

class Student:
    """Represents a student with a name and a dictionary of subject: grade."""
    
    def __init__(self, name):
        self.name = name
        self.grades = {}   # subject -> score (float)
    
    def add_grade(self, subject, score):
        """Add or update a grade for a subject. Score must be between 0 and 100."""
        if not (0 <= score <= 100):
            raise ValueError("Grade must be between 0 and 100")
        self.grades[subject] = score
    
    def get_average(self):
        """Return the average score across all subjects, or 0 if no grades."""
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)
    
    def get_letter_grade(self):
        """Return the letter grade based on the average score."""
        avg = self.get_average()
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'
    
    def __str__(self):
        """String representation for display."""
        grade_str = ', '.join(f"{subj}: {score:.1f}" for subj, score in self.grades.items())
        if not grade_str:
            grade_str = "No grades"
        return f"{self.name} | Avg: {self.get_average():.2f} | Letter: {self.get_letter_grade()} | Grades: {grade_str}"


class GradeSystem:
    """Manages a collection of students."""
    
    def __init__(self):
        self.students = {}   # name -> Student object
    
    def add_student(self, name):
        """Add a new student. Raises ValueError if name already exists."""
        if name in self.students:
            raise ValueError(f"Student '{name}' already exists.")
        self.students[name] = Student(name)
        print(f"Student '{name}' added successfully.")
    
    def get_student(self, name):
        """Return the Student object, or None if not found."""
        return self.students.get(name)
    
    def add_grade(self, name, subject, score):
        """Add a grade to a student. Raises ValueError if student not found or invalid score."""
        student = self.get_student(name)
        if not student:
            raise ValueError(f"Student '{name}' not found.")
        student.add_grade(subject, score)
        print(f"Grade {score} added for {name} in {subject}.")
    
    def display_all(self):
        """Print all students and their grades."""
        if not self.students:
            print("No students in the system.")
            return
        print("\n--- All Students ---")
        for student in self.students.values():
            print(student)
        print("--------------------\n")
    
    def display_student(self, name):
        """Print details for a single student."""
        student = self.get_student(name)
        if not student:
            print(f"Student '{name}' not found.")
            return
        print(student)


def main():
    """Main menu loop."""
    system = GradeSystem()
    
    while True:
        print("\n===== Student Grade System =====")
        print("1. Add student")
        print("2. Add grade")
        print("3. View all students")
        print("4. View a specific student")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            name = input("Enter student name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            try:
                system.add_student(name)
            except ValueError as e:
                print(e)
        
        elif choice == '2':
            name = input("Enter student name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            subject = input("Enter subject: ").strip()
            if not subject:
                print("Subject cannot be empty.")
                continue
            try:
                score = float(input("Enter grade (0-100): "))
                system.add_grade(name, subject, score)
            except ValueError as e:
                print(f"Invalid input: {e}")
        
        elif choice == '3':
            system.display_all()
        
        elif choice == '4':
            name = input("Enter student name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            system.display_student(name)
        
        elif choice == '5':
            print("Exiting system. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == "__main__":
    main()