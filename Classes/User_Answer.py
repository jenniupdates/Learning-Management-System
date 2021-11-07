from Database import DBHelper

class Quiz_User:
    def __init__(self,qid,uid,question_id,user_answer):
        self.quiz_id = qid
        self.user_id = uid
        self.question_id = question_id
        self.user_answer = user_answer
        self.db = DBHelper()

    def getAllQuizAnswersOfUser(self,user_id,quiz_id):
        # Returns the user's answers for that particular quiz in dictionary
        sql = "SELECT * FROM quiz_user WHERE User_ID = %s AND Quiz_ID = %s"
        val = (user_id,quiz_id)
        result = self.db.fetch(sql,val)
        quiz_dict = {}
        if len(result) < 1:
            return None
        else:
            for row in result:
                quiz_dict[row['Question_ID']] = row['User_Answer']

        return quiz_dict

    def calculateScore(self,user_id,quiz_id):
        # Returns score in %
        sql = "SELECT * FROM quiz_user WHERE User_ID = %s AND Quiz_ID = %s"
        val = (user_id,quiz_id)
        result = self.db.fetch(sql,val)
        num_questions = len(result)
        num_correct = 0
        for row in result:
            sql = "SELECT * FROM question WHERE Quiz_ID = %s AND Question_ID = %s"
            val = (row['Quiz_ID'],row['Question_ID'])
            result2 = self.db.fetch(sql,val)
            if result2[0]['Answer'] == row['User_Answer']:
                num_correct += 1

        return round(num_correct / num_questions * 100,2)

