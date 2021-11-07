class Quiz:
    def __init__(self, quiz_id, time_limit):
        self.quiz_id = quiz_id
        self.time_limit = time_limit


    def getTimeLimit(self):
        return self.time_limit
    

    def updateTimeLimit(self, time_limit, new_time_limit):
        if self.time_limit == time_limit:
            self.time_limit = new_time_limit



