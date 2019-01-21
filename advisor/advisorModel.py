

class Advisor(object):
    def __init__(self,
            advisor_id:int,
            advisor_name:str, 
            field_of_interest:str = None,
            availability:bool = False):
        assert isinstance(advisor_id, int), "advisor_id must be int"
        assert isinstance(advisor_name, str), "advisor_name must be str"
        assert isinstance(field_of_interest, str) or field_of_interest is None, "field_of_interest must be str or None"
        assert availability==True or availability==False, "availability must be True or False"
        
        self.advisor_id = advisor_id
        self.advisor_name = advisor_name
        self.field_of_interest = field_of_interest
        self.availability = availability

    
    def __str__(self):
        return "#ID:{}, NAME:{}, FIELD_OF_INTEREST:{}, AVAILABILITY:{}".format(
                                                                                self.advisor_id,
                                                                                self.advisor_name,
                                                                                self.field_of_interest,
                                                                                self.availability)  
    def to_dict(self):
        return {"advisor_id":self.advisor_id,
                "advisor_name":self.advisor_name,
                "field_of_interest":self.field_of_interest,
                "availability":self.availability}