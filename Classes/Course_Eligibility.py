# Lim Yin Shan

class Course_Eligibility:
    def __init__(self,cid,uid,eligi):
        self.course_id = cid
        self.user_id = uid
        self.eligibility = eligi # eligible or ineligible
        
    def getCourseID(self):
        return self.course_id
    
    def getUserID(self):
        return self.user_id
    
    def getCourseEligibility(self):
        return self.eligibility

    def updateCourseEligibility(self):
        if self.eligibility == "ineligible":
            self.eligibility = "eligible"