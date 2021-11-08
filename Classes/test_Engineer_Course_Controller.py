# To test if DB control works, Add the following rows into SQL
# INSERT INTO course_eligibility VALUES (1,1,'Ineligible')
# INSERT into quiz VALUES (5,60);
# INSERT into sections VALUES (3,1,1,'WAD Part 0',5,'Part 0 Course Materials');
# INSERT into engineer_course_section VALUES (3,1,3,1,'Available',5);
import unittest
from Engineer_Course_Controller import Engineer_Course_Controller 

class testEngineerCourseController(unittest.TestCase):

    def setUp(self):
        self.ecc = Engineer_Course_Controller()

    def test(self):
        # Getting Enrolment, Section and Eligibility for a partiuclar engineer and course
        engineer_course_enrolment = self.ecc.getEngineerCourseEnrolment(1,1,1)
        # print("Old Enrolment: ", engineer_course_enrolment.getCourseStatus())
        oldenrolment = engineer_course_enrolment.getCourseStatus()
        self.assertNotEqual(oldenrolment, None)
           
        engineer_course_section = self.ecc.getEngineerCourseSection(3,1,3,2)
        oldsection = engineer_course_section.getSectionStatus()
        self.assertNotEqual(oldsection, None)

        # Update Course eligibility to complete
        engineer_course_eligibility = self.ecc.getEngineerCourseEligibility(1,1)
        old_eligibility = engineer_course_eligibility.getCourseEligibility()
        self.assertNotEqual(old_eligibility, None)
        
        self.ecc.updateCourseEligibility(engineer_course_eligibility)

        new_engineer_course_eligibility = self.ecc.getEngineerCourseEligibility(1,1)
        new_eligibility = new_engineer_course_eligibility.getCourseEligibility()

        self.ecc.completeCourse(engineer_course_enrolment)

        new_engineer_course_enrolment = self.ecc.getEngineerCourseEnrolment(1,1,1)
        newenrolment = new_engineer_course_enrolment.getCourseStatus()

        self.assertNotEqual(oldenrolment, newenrolment)

        prev_section = self.ecc.getEngineerCourseSection(3,1,3,1)
        self.ecc.accessNextSection(prev_section)
        new_section = self.ecc.getEngineerCourseSection(3,1,3,2)
        newsection = new_section.getSectionStatus()

        self.assertNotEqual(oldsection, newsection)


if __name__ == '__main__':
    unittest.main()