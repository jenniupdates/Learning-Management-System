# Lim Yin Shan

class Section:
    # Course_ID, Class_ID, Section_ID, Description, Quiz_ID, Course_Material
    def __init(self, course_id, class_id, section_id, description, quiz_id):
        self.__cid = course_id
        self.__clid = class_id
        self.__sid = section_id
        self.__desc = description
        self.__qid = quiz_id
    
    # getter functions for course_class attributes
    
    def getCourseID(self):
        return (self.__cid)

    def getClassID(self):
        return (self.__clid)
    
    def getSectionID(self):
        return (self.__sid)
    
    def getSectionDescription(self):
        return (self.__desc)

    def getQuizID(self):
        return (self.__qid)
