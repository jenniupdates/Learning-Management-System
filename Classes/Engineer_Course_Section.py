from Database import DBHelper

class Engineer_Course_Section:
    def __init__(self,uid,cid,sid,class_id,status,quiz_id):
        self.user_id = uid
        self.course_id = cid
        self.section_id = sid
        self.class_id = class_id
        self.section_status = status # Unavailable , Available"
        self.quiz_id = quiz_id 
        self.db = DBHelper()

    def getUserID(self):
        return self.user_id
    
    def getCourseID(self):
        return self.course_id

    def getSectionID(self):
        return self.section_id
    
    def getClassID(self):
        return self.class_id
    
    def getSectionStatus(self):
        return self.section_status
    
    def getQuizID(self):
        return self.quiz_id

    def updateSectionStatus(self):
        if self.section_status == "Unavailable":
            self.section_status = "Available"
