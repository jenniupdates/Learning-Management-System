# Stephen Pang Qing Yang

import unittest
from Engineer_Course_Section import Engineer_Course_Section

class testEngineer_Course_Section(unittest.TestCase):
    def test_getters2(self):
        ecs = Engineer_Course_Section(10,2,4,5,'unavailable')

        uid = ecs.getUserID()
        self.assertEqual(uid,10)

        cid = ecs.getCourseID()
        self.assertEqual(cid,2)

        sect_id = ecs.getSectionID()
        self.assertEqual(sect_id,4)
        
        class_id = ecs.getClassID()
        self.assertEqual(class_id,5)

        section_status = ecs.getSectionStatus()
        self.assertEqual(section_status,'unavailable')

        ecs.updateSectionStatus()
        section_status = ecs.getSectionStatus()
        self.assertEqual(section_status,'incomplete')

        # quiz_id = ecs.getQuizID()
        # self.assertEqual(quiz_id,5)