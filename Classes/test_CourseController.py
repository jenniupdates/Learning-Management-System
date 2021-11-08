import unittest
from Course_Controller import CourseController
from Course import Course
from Course_Class import Course_Class

class testCourseController(unittest.TestCase):
    def setUp(self):
        self.ct = CourseController()
        self.co = Course('ES102', 'Intro to Engineering', 'The basics of engineering')
        self.co2 = Course('IS216', 'Web Development I', 'Web Development for Beginners')
        self.cc = Course_Class('ES102', '1', '2', '2021-09-29', '2021-10-20', '40', '2021-09-10', '2021-09-13', '1')

    def testgetCourse(self):   
        temp = self.ct.getCourse('ES102')
        self.assertEqual(self.co.name(), temp.name())
        self.assertEqual(self.co.outline(), temp.outline())
        self.assertEqual(self.co.cid(), temp.cid())
    
    def testgetClass(self):
        temp = self.ct.getClass('ES102', '1')
        self.assertEqual(self.cc.cid(), temp.cid())
        self.assertEqual(self.cc.clid(), temp.clid())
        self.assertEqual(self.cc.tid(), temp.tid())
        self.assertEqual(self.cc.classstart(), temp.classstart())
        self.assertEqual(self.cc.classend(), temp.classend())
        self.assertEqual(self.cc.sizelimit(), temp.sizelimit())
        self.assertEqual(self.cc.regstart(), temp.regstart())
        self.assertEqual(self.cc.regend(), temp.regend())
        self.assertEqual(self.cc.fqid(), temp.fqid())
    
    def testgetPrereqs(self):
        self.assertEqual(self.ct.getPrereqs(self.co2), ['ES102','IS111'])
    
    def testeditPrereqs(self):
        self.ct.editPrereqs(self.co2, self.co, "delete")
        self.assertEqual(self.ct.getPrereqs(self.co2), ['IS111'])
        self.ct.editPrereqs(self.co2, self.co)
        self.assertEqual(self.ct.getPrereqs(self.co2), ['ES102','IS111'])

    def testgetNumClasses(self):
        num = self.ct.getNumClasses(self.co)
        self.assertEqual(num, 2)

    def tearDown(self):
        self.ct = None

if __name__ == '__main__':
    unittest.main()