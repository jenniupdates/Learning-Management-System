# Khoo Chee Kuang

from Database import DBHelper

class HR:
    def __init__(self, Name, UserName,Password):
        self.Name = Name
        self.UserName = UserName
        self.Password = Password


    def checkProgress(self): 
        db = DBHelper()
        retrive_section = "Select * from engineer_course_section;"
        section_retrival = db.fetch(retrive_section)



        count_of_section = len(section_retrival)

        total_section = 0 # total number of section in the course ID
        section_done = 0 # section completed
        number_of_loops = 0 # cto count the number of times it loop in engineer_course_section table

        course_percentage_keeper = [] # to keep track of the different course progress for the same user


        for i in range(1,count_of_section + 1): # this is to count the number of section and it start from 1 as course_id start from 1
            if number_of_loops == len(section_retrival): # this is use to store the unique course progress for the section . example [20,40] is refering to the percentage of course id 1(left) and course id 2(right)
                course_percentage = (section_done / total_section) * 100 # calculate percentage
                course_percentage_keeper.append(course_percentage)# apppend in ascending order, course 1 then course 2 then course 3
                section_done = 0
                total_section = 0
                number_of_loops = 0 # all the 0 is to restart
        
            for status in section_retrival:
                if status["User_ID"] == 1: # this will be the part that will take from the frontend.
                    if i == status["Course_ID"]:
                        if status["Section_Status"] == "complete":
                            section_done += 1 
                            total_section += 1
                            number_of_loops += 1
                    else:
                        total_section += 1
                        number_of_loops += 1
        
                else:
                    number_of_loops += 1    
     

        print(course_percentage_keeper)      

        
       
      
        
 




            
