import unittest
from Course import Course

class testCourse(unittest.TestCase):
    def setUp(self):
        self.c = Course('1', "Intro to Programming", '3', "Outline")

    def testCourse(self):
        # test getter functions
        self.assertEquals(self.c.cid(), '1')
        self.assertEquals(self.c.name(), "Intro to Programming")
        self.assertEquals(self.c.outline(), "Outline")
        self.assertEquals(self.c.hrid(), '3')

        # test edit functions
        self.c.edit_name("Introduction to Python")
        self.assertEquals(self.c.name(), "Introduction to Python")
        self.c.edit_outline("New Outline")
        self.assertEquals(self.c.outline(), "New Outline")

        
    def tearDown(self):
        self.c = None

if __name__ == '__main__':
    unittest.main()