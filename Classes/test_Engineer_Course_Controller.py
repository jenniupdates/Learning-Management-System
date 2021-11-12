# Lim Yin Shan

import unittest
from Engineer_Course import Engineer_Course
from Engineer_Course_Controller import Engineer_Course_Controller 

class testEngineerCourseController(unittest.TestCase):

    def setUp(self):
        self.ecc = Engineer_Course_Controller()
        # self.ec = Engineer_Course(1, "IS111", 1, "Enrolled", 70)

    # need to edit the test case data
    def test(self):
        engineer_course_enrolment = self.ecc.getEngineerCourseEnrolment("IS217",1,1)
        oldenrolment = engineer_course_enrolment.getCourseStatus()
        self.assertNotEqual(oldenrolment, None)
           
        engineer_course_section = self.ecc.getEngineerCourseSection("IS111",1,1,2)
        oldsection = engineer_course_section.getSectionStatus()
        self.assertNotEqual(oldsection, None)



if __name__ == '__main__':
    unittest.main()