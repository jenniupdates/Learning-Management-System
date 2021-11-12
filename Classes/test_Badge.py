# Stephen Pang Qing Yang

import unittest
from Badge import Badge

class testBadge(unittest.TestCase):
    def test_badge(self):
        b = Badge(3,2,"For those who have understood the Basics of Engineering")

        uid = b.getUserID()
        self.assertEqual(uid,3)

        cid = b.getCourseID()
        self.assertEqual(cid,2)

        b_info = b.getBadgeInfo()
        self.assertEqual(b_info,"For those who have understood the Basics of Engineering")

