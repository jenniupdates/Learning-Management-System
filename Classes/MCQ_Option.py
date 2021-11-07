class MCQ_Option:
    def __init__(self, quiz_id, question_id, question_option):
        self.quiz_id = quiz_id
        self.question_id = question_id
        self.question_option = question_option

    def getQuestionOption(self):
        return self.question_option

    def editQuestionOption(self, new_question_option):
        self.question_option = new_question_option
