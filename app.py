import grpc
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import grading_pb2
import grading_pb2_grpc

app = Flask(__name__)
CORS(app)

# Insecure channel for local development
channel = grpc.insecure_channel('localhost:50051')
grading_stub = grading_pb2_grpc.GradingServiceStub(channel)

@app.route('/')
def home():
    return render_template('/template/index.html')

@app.route('/grades', methods=['GET'])
def get_all_grades():
    try:
        response = grading_stub.GetAllGrades(grading_pb2.Empty())
        grades = [{
            'id': grade.id,
            'student_name': grade.student_name,
            'course_name': grade.course_name,
            'score': grade.score
        } for grade in response.grades]
        return jsonify(grades), 200
    except grpc.RpcError as e:
        logging.error(f"Error getting all grades: {e}")
        return jsonify({'error': 'Failed to fetch grades'}), 500

@app.route('/grades', methods=['POST'])
def add_grade():
    try:
        data = request.json
        grade = grading_pb2.Grade(
            id=data['id'],
            student_name=data['student_name'],
            course_name=data['course_name'],
            score=data['score']
        )
        response = grading_stub.AddGrade(grade)
        return jsonify({'message': 'Grade added successfully'}), 201
    except grpc.RpcError as e:
        logging.error(f"Error adding grade: {e}")
        return jsonify({'error': 'Failed to add grade'}), 500

@app.route('/grades/<string:id>', methods=['GET'])
def get_grade(id):
    try:
        response = grading_stub.GetGrade(grading_pb2.GradeId(id=id))
        if not response.id:
            return jsonify({'error': 'Grade not found'}), 404
        grade = {
            'id': response.id,
            'student_name': response.student_name,
            'course_name': response.course_name,
            'score': response.score
        }
        return jsonify(grade), 200
    except grpc.RpcError as e:
        logging.error(f"Error getting grade: {e}")
        return jsonify({'error': 'Failed to fetch grade'}), 500

@app.route('/grades/<string:id>', methods=['PUT'])
def update_grade(id):
    try:
        data = request.json
        grade = grading_pb2.Grade(
            id=id,
            student_name=data['student_name'],
            course_name=data['course_name'],
            score=data['score']
        )
        response = grading_stub.UpdateGrade(grade)
        if response.id == '':
            return jsonify({'error': 'Grade not found'}), 404
        return jsonify({'message': 'Grade updated successfully'}), 200
    except grpc.RpcError as e:
        logging.error(f"Error updating grade: {e}")
        return jsonify({'error': 'Failed to update grade'}), 500

@app.route('/grades/<string:id>', methods=['DELETE'])
def delete_grade(id):
    try:
        response = grading_stub.DeleteGrade(grading_pb2.GradeId(id=id))
        if response.result == 'Grade deleted successfully':
            return jsonify({'message': 'Grade deleted successfully'}), 200
        elif response.result == 'Grade not found':
            return jsonify({'error': 'Grade not found'}), 404
        else:
            return jsonify({'error': 'Failed to delete grade'}), 500
    except grpc.RpcError as e:
        logging.error(f"Error deleting grade: {e}")
        return jsonify({'error': 'Failed to delete grade'}), 500

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5003)
