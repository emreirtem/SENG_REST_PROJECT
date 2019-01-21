

class Student(object):
    def __init__(self,
            student_id:int,
            student_name:str, 
            advisor_id:int = None,
            approval_status:str = None, 
            thesis_topic:str = None):
        assert isinstance(student_id, int), "student_id must be int"
        assert isinstance(student_name, str), "student_name must be str"
        assert isinstance(advisor_id, int) or advisor_id is None, "advisor_id must be int or None"
        assert isinstance(approval_status, str) or approval_status is None, "approval_status must be str or None"
        assert isinstance(thesis_topic, str) or thesis_topic is None, "thesis_topic must be str or None"
        
        self.student_id = student_id
        self.student_name = student_name
        self.advisor_id = advisor_id
        self.approval_status = approval_status
        self.thesis_topic = thesis_topic
    
    def __str__(self):
        return "#ID:{}, NAME:{}, ADVISOR_ID:{}, APPROVAL_STATUS:{}, THESIS_TOPIC:{}".format(
                                                                                self.student_id,
                                                                                self.student_name,
                                                                                self.advisor_id,
                                                                                self.approval_status,
                                                                                self.thesis_topic)  
    def to_dict(self):
        return {"student_id":self.student_id,
                "student_name":self.student_name,
                "advisor_id":self.advisor_id,
                "approval_status":self.approval_status,
                "thesis_topic":self.thesis_topic}