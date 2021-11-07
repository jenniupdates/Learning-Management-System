class Course:
    
    def __init__(self, course_id, course_name, course_outline):
        self.__cid = course_id
        self.__name = course_name 
        self.__outline = course_outline
    # getter functions for course attributes

    def cid(self):
        return (self.__cid)
    
    def name(self):
        return (self.__name)
    
    def outline(self):
        return (self.__outline)
    
    # edit functions
    def edit_name(self, newname):
        self.__name = newname
    
    def edit_outline(self, newoutline):
        self.__outline = newoutline
    