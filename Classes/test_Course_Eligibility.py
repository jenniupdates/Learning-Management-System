import unittest
from Course_Eligibility import Course_Eligibility

class testCourse_Eligibility(unittest.TestCase):
    def test_getters(self):
        ece = Course_Eligibility(2,5,'Ineligible')

        course_eli = ece.getCourseEligibility()
        self.assertEqual(course_eli,'Ineligible')

        ece_cid = ece.getCourseID()
        self.assertEqual(ece_cid,2)

        ece_uid = ece.getUserID()
        self.assertEqual(ece_uid,5)


        



