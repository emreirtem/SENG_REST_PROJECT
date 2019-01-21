import pandas as pd
from advisorModel import Advisor
import numpy as np
import requests
from requests.exceptions import ConnectionError

class RemoteStudentService(object):
    REMOTE_STUDENT_SERVICE_URI = "http://localhost:5000/student/"
    CONNECTION_ERROR = "RemoteStudentService cannot be reached."
    
    @staticmethod
    def checkStudentValidity(student_id:int)-> bool:
        uri = RemoteStudentService.REMOTE_STUDENT_SERVICE_URI+"{}/validate"
        try:
            r = requests.get(uri.format(student_id))
        except ConnectionError as e:
            raise AssertionError(RemoteStudentService.CONNECTION_ERROR)

        assert r.status_code==200, "RemoteStudentService Connection problem. Status Code %d"%r.status_code
        return r.json()["isStudentValid"]
    
    def notify_approval_status_update(student_id:int, status:str)-> bool:
        uri = RemoteStudentService.REMOTE_STUDENT_SERVICE_URI+"{}/approval/{}"
        try:
            r = requests.patch(uri.format(student_id, status.lower()))
        except ConnectionError as e:
            raise AssertionError(RemoteStudentService.CONNECTION_ERROR)

        assert r.status_code==200, "RemoteStudentService Connection problem. Status Code %d"%r.status_code
        return r.json()


    
class AdvisorManager(object):
    CONST_ACCEPTED = "ACCEPTED"
    CONST_WAIT_ACCEPT = "ACCEPT_WAITING"
    CONST_REJECTED = "REJECTED"
    
    DATA_ADVISOR_URI = "./data/advisors.csv"
    DATA_APPROVALS_URI = "./data/approvalsRequests.csv"
    data_advisors = pd.read_csv(DATA_ADVISOR_URI, dtype={"advisor_id":np.int64,
                                                         "advisor_name":np.object,
                                                         "field_of_interest":np.object,
                                                         "availability":np.bool}, )
    data_approvals = pd.read_csv(DATA_APPROVALS_URI, dtype={"advisor_id":np.int64,
                                                         "student_id":np.int64,
                                                         "status":np.object}, )
    
    @staticmethod
    def isAdvisorIdValid(advisor_id:int)-> dict:
        assert isinstance(advisor_id, int) and advisor_id is not None, "Advisor_id must be int"
        tmp = AdvisorManager.data_advisors.advisor_id==advisor_id
        if tmp.sum()>0:
            return {"isAdvisorValid":True}
        else:
            return {"isAdvisorValid":False}
    
    def isAdvisorAvailable(advisor_id:int)->dict:
        assert isinstance(advisor_id, int) and advisor_id is not None, "Advisor_id must be int"
        tmp = (AdvisorManager.data_advisors.advisor_id==advisor_id)
        if tmp.sum()>0:
            return {"isAdvisorValid":bool(AdvisorManager.data_advisors[tmp].iloc[0].availability)}
        else:
            return {"isAdvisorValid":False}
    
    
    @staticmethod
    def addAdvisor(advisor:Advisor) -> dict:
        assert isinstance(advisor, Advisor) and advisor is not None, "advisor object is invalid"
        assert len(AdvisorManager.data_advisors.query("advisor_id==@advisor.advisor_id"))==0, "Advisor Id exist"
        try:
            AdvisorManager.data_advisors = AdvisorManager.data_advisors.append(advisor.to_dict(), ignore_index=True)
            AdvisorManager.commit()
            out =  {"success":True,"desc":"Advisor added."}
        except (AssertionError, KeyError, ValueError) as e:
            out = {"success":False,"desc": str(e)}
        return out
    
    @staticmethod
    def updateAdvisorAvailability(advisor_id:int, availability:bool)-> dict:
        assert isinstance(advisor_id, int) and advisor_id is not None
        assert availability==True or availability==False, "availability must be True or False"
        tmp = AdvisorManager.data_advisors.advisor_id==advisor_id
        if tmp.sum()>0:
            AdvisorManager.data_advisors.loc[tmp,"availability"] = availability
            AdvisorManager.commit()
            return {"success":True,"desc":"availability updated."}
        return {"success":False, "desc":"No advisors found to be updated."}
        
    
    @staticmethod
    def getAdvisors()-> list:
        return [AdvisorManager.__to_advisor_obj__(advisor).to_dict() for index,advisor in AdvisorManager.data_advisors.iterrows()]

    
    @staticmethod
    def getAdvisor(advisor_id:int)-> dict:
        assert isinstance(advisor_id, int) and advisor_id is not None, "advisor_id must be int"
        tmp = AdvisorManager.data_advisors.advisor_id==advisor_id
        advisor = AdvisorManager.data_advisors.loc[tmp]
        if tmp.sum()==1:
            return AdvisorManager.__to_advisor_obj__(advisor.iloc[0]).to_dict()
        else:
            return {}
    
    @staticmethod
    def getApprovals(advisor_id:int)-> dict:
        assert isinstance(advisor_id, int) and advisor_id is not None, "advisor_id must be int"
        # here can get student info with remote call
        tmp = (AdvisorManager.data_approvals.advisor_id==advisor_id)&(AdvisorManager.data_approvals.status==AdvisorManager.CONST_ACCEPTED)
        approvals = AdvisorManager.data_approvals.loc[tmp]
        return [{"advisor_id":approval.advisor_id,
                 "student_id":approval.student_id,
                 "status":approval.status} for index, approval in approvals.iterrows()]

    
    @staticmethod
    def getApprovalRequests(advisor_id:int)-> dict:
        assert isinstance(advisor_id, int) and advisor_id is not None, "advisor_id must be int"
        # here can get student info with remote call
        tmp = (AdvisorManager.data_approvals.advisor_id==advisor_id)&(AdvisorManager.data_approvals.status==AdvisorManager.CONST_WAIT_ACCEPT)
        requests = AdvisorManager.data_approvals.loc[tmp]
        # here can get student info with remote call
        return [{"advisor_id":approval_request.advisor_id,
                 "student_id":approval_request.student_id,
                 "status":approval_request.status} for index, approval_request in requests.iterrows()]
        
    
    @staticmethod
    def addApproveRequest(advisor_id, student_id)->dict:
        assert isinstance(advisor_id, int), "advisor_id must be int"
        assert isinstance(student_id, int), "student_id must be int"
        assert AdvisorManager.isAdvisorIdValid(advisor_id)["isAdvisorValid"], "invalid advisor_id"
        assert RemoteStudentService.checkStudentValidity(student_id), "Student service states that the student_id is invalid"
        tmp = ((AdvisorManager.data_approvals.advisor_id==advisor_id) & 
               (AdvisorManager.data_approvals.student_id==student_id)
               )
        assert tmp.sum()<1, "This request already sended."
        
        tmp = ((AdvisorManager.data_advisors.advisor_id==advisor_id) & 
               (AdvisorManager.data_advisors.availability==True)
               )
        assert tmp.sum()>0, "Request rejected due to availability of the advisor"
        
        try:
            AdvisorManager.data_approvals = AdvisorManager.data_approvals.append({"advisor_id":advisor_id,
                                                                                  "student_id":student_id,
                                                                                  "status":AdvisorManager.CONST_WAIT_ACCEPT}, ignore_index=True)
            AdvisorManager.commit()
            out =  {"success":True,"desc":"approve request added."}
        except (AssertionError, KeyError, ValueError) as e:
            out = {"success":False,"desc": str(e)}
        return out
    
    @staticmethod
    def updateApproveStatus(advisor_id:int, student_id:int, status:str)->dict:
        assert isinstance(advisor_id, int), "advisor_id must be int"
        assert isinstance(student_id, int), "student_id must be int"
        assert isinstance(status, str), "status must be str"
        assert status==AdvisorManager.CONST_ACCEPTED or status== AdvisorManager.CONST_REJECTED, "invalid status."
        tmp = ((AdvisorManager.data_approvals.advisor_id==advisor_id) & 
               (AdvisorManager.data_approvals.student_id==student_id) & 
               ~(AdvisorManager.data_approvals.status==AdvisorManager.CONST_REJECTED)
               )
        if tmp.sum()>0:
            AdvisorManager.data_approvals.loc[tmp,"status"] = status
            out = RemoteStudentService.notify_approval_status_update(student_id, status)
            AdvisorManager.commit()
            return {"success":True,"desc":"approve request updated.", "RemoteStudentService": out}
        return {"success":False, "desc":"No approve request found to be updated."}
    
    def __to_advisor_obj__(row) -> Advisor: 
        advisor_id = int(row.advisor_id)
        if row.advisor_name is np.nan or row.advisor_name is None :
            advisor_name=None
        else:
            advisor_name = str(row.advisor_name)
        if row.field_of_interest is np.nan or row.field_of_interest is None:
            field_of_interest = None
        else:
            field_of_interest = str(row.field_of_interest)
        if row.availability is np.nan or row.availability is None:
            availability = None
        else:
            availability = bool(row.availability)
        return Advisor(advisor_id,advisor_name,field_of_interest,availability)
    
    
    
    @staticmethod
    def commit():
        AdvisorManager.data_advisors.to_csv(AdvisorManager.DATA_ADVISOR_URI, index=False)
        AdvisorManager.data_approvals.to_csv(AdvisorManager.DATA_APPROVALS_URI, index=False)
        
        
        
        
        
        
        
        
        
        