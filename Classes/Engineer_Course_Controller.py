# Lim Yin Shan 

from Database import DBHelper
from Engineer_Course import Engineer_Course
from Engineer_Course_Section import Engineer_Course_Section
from Course_Eligibility import Course_Eligibility

class Engineer_Course_Controller:
    def __init__(self):
        self.db = DBHelper()

    def getEngineerCourseEnrolment(self,cid,class_id,user_id):
        sql = "SELECT * FROM engineer_course_enrolment WHERE Course_ID = %s AND Class_ID = %s AND User_ID = %s"
        val = (cid,class_id,user_id)
        result = self.db.fetch(sql,val)
        if len(result) < 1:
            return None
        engineer_course_enrolment = Engineer_Course(result[0]['User_ID'],result[0]['Course_ID'],result[0]['Class_ID'],result[0]['Course_Status'],result[0]['Score'])
        return engineer_course_enrolment

    def getEngineerCourseSection(self,cid,class_id,user_id,sect_id):
        sql = "SELECT * FROM engineer_course_section WHERE Course_ID = %s AND Class_ID = %s AND User_ID = %s AND Section_ID = %s"
        val = (cid,class_id,user_id,sect_id)
        result = self.db.fetch(sql,val)
        if len(result) < 0:
            return None
        engineer_course_section = Engineer_Course_Section(result[0]['User_ID'],result[0]['Course_ID'],result[0]['Section_ID'],result[0]['Class_ID'],result[0]['Section_Status'])
        return engineer_course_section

    def completeCourse(self,Engineer_Course):
        if Engineer_Course.getCourseStatus() == "Enrolled":
            Engineer_Course.setCourseStatus()
            sql = "UPDATE engineer_course_enrolment SET Course_Status = %s WHERE Course_ID = %s AND Class_ID = %s and User_ID = %s"
            val = (Engineer_Course.getCourseStatus(),Engineer_Course.getCourseID(),Engineer_Course.getClassID(),Engineer_Course.getUserID())
            self.db.execute(sql,val)
            self.db.con.commit()

    # new method to get the capacity for a class given its Course_ID
    def getClassCapacity(self, cid, clid):
        sql = "SELECT count(*) FROM engineer_course_enrolment WHERE course_id = %s AND class_id = %s AND course_status = 'enrolled'"
        val = (cid, clid)
        result = self.db.fetch(sql, val)
        return result[0]["count(*)"]
