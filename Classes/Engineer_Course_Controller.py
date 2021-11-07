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
        engineer_course_section = Engineer_Course_Section(result[0]['User_ID'],result[0]['Course_ID'],result[0]['Section_ID'],result[0]['Class_ID'],result[0]['Section_Status'],result[0]['Quiz_ID'])
        return engineer_course_section

    def getEngineerCourseEligibility(self,cid,uid):
        sql = "SELECT * FROM course_eligibility WHERE Course_ID = %s AND User_ID = %s"
        val = (cid,uid)
        result = self.db.fetch(sql,val)
        if len(result) < 0:
            return None
        course_eligibility = Course_Eligibility(result[0]['Course_ID'],result[0]['User_ID'],result[0]['Eligibility'])
        return course_eligibility

    def accessNextSection(self,current_Engineer_Course_Section):
        if (current_Engineer_Course_Section.getSectionStatus() == 'Available'):
            next_section_id = current_Engineer_Course_Section.getSectionID() + 1
            # First check if section with that ID exists
            sql = "SELECT * FROM sections WHERE Course_ID = %s AND Class_ID = %s AND Section_ID = %s"
            val = (current_Engineer_Course_Section.getCourseID(),current_Engineer_Course_Section.getClassID(),next_section_id)
            result = self.db.fetch(sql,val)
            if len(result) > 0:
                # Next section exists, now edit it as available
                sql = "UPDATE engineer_course_section SET Section_Status = 'Available' WHERE Course_ID = %s AND Class_ID = %s AND User_ID = %s AND Section_ID = %s"
                val = (current_Engineer_Course_Section.getCourseID(),current_Engineer_Course_Section.getClassID(),current_Engineer_Course_Section.getUserID(),next_section_id)
                self.db.execute(sql,val)
                self.db.con.commit()

    def completeCourse(self,Engineer_Course):
        if Engineer_Course.getCourseStatus() == "Enrolled":
            Engineer_Course.setCourseStatus()
            sql = "UPDATE engineer_course_enrolment SET Course_Status = %s WHERE Course_ID = %s AND Class_ID = %s and User_ID = %s"
            val = (Engineer_Course.getCourseStatus(),Engineer_Course.getCourseID(),Engineer_Course.getClassID(),Engineer_Course.getUserID())
            self.db.execute(sql,val)
            self.db.con.commit()

    def updateCourseEligibility(self,Engineer_Course_Eligibility):
        if Engineer_Course_Eligibility.getCourseEligibility() == "Ineligible":
            Engineer_Course_Eligibility.updateCourseEligibility()
            # edit in DB
            sql = "UPDATE course_eligibility SET Eligibility = %s WHERE Course_ID = %s AND User_ID = %s"
            val = (Engineer_Course_Eligibility.getCourseEligibility(),Engineer_Course_Eligibility.getCourseID(),Engineer_Course_Eligibility.getUserID())

            self.db.execute(sql,val)
            self.db.con.commit()
    
    # new method to get the capacity for a class given its Course_ID
    def getClassCapacity(self, cid, clid):
        sql = "SELECT count(*) FROM engineer_course_enrolment WHERE course_id = %s AND class_id = %s AND course_status = 'enrolled'"
        val = (cid, clid)
        result = self.db.fetch(sql, val)
        return result[0]["count(*)"]
