from Database import DBHelper
from Section import Section
class Section_Controller:
    def __init__(self):
        self.db = DBHelper()
        
    # creates a new section
    def addSection(self, cid, sid, desc, qid, material):
        # current script in DB:
        # INSERT INTO `g3t4`.`sections` (Course_ID, Class_ID, Section_ID, Description, Quiz_ID, Course_Material) VALUES ('1', '1', '1', 'Intro to Programming Part 2', '1', 'Part 2 Lecture Materials');
        ql = "INSERT INTO Sections (Course_ID, Class_ID, Section_ID, Description, Quiz_ID, Course_Material) VALUES (%s,%s,%s,%s,%s,%s)"
    
