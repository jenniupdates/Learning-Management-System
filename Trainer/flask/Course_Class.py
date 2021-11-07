class Course_Class:
    def __init__(self, course_id, class_id, trainer_id, class_start, class_end, size_limit, reg_start, reg_end, final_quiz_id):
        self.__cid = course_id
        self.__clid = class_id
        self.__tid = trainer_id
        self.__classstart = class_start
        self.__classend = class_end
        self.__sizelimit = size_limit
        self.__regstart = reg_start
        self.__regend = reg_end
        self.__fqid = final_quiz_id
    
    # getter functions for course_class attributes
    
    def cid(self):
        return (self.__cid)
    
    def clid(self):
        return (self.__clid)
    
    def tid(self):
        return (self.__tid)

    def classstart(self):
        return (self.__classstart)

    def classend(self):
        return (self.__classend)
    
    def sizelimit(self):
        return (self.__sizelimit)
    
    def regstart(self):
        return (self.__regstart)
    
    def regend(self):
        return (self.__regend)

    def fqid(self):
        return (self.__fqid)