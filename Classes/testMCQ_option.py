import unittest
from MCQ_Option import MCQ_Option

class TestMCQOption(unittest.TestCase):
    def test_MCQ_Option(self):
        q = MCQ_Option(7,4,1)

        question_option = q.getQuestionOption()
        self.assertEqual(question_option, 1)

    def test_edit_MCQ_Option(self):
        q = MCQ_Option(7,4,1)

        q.editQuestionOption(2)
        question_option = q.getQuestionOption()
        self.assertEqual(question_option, 2)



# if __name__ == "__main__":
#     unittest.main()