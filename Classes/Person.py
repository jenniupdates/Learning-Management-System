
class Person:
  def __init__(self, Name, UserID,UserType,Password):
    self.Name = Name
    self.UserID = UserID
    self.UserType = UserType # 1 - Engineer, 2 - Trainer, 3 - HR
    self.Password = Password
  
  def getUserType(self):
     if self.UserType == 1:
       return "Engineer"
      
     if self.UserType == 2:
       return "Trainer"
    
     if self.UserType == 3:
       return "HR"

  def getUserID(self):
     return self.UserID

  def getName(self):
     return self.Name
  
  def getPassword(self):
     return self.Password

