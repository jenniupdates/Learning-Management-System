# Isaac Einstein Fong

import unittest
from Question import Question

class TestQuestion(unittest.TestCase):
    def test_Question(self):
        q = Question(7,4,"Define Engineering","Engineering is art")

        question_name = q.getQuestionName()
        self.assertEqual(question_name, "Define Engineering")

        answer = q.getCorrectAnswer()
        self.assertEqual(answer, "Engineering is art")


    def test_edit_Question(self):
        q = Question(7,4,"Define Engineering","Engineering is art")
        
        q.editQuestionName("What is math?")
        question_name = q.getQuestionName()
        self.assertEqual(question_name, "What is math?")

        q.editCorrectAnswer("Math is numbers")
        answer = q.getCorrectAnswer()
        self.assertEqual(answer, "Math is numbers")


