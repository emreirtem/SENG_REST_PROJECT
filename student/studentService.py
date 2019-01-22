from flask import Flask
from flask import Response
from flask import request
import pandas as pd
from studentManager import StudentManager
from studentModel import Student
from flask import jsonify
from flask import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def to_json_response(out:dict)-> Response:
    return app.response_class(
        response=json.dumps(out),
        status=200,
        mimetype='application/json'
    )

@app.route('/student/<int:student_id>/validate', methods=['GET'])
def is_student_valid(student_id:int):
    try:
        out = StudentManager.isStudentIdValid(student_id)
    except (AssertionError, KeyError, ValueError) as e:
        out = {"success":False,"desc": str(e)}
    return to_json_response(out)
    

@app.route('/student/all', methods=['GET'])
def get_students():
    return to_json_response(StudentManager.getStudents())


@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    return to_json_response(StudentManager.getStudent(student_id))

@app.route('/student/new', methods=['POST'])
def post_student():
    try:
        s = Student(
            request.form.get('student_id', default = None, type = int),
            request.form.get('student_name', default = None, type = str),
            request.form.get('advisor_id', default = None, type = int),
            request.form.get('approval_status', default = None, type = str),
            request.form.get('thesis_topic', default = None, type = str)
        )
        out = StudentManager.addStudent(s)
    except (AssertionError, KeyError, ValueError) as e:
        out = {"success":False,"desc": str(e)}
    return to_json_response(out)


@app.route('/student/<int:student_id>/approval/send/<int:advisor_id>', methods=['PATCH'])
def send_approval_request(student_id:int, advisor_id:int):
    try:
        out = StudentManager.sendApprovalRequest(student_id, advisor_id)
    except (AssertionError, KeyError, ValueError) as e:
        out = {"success":False,"desc": str(e)}
    return to_json_response(out)

@app.route('/student/<int:student_id>/approval/accepted', methods=['PATCH'])
def approval_accepted(student_id:int):
    return to_json_response(StudentManager.updateApprovalStatus(student_id, StudentManager.CONST_ACCEPTED))

@app.route('/student/<int:student_id>/approval/rejected', methods=['PATCH'])
def approval_rejected(student_id:int):
    return to_json_response(StudentManager.updateApprovalStatus(student_id, StudentManager.CONST_REJECTED))

@app.route('/student/<int:student_id>/thesis_topic/<string:thesis_topic>', methods=['PATCH'])
def update_thesis_topic(student_id:int,thesis_topic:str):
    return to_json_response(StudentManager.updateThesisTopic(student_id, thesis_topic))
    
app.run(host="0.0.0.0", port=5000, debug=True)