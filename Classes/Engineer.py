# Khoo Chee Kuang

from Database import DBHelper


class Engineer:
    def __init__(self, Name, UserName,UserType,Password):
        self.Name = Name
        self.UserName = UserName
        self.UserType = UserType
        self.Password = Password



    def viewCourse(self): # this is to view all the items inside course db
       
        db = DBHelper()
        retrive_courses = "Select * from courses;"
        course_retrival = db.fetch(retrive_courses)
        for course in course_retrival:
            print(course)
        

    def enrolCourseClass(self):
        db = DBHelper()
        
        retrive_course_status= "Select * from engineer_course_enrolment;" # this is to check the course status of the user/engineer
        retrive_course_eligibility= "Select * from course_eligibility ;"# this is to check if the 
        eligibilty_status = db.fetch(retrive_course_status)
        user_eligibilty = db.fetch(retrive_course_eligibility)

        not_enrol = [] # this is a empty list to keep a list of not enrol courses.
        
        for status in eligibilty_status:
            if status["Course_Status"] == "not enrolled":
                not_enrol.append(status["Course_ID"]) # this is to append the course id
            #print(not_enrol)
        #---this part is to gather all the course id that is not enrol. the purpose is to gather all the course id -----------------------------------

        for eligibilty in user_eligibilty:
            for test in not_enrol:
                if test == eligibilty["Course_ID"]:
                    if eligibilty["Eligibility"] == "Yes":
                        print("hello")# it will change again once we got the frontend ready
  
       #the for loop is to check the course id that is not enrol. then check the eligibilty. the reason for this is for future frontend
        #when we not allowing the user to click the button or isit i get my rationale wrong LOL



    def viewSections(self):# this is to view all the items in sections db
        #database connection
        db = DBHelper()
        
        retrive_sections = "Select * from sections;"
        section_retrival = db.fetch(retrive_sections)

        for section in section_retrival:
            print(section)
  
    
    def takeQuiz(self):# this is to check if the user has completed the section. if completed, the user is allowed to take vice versa.
    
        db = DBHelper()

        check_section_status ="Select * from engineer_course_section"
        status_retrival = db.fetch(check_section_status)

        for status in status_retrival:
            if status["Section_Status"] == "complete":
                print("can take quiz")
            else:
                print("cannot take")
        
        

    
    def viewBadge(self):# this is to retreive all the items in badge.
        #database connection
        db = DBHelper()
        
        retrive_badge = "Select * from badgedb;"
        badge_retrival = db.fetch(retrive_badge)

        for badge in badge_retrival:
            print(badge)
  
       













