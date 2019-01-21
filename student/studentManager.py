import pandas as pd
from studentModel import Student
import numpy as np
import requests
from requests.exceptions import ConnectionError

class RemoteAdvisorService(object):
    REMOTE_ADVISOR_SERVICE_URI = "http://localhost:5001/advisor/"
    CONNECTION_ERROR = "RemoteAdvisorService cannot be reached."
    
    @staticmethod
    def checkAdvisorValidity(advisor_id:int)-> bool:
        uri = RemoteAdvisorService.REMOTE_ADVISOR_SERVICE_URI+"{}/validate"
        try:
            r = requests.get(uri.format(advisor_id))
        except ConnectionError as e:
            raise AssertionError(RemoteAdvisorService.CONNECTION_ERROR)
        assert r.status_code==200, "status code %d"%r.status_code
        return r.json()["isAdvisorValid"]
    
    @staticmethod
    def checkAdvisorAvailability(advisor_id:int)->bool:
        uri = RemoteAdvisorService.REMOTE_ADVISOR_SERVICE_URI+"{}/is_available"
        try:
            r = requests.get(uri.format(advisor_id))
        except ConnectionError as e:
            raise AssertionError(RemoteAdvisorService.CONNECTION_ERROR)
        assert r.status_code==200, "status code %d"%r.status_code
        return r.json()["isAdvisorValid"]
    
    @staticmethod
    def sendApprovalRequest(advisor_id:int, student_id:int)-> dict:
        uri = RemoteAdvisorService.REMOTE_ADVISOR_SERVICE_URI+"{}/approval/request/{}"
        try:
            r = requests.post(uri.format(advisor_id, student_id))
        except ConnectionError as e:
            raise AssertionError(RemoteAdvisorService.CONNECTION_ERROR)
        assert r.status_code==200, "status code %d"%r.status_code
        return r.json()
    

class StudentManager(object):
    CONST_ACCEPTED = "ACCEPTED"
    CONST_WAIT_ACCEPT = "ACCEPT_WAITING"
    CONST_REJECTED = "REJECTED"
    
    DATA_URI = "./data/students.csv"
    data_students = pd.read_csv(DATA_URI, dtype={"student_id":np.int64,
                                                 "student_name":np.object,
                                                 "advisor_id":np.object,
                                                 "approval_status":np.object,
                                                 "thesis_topic":np.object}, )
    @staticmethod
    def isStudentIdValid(student_id:int)-> dict:
        assert isinstance(student_id, int) and student_id is not None, "Student adress must be int"
        tmp = StudentManager.data_students.student_id==student_id
        if tmp.sum()>0:
            return {"isStudentValid":True}
        else:
            return {"isStudentValid":False}
    
    @staticmethod
    def addStudent(student:Student) -> dict:
        assert isinstance(student, Student) and student is not None, "student object is invalid"
        assert len(StudentManager.data_students.query("student_id==@student.student_id"))==0, "Student Id exist"
        try:
            StudentManager.data_students = StudentManager.data_students.append(student.to_dict(), ignore_index=True)
            StudentManager.commit()
            out =  {"success":True,"desc":"Student added."}
        except (AssertionError, KeyError, ValueError) as e:
            out = {"success":False,"desc": str(e)}
        return out
        
    @staticmethod
    def updateApprovalStatus(student_id:int, approval_status:str) -> dict:
        assert isinstance(student_id, int) and student_id is not None, "student id must be int"
        assert approval_status is None or isinstance(approval_status, str) , "approval"
        tmp = StudentManager.data_students.student_id==student_id
        if tmp.sum()>0:
            StudentManager.data_students.loc[tmp,"approval_status"] = approval_status
            StudentManager.commit()
            return {"success":True,"desc":"aproval status updated."}
        return {"success":False, "desc":"No student found to be updated."}
    
    @staticmethod
    def sendApprovalRequest(student_id:int, advisor_id:int):
        assert RemoteAdvisorService.checkAdvisorValidity(advisor_id), "Remote Advisor services states that the advisor_id is invalid"
        assert RemoteAdvisorService.checkAdvisorAvailability(advisor_id), "Remote Advisor services states that the advisor is unavailable."
        r = RemoteAdvisorService.sendApprovalRequest(advisor_id, student_id)
        if r["success"]:
            StudentManager.updateAdvisorId(student_id, advisor_id)
            return StudentManager.updateApprovalStatus(student_id, StudentManager.CONST_WAIT_ACCEPT)
        else:
            return {"success":False, "desc":"RemoteAdvisorService replied sendRequest as False", "remoteAdvisorService":r}
        
    
    @staticmethod
    def updateAdvisorId(student_id:int, advisor_id:int) -> dict:
        assert isinstance(student_id, int) and student_id is not None, "Student id must be integer type"
        assert isinstance(advisor_id, int) or advisor_id is None, "advisor id must be integer type"
        assert advisor_id is None or RemoteAdvisorService.checkAdvisorValidity(advisor_id), "Remote Advisor services states that the advisor_id is invalid"
        tmp = StudentManager.data_students.student_id==student_id
        if tmp.sum()>0:
            StudentManager.data_students.loc[tmp,"advisor_id"] = advisor_id
            StudentManager.commit()
            return {"success":True,"desc":"advisor updated."}
        return {"success":False, "desc":"No student found to be updated."}
    
    @staticmethod
    def updateThesisTopic(student_id:int, thesis_topic:int) -> dict:
        assert isinstance(student_id, int) and student_id is not None, "Student_id must be int"
        assert isinstance(thesis_topic, str) or thesis_topic is None, "thesis topic must be str"
        tmp = StudentManager.data_students.student_id==student_id
        if tmp.sum()>0:
            if StudentManager.data_students.loc[tmp,"approval_status"].iloc[0] == StudentManager.CONST_ACCEPTED:
                StudentManager.data_students.loc[tmp,"thesis_topic"] = thesis_topic
                StudentManager.commit()
                return {"success":True,"desc":"Thesis topic updated."}
            else:
                return {"success":False,"desc":"You must choose your advisor first"}
            
        return {"success":False, "desc":"No student found to be updated."}
    
    @staticmethod
    def getStudent(student_id:int)-> dict:
        assert isinstance(student_id,int)
        tmp = StudentManager.data_students.student_id==student_id
        student = StudentManager.data_students.loc[tmp]
        if tmp.sum()==1:
            return StudentManager.__to_student_obj__(student.iloc[0]).to_dict()
        else:
            return {}
    
    @staticmethod
    def getStudents()-> list:
        return [StudentManager.__to_student_obj__(student).to_dict() for index,student in StudentManager.data_students.iterrows()]

    def __to_student_obj__(row) -> Student: 
        student_id = int(row.student_id)
        if row.student_name is np.nan or row.student_name is None :
            student_name=None
        else:
            student_name = str(row.student_name)
        
        if row.advisor_id is np.nan or row.advisor_id is None:
            advisor_id = None
        else:
            advisor_id = int(row.advisor_id)
            
        if row.approval_status is np.nan or row.approval_status is None:
            approval_status = None
        else:
            approval_status = str(row.approval_status)
            
        if row.thesis_topic is np.nan or row.thesis_topic is None:
            thesis_topic = None
        else:
            thesis_topic=str(row.thesis_topic)
        
        return Student(student_id,student_name,advisor_id,approval_status,thesis_topic)
    
    
    @staticmethod
    def commit():
        StudentManager.data_students.to_csv(StudentManager.DATA_URI, index=False)
        
        
        
        
        
        
        
        
        
        