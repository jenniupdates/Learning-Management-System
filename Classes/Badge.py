# Stephen Pang Qing Yang

class Badge:
    def __init__(self,uid,cid,binfo):
        self.user_id = uid
        self.course_id = cid
        self.badge_info = binfo

    def getUserID(self):
        return self.user_id

    def getCourseID(self):
        return self.course_id

    def getBadgeInfo(self):
        return self.badge_info
        