from Database import DBHelper


class Engineer_Course:
    def __init__(self,uid,cid,class_id,cstatus,score):
        self.user_id = uid
        self.course_id = cid
        self.class_id = class_id
        self.course_status = cstatus # Enrolled, Completed
        self.score = score # in terms of %
        self.db = DBHelper()

    def getUserID(self):
        return self.user_id
    
    def getCourseID(self):
        return self.course_id

    def getClassID(self):
        return self.class_id

    def getCourseStatus(self):
        return self.course_status

    def setCourseStatus(self):
        if self.course_status == "Enrolled":
            self.course_status = "Completed"
    
    def getScore(self):
        return self.score

    
