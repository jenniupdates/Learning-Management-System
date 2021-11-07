import unittest
from Course_Class import Course_Class

class testCourse_Class(unittest.TestCase):
    def setUp(self):
        self.cc = Course_Class('1', '1', '2', '2021-09-29', '2021-10-20', '40', '2021-09-10', '2021-09-13', '1')
    
    def testCourse_Class(self):
        # test getter functions
        self.assertEqual(self.cc.cid(),'1')
        self.assertEqual(self.cc.clid(),'1')
        self.assertEqual(self.cc.tid(),'2')
        self.assertEqual(self.cc.classstart(),'2021-09-29')
        self.assertEqual(self.cc.classend(),'2021-10-20')
        self.assertEqual(self.cc.sizelimit(),'40')
        self.assertEqual(self.cc.regstart(),'2021-09-10')
        self.assertEqual(self.cc.regend(),'2021-09-13')
        self.assertEqual(self.cc.fqid(),'1')
    
    def tearDown(self):
        self.cc = None

if __name__ == '__main__':
    unittest.main()