import unittest
from Engineer_Course import Engineer_Course

class testEngineer_Course(unittest.TestCase):
    def test_engineerCourse(self):
        ec = Engineer_Course(2,5,3,'Enrolled',50)
        
        user_id = ec.getUserID()
        self.assertEqual(user_id,2)

        course_id = ec.getCourseID()
        self.assertEqual(course_id,5)

        class_id = ec.getClassID()
        self.assertEqual(class_id,3)

        courseStatus = ec.getCourseStatus()
        self.assertEqual(courseStatus,'Enrolled')

        ec.setCourseStatus()
        courseStatus = ec.getCourseStatus()
        self.assertEqual(courseStatus,"Completed")

        score = ec.getScore()
        self.assertEqual(score,50)

