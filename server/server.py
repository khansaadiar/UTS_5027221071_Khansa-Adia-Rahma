import grpc
import logging
from concurrent import futures
import sys
sys.path.append('../')
import time
import pymongo
import grading_pb2
import grading_pb2_grpc

class GradingService(grading_pb2_grpc.GradingServiceServicer):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["GradingSystem"]
        self.grades_collection = self.db["Grades"]
        logging.info("Grading service initialized. Feeling Connected to MongoDB.")

    def AddGrade(self, request, context):
        logging.info(f"A request to add a new grade has been received:: {request}")
        try:
            grade_data = {
                "id": request.id,
                "student_name": request.student_name,
                "course_name": request.course_name,
                "score": request.score
            }
            self.grades_collection.insert_one(grade_data)
            logging.info("Grade added successfully to the system.")
            return grading_pb2.Empty()
        except Exception as e:
            error_msg = f"Oops! Error adding grade: {e}"
            logging.error(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(error_msg)
            return grading_pb2.Empty()

    def GetGrade(self, request, context):
        logging.info(f"A request to retrieve a grade with ID: {request.id} has been received.")
        try:
            grade_data = self.grades_collection.find_one({"id": request.id})
            if grade_data:
                logging.info("Grade found.")
                return grading_pb2.Grade(
                    id=grade_data["id"],
                    student_name=grade_data["student_name"],
                    course_name=grade_data["course_name"],
                    score=grade_data["score"]
                )
            else:
                logging.info("Grade not found.")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Grade not found")
                return grading_pb2.Grade()
        except Exception as e:
            error_msg = f"Error getting grade: {e}"
            logging.error(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(error_msg)
            return grading_pb2.Grade()

    def GetAllGrades(self, request, context):
        logging.info("A request to retrieve all grades has been received.")
        try:
            all_grades = list(self.grades_collection.find())
            grades_list = [grading_pb2.Grade(
                id=grade["id"],
                student_name=grade["student_name"],
                course_name=grade["course_name"],
                score=grade["score"]
            ) for grade in all_grades]
            logging.info("All grades retrieved successfully.")
            return grading_pb2.GradeList(grades=grades_list)
        except Exception as e:
            error_msg = f"Error getting all grades: {e}"
            logging.error(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(error_msg)
            return grading_pb2.GradeList()

    def UpdateGrade(self, request, context):
        logging.info(f"A request to update a grade has been received: {request}")
        try:
            update_result = self.grades_collection.update_one(
                {"id": request.id},
                {"$set": {
                    "student_name": request.student_name,
                    "course_name": request.course_name,
                    "score": request.score
                }}
            )
            if update_result.matched_count > 0:
                logging.info("Grade updated successfully.")
                return grading_pb2.Empty()
            else:
                logging.info("Couldn't find the grade to update. Try again?")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Grade not found")
                return grading_pb2.Empty()
        except Exception as e:
            error_msg = f"Error updating grade: {e}"
            logging.error(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(error_msg)
            return grading_pb2.Empty()

    def DeleteGrade(self, request, context):
        logging.info(f"A request to Delete a grade has been received: {request}")
        try:
            delete_result = self.grades_collection.delete_one({"id": request.id})
            if delete_result.deleted_count > 0:
                logging.info("Grade deleted successfully.")
                return grading_pb2.Empty()
            else:
                logging.info("Grade not found.")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Grade not found")
                return grading_pb2.Empty()
        except Exception as e:
            error_msg = f"Error deleting grade: {e}"
            logging.error(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(error_msg)
            return grading_pb2.Empty()

def serve():
    logging.basicConfig(level=logging.INFO)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grading_pb2_grpc.add_GradingServiceServicer_to_server(GradingService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Server started on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        server.stop(0)

if __name__ == '__main__':
    serve()
