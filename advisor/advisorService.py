from flask import Flask
from flask import request, Response
import pandas as pd
from advisorManager import AdvisorManager
from advisorModel import Advisor
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


@app.route('/advisor/<int:advisor_id>/validate', methods=['GET'])
def is_advisor_valid(advisor_id:int):
    try:
        out = AdvisorManager.isAdvisorIdValid(advisor_id)
    except (AssertionError, KeyError, ValueError) as e:
        out = {"success":False,"desc": str(e)}
    return to_json_response(out)


@app.route('/advisor/<int:advisor_id>/is_available', methods=['GET'])
def is_advisor_available(advisor_id:int):
    try:
        out = AdvisorManager.isAdvisorAvailable(advisor_id)
    except (AssertionError, KeyError, ValueError) as e:
        out = {"success":False,"desc": str(e)}
    return to_json_response(out)
    


@app.route('/advisor/all', methods=['GET'])
def get_advisors():
    return to_json_response(AdvisorManager.getAdvisors())

@app.route('/advisor/<int:advisor_id>', methods=['GET'])
def get_advisor(advisor_id:int):
    return to_json_response(AdvisorManager.getAdvisor(advisor_id))



@app.route('/advisor/new', methods=['POST'])
def post_advisor():
    try:
        availability = str(request.form.get('availability', default = None, type = str)).upper()=='TRUE'
        s = Advisor(
            request.form.get('advisor_id', default = None, type = int),
            request.form.get('advisor_name', default = None, type = str),
            request.form.get('field_of_interest', default = None, type = str),
            availability
        )
        out = AdvisorManager.addAdvisor(s)
        
    except (AssertionError, KeyError, ValueError) as e:
        out = {"success":False,"desc": str(e)}
    return to_json_response(out)


@app.route('/advisor/<int:advisor_id>/update_availability/<string:value>', methods=['PATCH'])
def update_availability(advisor_id:int, value:bool):
    try:
        if value.upper()=='FALSE':
            out = AdvisorManager.updateAdvisorAvailability(advisor_id, False)
        else:
            out = AdvisorManager.updateAdvisorAvailability(advisor_id, True)
    except (AssertionError, KeyError, ValueError) as e:
        out = {"success":False,"desc": str(e)}
    return to_json_response(out)


@app.route('/advisor/<int:advisor_id>/approval/request/<int:student_id>', methods=['POST'])
def approval_request(advisor_id:int, student_id:int):
    #check student_id validity
    try:
        out = AdvisorManager.addApproveRequest(advisor_id, student_id)
    except (AssertionError, KeyError, ValueError, ConnectionError) as e:
        out = {"success":False,"desc": str(e)}
    return to_json_response(out)

@app.route('/advisor/<int:advisor_id>/approval/request/<int:student_id>/<string:action>', methods=['PATCH'])
def reply_approval_request(advisor_id:int, student_id:int, action:str):
    try:
        if action=="accept":
            out = AdvisorManager.updateApproveStatus(advisor_id, student_id, AdvisorManager.CONST_ACCEPTED)
        elif action=="reject":
            out = AdvisorManager.updateApproveStatus(advisor_id, student_id, AdvisorManager.CONST_REJECTED)
        else:
            out = {"success":False,"desc": "invalid action"}
    except (AssertionError, KeyError, ValueError) as e:
        out = {"success":False,"desc": str(e)}
    return to_json_response(out)

@app.route('/advisor/<int:advisor_id>/approval/all', methods=['GET'])
def get_approvals(advisor_id:int):
    try:
        out = AdvisorManager.getApprovals(advisor_id)
    except (AssertionError, KeyError, ValueError) as e:
        out = {"success":False,"desc": str(e)}
    return to_json_response(out)

@app.route('/advisor/<int:advisor_id>/approval/requests', methods=['GET'])
def get_approval_requests(advisor_id:int):
    try:
        out = AdvisorManager.getApprovalRequests(advisor_id)
    except (AssertionError, KeyError, ValueError) as e:
        out = {"success":False,"desc": str(e)}
    return to_json_response(out)
    

app.run(host="0.0.0.0", port=5001, debug=True)