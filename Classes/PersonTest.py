import unittest

from Person import Person

class Testperson(unittest.TestCase):
    def test_userType(self):
        hr = Person("John","Johnny","HR","testing")
        engineer = Person("Charlotte","JIJI","Engineer","testing1")
        trainer = Person("Macy","KIMKIM","Trainer","testing2")
        self.assertEqual(hr.getUserType(),1)
        self.assertEqual(engineer.getUserType(),2)
        self.assertEqual(trainer.getUserType(),3)
    
    def test_userName(self):
         hr = Person("John","Johnny","HR","testing")
         engineer = Person("Charlotte","JIJI","Engineer","testing1")
         trainer = Person("Macy","KIMKIM","Trainer","testing2")
         self.assertEqual(hr.getUserName(),"Johnny")
         self.assertEqual(engineer.getUserName(),"JIJI")
         self.assertEqual(trainer.getUserName(),"KIMKIM")
    
    def test_name(self):
        hr = Person("John","Johnny","HR","testing")
        engineer = Person("Charlotte","JIJI","Engineer","testing1")
        trainer = Person("Macy","KIMKIM","Trainer","testing2")
        self.assertEqual(hr.getName(),"John")
        self.assertEqual(engineer.getName(),"Charlotte")
        self.assertEqual(trainer.getName(),"Macy")
    



    






if __name__ == "__main__":
    unittest.main()

