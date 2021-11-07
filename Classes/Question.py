class Question:
    def __init__(self, quiz_id, question_id, question_name, solution):
        self.quiz_id = quiz_id
        self.question_id = question_id
        self.question_name = question_name
        self.solution = solution

    def getQuestionName(self):
        return self.question_name
    
    def getQuestionSolution(self):
        return self.solution

    def editQuestionName(self, new_question_name):
        self.question_name = new_question_name

    def editQuestionSolution(self, new_solution):
        self.solution = new_solution