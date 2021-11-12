# Richard Goh Jiangwei

from Course import Course
from Database import DBHelper
from Course_Class import Course_Class
class CourseController:

    def __init__(self):
        self.db = DBHelper()
        
    def getCourse(self, cid):
        sql = "SELECT * FROM courses WHERE course_id = %s"
        result = self.db.fetch(sql, cid)
        result = result[0]
        params = [str(result[key]) for key in result]
        course = Course(*params)
        return course # returns a Course object 

    def getClass(self, cid, clid):
        sql = "SELECT * FROM course_class WHERE (course_id, class_id) = (%s,%s)"
        val = (cid, clid)
        result = self.db.fetch(sql, val)
        result = result[0]
        params = [str(result[key]) for key in result]
        course_class = Course_Class(*params)
        return course_class

    def getClassByTrainer(self, tid):
        sql = "SELECT * FROM course_class WHERE trainer_id = %s"
        val = (tid)
        result = self.db.fetch(sql, val)
        return result
    
    #

    # get prerequisites for a given Course object and returns a list of prerequisites' ID, return empty list if no prerequisites
    def getPrereqs(self, Course):
        cid = Course.cid()
        sql = "SELECT * FROM course_prereqs WHERE course_ID = %s"
        result = self.db.fetch(sql, cid)
        prereq_list = []
        if len(result) != 0:
            for dict in result:
                prereq_list.append(dict["Course_prereq_ID"])
        return prereq_list # returns a list of prerequisites' ID, if none return an empty list


    # update/delete prerequisites for a given Course object (Course 1), args are edit type (add, delete), and Course2 is prereq to be added/removed
    def editPrereqs(self, Course1, Course2, edit="add"):
        cid1 = Course1.cid()
        cid2 = Course2.cid()
        if edit == "add": # add a new prerequisite
            sql = "INSERT INTO course_prereqs (Course_ID, Course_prereq_ID) VALUES (%s,%s)"
            self.db.execute(sql, (cid1, cid2))
            return
        else: # delete an existing prerequisite
            sql = "DELETE FROM course_prereqs WHERE (Course_ID, Course_prereq_ID) = (%s,%s)"
            self.db.execute(sql, (cid1, cid2))
            return

    # create a new course, course_id is auto incremented, name and outline provided, and hrid obtained with GET from user page   
    def createCourse(self, cid, name, outline):
        sql = "INSERT INTO courses (Course_ID, Course_Name, Course_Outline) VALUES (%s,%s,%s)"
        val = (cid, name, outline)
        self.db.execute(sql, val)
        return
    
    # create a new class, class_ID is auto incremented based on number of classes for that course currently
    def createClass(self, Course, trainer_id, class_start, class_end, size_limit, reg_start, reg_end, final_quiz_id):
        numClasses = self.getNumClasses(Course)
        cid = Course.cid()
        sql = "INSERT INTO course_class (Course_ID, Class_ID, Trainer_ID, Class_Start, Class_End, Size_Limit, Reg_Start, Reg_End, Final_Quiz_ID)" + \
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (cid, numClasses + 1, trainer_id, class_start, class_end, size_limit, reg_start, reg_end, final_quiz_id)
        self.db.execute(sql, val)
        return 
    
    # edits information about a Course_Class
    def editClass(self, classcol, newvalue, Course_Class):
        cid = Course_Class.cid()
        clid = Course_Class.clid()
        sql = "UPDATE Course_Class SET " + classcol + " = %s WHERE (Course_ID, Class_ID) = (%s, %s)"
        val = (newvalue, cid, clid)
        self.db.execute(sql, val)
        return
    
    # returns number of Classes for a given Course
    def getNumClasses(self, Course):
        cid = Course.cid()
        sql = "SELECT count(*) as numClasses FROM course_class WHERE Course_ID = %s"
        result = self.db.fetch(sql, cid)
        return result[0]['numClasses']
    
    # assign a Learner to a Course_Class based on their ID
    def assignLearner(self, Course_Class, User_ID):
        (cid, clid) = (Course_Class.cid(), Course_Class.clid())
        sql = "INSERT INTO engineer_course_enrolment (Course_ID, Class_ID, User_ID, Course_Status)" + \
            "VALUES (%s, %s, %s, %s)"
        val = (cid, clid, User_ID, "enrolled")
        self.db.execute(sql, val)
        return
    
    # from HR, approve a learner given their User_ID and for a given Course_Class, updates engineer_course_enrolment
    def approveLearner(self, Course_Class, User_ID, approve_bool = True):
        (cid, clid) = (Course_Class.cid(), Course_Class.clid())
        if approve_bool == True:
            # if learner is approved for course, change course_status from registered to enrolled
            sql = "UPDATE engineer_course_enrolment SET Course_Status = 'enrolled'" + \
                "WHERE (Course_ID, Class_ID, User_ID) = (%s,%s,%s)"
        else:
            # if learner is not approved for course, remove row from engineer course_enrolment
            sql = "DELETE FROM engineer_course_enrolment WHERE (Course_ID, Class_ID, User_ID) = (%s,%s,%s)"
        val = (cid, clid, User_ID)
        self.db.execute(sql, val)
        return
    







