# To test if DB control works, Add the following rows into SQL
# INSERT INTO course_eligibility VALUES (1,1,'Ineligible')
# INSERT into quiz VALUES (5,60);
# INSERT into sections VALUES (3,1,1,'WAD Part 0',5,'Part 0 Course Materials');
# INSERT into engineer_course_section VALUES (3,1,3,1,'Available',5);
import unittest
from Engineer_Course import Engineer_Course
from Engineer_Course_Controller import Engineer_Course_Controller 

class testEngineerCourseController(unittest.TestCase):

    def setUp(self):
        self.ecc = Engineer_Course_Controller()
        # self.ec = Engineer_Course(1, "IS111", 1, "Enrolled", 70)

    # need to edit the test case data
    def test(self):
        engineer_course_enrolment = self.ecc.getEngineerCourseEnrolment("IS111",1,1)
        oldenrolment = engineer_course_enrolment.getCourseStatus()
        self.assertNotEqual(oldenrolment, None)
           
        engineer_course_section = self.ecc.getEngineerCourseSection("IS111",1,1,1)
        oldsection = engineer_course_section.getSectionStatus()
        self.assertNotEqual(oldsection, None)

        # current_section = self.ecc.getEngineerCourseSection("IS111",1,1,1)
        # new_section = self.ecc.getEngineerCourseSection("IS111",1,1,2)
        # new_section_current_status = new_section.getSectionStatus()
        # self.ecc.accessNextSection(current_section)
        # new_section_new_status = new_section.getSectionStatus()
        # self.assertNotEqual(new_section_current_status, new_section_new_status)

        # ****still need tdd for accessNextSection and completeCourse functions in Engineer_Course_Controller


if __name__ == '__main__':
    unittest.main()