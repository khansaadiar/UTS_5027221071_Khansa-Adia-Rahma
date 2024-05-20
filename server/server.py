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
        logging.info("Connected to MongoDB")

    def AddGrade(self, request, context):
        logging.info(f"Received AddGrade request: {request}")
        try:
            self.grades_collection.insert_one({
                "id": request.id,
                "student_name": request.student_name,
                "course_name": request.course_name,
                "score": request.score
            })
            return grading_pb2.Empty()
        except Exception as e:
            logging.error(f"Error adding grade: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to add grade")
            return grading_pb2.Empty()

    def GetGrade(self, request, context):
        logging.info(f"Received GetGrade request for ID: {request.id}")
        try:
            grade_data = self.grades_collection.find_one({"id": request.id})
            if grade_data:
                return grading_pb2.Grade(
                    id=grade_data["id"],
                    student_name=grade_data["student_name"],
                    course_name=grade_data["course_name"],
                    score=grade_data["score"]
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Grade not found")
                return grading_pb2.Grade()
        except Exception as e:
            logging.error(f"Error getting grade: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to get grade")
            return grading_pb2.Grade()

    def GetAllGrades(self, request, context):
        logging.info("Received GetAllGrades request")
        try:
            all_grades = list(self.grades_collection.find())
            grades_list = [grading_pb2.Grade(
                id=grade["id"],
                student_name=grade["student_name"],
                course_name=grade["course_name"],
                score=grade["score"]
            ) for grade in all_grades]
            return grading_pb2.GradeList(grades=grades_list)
        except Exception as e:
            logging.error(f"Error getting all grades: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to get all grades")
            return grading_pb2.GradeList()

    def UpdateGrade(self, request, context):
        logging.info(f"Received UpdateGrade request: {request}")
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
                return grading_pb2.Empty()
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Grade not found")
                return grading_pb2.Empty()
        except Exception as e:
            logging.error(f"Error updating grade: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to update grade")
            return grading_pb2.Empty()

    def DeleteGrade(self, request, context):
        logging.info(f"Received DeleteGrade request for ID: {request.id}")
        try:
            delete_result = self.grades_collection.delete_one({"id": request.id})
            if delete_result.deleted_count > 0:
                return grading_pb2.Empty()
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Grade not found")
                return grading_pb2.Empty()
        except Exception as e:
            logging.error(f"Error deleting grade: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to delete grade")
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
            time.sleep(86400)  # One day in seconds
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        server.stop(0)

if __name__ == '__main__':
    serve()
