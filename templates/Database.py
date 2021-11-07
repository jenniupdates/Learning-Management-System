import pymysql

class DBHelper:

    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.db = "g3t4"

    def __connect__(self):
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql, var = None):
        self.__connect__()
        if var is None:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, var)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result
    
    def fetchall(self, sql, var = None):
        self.__connect__()
        if var is None:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, var)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql, var = None):
        self.__connect__()
        if var is None:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, var)
        self.con.commit()
        self.__disconnect__()
        


db = DBHelper()

