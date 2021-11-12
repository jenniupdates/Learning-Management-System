# Isaac Einstein Fong

class Question:
    def __init__(self, quiz_id, question_id, question_name, correct_ans):
        self.quiz_id = quiz_id
        self.question_id = question_id
        self.question_name = question_name
        self.correct_ans = correct_ans

    def getQuestionName(self):
        return self.question_name
    
    def getCorrectAnswer(self):
        return self.correct_ans

    def editQuestionName(self, new_question_name):
        self.question_name = new_question_name

    def editCorrectAnswer(self, correct_ans):
        self.correct_ans = correct_ans