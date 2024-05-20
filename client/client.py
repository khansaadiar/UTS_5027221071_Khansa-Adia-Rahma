import grpc
import logging
import sys
sys.path.append('../')
import grading_pb2
import grading_pb2_grpc

def create_grade(stub):
    id = input("Enter grade ID: ")
    student_name = input("Enter student name: ")
    course_name = input("Enter course name: ")
    score = float(input("Enter score: "))

    grade = grading_pb2.Grade(
        id=id,
        student_name=student_name,
                course_name=course_name,
        score=score
    )
    try:
        response = stub.AddGrade(grade)
        print("AddGrade Response:", response)
    except grpc.RpcError as e:
        print(f"Error adding grade: {e.details()}")

def get_all_grades(stub):
    try:
        response = stub.GetAllGrades(grading_pb2.Empty())
        grades = response.grades
        for grade in grades:
            print("Grade ID:", grade.id)
            print("Student Name:", grade.student_name)
            print("Course Name:", grade.course_name)
            print("Score:", grade.score)
            print()
    except grpc.RpcError as e:
        print(f"Error getting all grades: {e.details()}")

def get_grade(stub):
    id = input("Enter grade ID: ")
    try:
        response = stub.GetGrade(grading_pb2.GradeId(id=id))
        print("GetGrade Response:")
        print("Grade ID:", response.id)
        print("Student Name:", response.student_name)
        print("Course Name:", response.course_name)
        print("Score:", response.score)
    except grpc.RpcError as e:
        print(f"Error getting grade: {e.details()}")

def update_grade(stub):
    id = input("Enter grade ID to update: ")
    student_name = input("Enter updated student name: ")
    course_name = input("Enter updated course name: ")
    score = float(input("Enter updated score: "))

    grade = grading_pb2.Grade(
        id=id,
        student_name=student_name,
        course_name=course_name,
        score=score
    )
    try:
        response = stub.UpdateGrade(grade)
        if response:
            print("UpdateGrade Response:", response)
        else:
            print("Grade not found.")
    except grpc.RpcError as e:
        print(f"Error updating grade: {e.details()}")

def delete_grade(stub):
    id = input("Enter grade ID to delete: ")
    try:
        response = stub.DeleteGrade(grading_pb2.GradeId(id=id))
        if response:
            print("DeleteGrade Response:", response)
        else:
            print("Grade not found.")
    except grpc.RpcError as e:
        print(f"Error deleting grade: {e.details()}")

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = grading_pb2_grpc.GradingServiceStub(channel)

    while True:
        print("\n1. Add Grade\n2. Get All Grades\n3. Get Grade\n4. Update Grade\n5. Delete Grade\n6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_grade(stub)
        elif choice == '2':
            get_all_grades(stub)
        elif choice == '3':
            get_grade(stub)
        elif choice == '4':
            update_grade(stub)
        elif choice == '5':
            delete_grade(stub)
        elif choice == '6':
            break
        else:
            print("Invalid choice! Please enter a valid option.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    run()
