import unittest
from Quiz import Quiz

class TestQuiz(unittest.TestCase):
    def test_time_limit(self):
        q = Quiz(7,45)

        time_limit = q.getTimeLimit()
        self.assertEqual(time_limit,45)


    def test_update_time_limit(self):
        q = Quiz(7,45)

        q.updateTimeLimit(45,60)
        time_limit = q.getTimeLimit()
        self.assertEqual(time_limit, 60)

    
