import json
import os

DATA_FILE = "student_results.json"

class Student:
    def __init__(self, matric_no, name, level):
        self.matric_no = matric_no
        self.name = name
        self.level = level
        self.grades = {}  # course_code: grade (0-5)

class Course:
    def __init__(self, code, title, credit_unit):
        self.code = code.upper()
        self.title = title
        self.credit_unit = credit_unit

class ResultManager:
    def __init__(self):
        self.students = []
        self.courses = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                # Load courses
                for c in data.get("courses", []):
                    course = Course(c["code"], c["title"], c["credit_unit"])
                    self.courses.append(course)
                # Load students
                for s in data.get("students", []):
                    student = Student(s["matric_no"], s["name"], s["level"])
                    student.grades = s["grades"]
                    self.students.append(student)
            except Exception as e:
                print(f"Error loading data: {e}. Starting empty.")

    def save_data(self):
        data = {
            "courses": [{"code": c.code, "title": c.title, "credit_unit": c.credit_unit} for c in self.courses],
            "students": [{"matric_no": s.matric_no, "name": s.name, "level": s.level, "grades": s.grades} for s in self.students]
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print("Data saved successfully.")

    def add_student(self):
        matric_no = input("Enter Matric Number (e.g., CSC/2023/1234): ").strip().upper()
        if any(s.matric_no == matric_no for s in self.students):
            print("Matric number already exists!")
            return
        name = input("Enter full name: ").strip()
        level = input("Enter level (e.g., 200): ").strip()
        student = Student(matric_no, name, level)
        self.students.append(student)
        print(f"Student added successfully! Matric No: {matric_no}")

    def add_course(self):
        code = input("Enter course code (e.g., CSC201): ").strip().upper()
        if any(c.code == code for c in self.courses):
            print("Course code already exists!")
            return
        title = input("Enter course title: ").strip()
        try:
            credit = int(input("Enter credit unit: "))
        except ValueError:
            print("Invalid credit unit.")
            return
        course = Course(code, title, credit)
        self.courses.append(course)
        print(f"Course added: {code} - {title} ({credit} units)")

    def record_grade(self):
        matric_no = input("Enter student's Matric Number: ").strip().upper()
        student = next((s for s in self.students if s.matric_no == matric_no), None)
        if not student:
            print("Student not found.")
            return

        self.view_all_courses()
        code = input("\nEnter course code: ").strip().upper()
        course = next((c for c in self.courses if c.code == code), None)
        if not course:
            print("Course not found.")
            return

        try:
            grade = float(input(f"Enter grade for {code} (0-5): "))
            if not 0 <= grade <= 5:
                print("Grade must be between 0 and 5.")
                return
        except ValueError:
            print("Invalid grade.")
            return

        student.grades[code] = grade
        print(f"Grade recorded: {code} = {grade}")

    def calculate_gpa(self, student):
        if not student.grades:
            return 0.0
        total_points = 0
        total_credits = 0
        for code, grade in student.grades.items():
            course = next((c for c in self.courses if c.code == code), None)
            if course:
                total_points += grade * course.credit_unit
                total_credits += course.credit_unit
        return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

    def view_student_result(self):
        matric_no = input("Enter Matric Number: ").strip().upper()
        student = next((s for s in self.students if s.matric_no == matric_no), None)
        if not student:
            print("Student not found.")
            return

        gpa = self.calculate_gpa(student)
        print(f"\nResult for {student.name} ({student.matric_no}) - Level {student.level}")
        print(f"{'Course':<10} {'Title':<35} {'Credit':<8} {'Grade':<8}")
        print("-" * 70)
        for code, grade in student.grades.items():
            course = next((c for c in self.courses if c.code == code), None)
            title = course.title if course else "Unknown"
            credit = course.credit_unit if course else "?"
            print(f"{code:<10} {title:<35} {credit:<8} {grade:<8}")
        print("-" * 70)
        print(f"Total GPA: {gpa:.2f}")

    def view_all_students(self):
        if not self.students:
            print("No students registered yet.")
            return
        print("\nAll Students:")
        print(f"{'Matric No':<15} {'Name':<30} {'Level':<8} {'GPA':<8}")
        print("-" * 70)
        for s in self.students:
            gpa = self.calculate_gpa(s)
            print(f"{s.matric_no:<15} {s.name:<30} {s.level:<8} {gpa:<8.2f}")

    def view_all_courses(self):
        if not self.courses:
            print("No courses added yet.")
            return
        print("\nAll Courses:")
        print(f"{'Code':<10} {'Title':<40} {'Credit':<8}")
        print("-" * 65)
        for c in self.courses:
            print(f"{c.code:<10} {c.title:<40} {c.credit_unit:<8}")

    def search_student(self):
        query = input("Enter matric number or name keyword: ").strip().lower()
        results = [s for s in self.students if query in s.matric_no.lower() or query in s.name.lower()]
        if not results:
            print("No matching students found.")
            return
        print("\nSearch Results:")
        for s in results:
            print(f"{s.matric_no} - {s.name} (Level {s.level})")

    def display_menu(self):
        print("\n" + "="*60)
        print("     STUDENT RESULT MANAGEMENT SYSTEM")
        print("="*60)
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Record Grade")
        print("4. View Student Result (GPA)")
        print("5. View All Students")
        print("6. View All Courses")
        print("7. Search Student")
        print("8. Exit & Save")
        print("="*60)

def main():
    manager = ResultManager()
    print("Welcome to Student Result Management System\n")

    while True:
        manager.display_menu()
        choice = input("Choose (1-8): ").strip()

        if choice == "1":
            manager.add_student()
        elif choice == "2":
            manager.add_course()
        elif choice == "3":
            manager.record_grade()
        elif choice == "4":
            manager.view_student_result()
        elif choice == "5":
            manager.view_all_students()
        elif choice == "6":
            manager.view_all_courses()
        elif choice == "7":
            manager.search_student()
        elif choice == "8":
            manager.save_data()
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()