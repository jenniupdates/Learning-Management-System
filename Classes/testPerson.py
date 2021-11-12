# Khoo Chee Kuang

import unittest

from Person import Person

class Testperson(unittest.TestCase):
    def test_userType(self):
        hr = Person("John","Johnny",3,"testing")
        engineer = Person("Charlotte","JIJI",1,"testing1")
        trainer = Person("Macy","KIMKIM",2,"testing2")
        self.assertEqual(hr.getUserType(),"HR")
        self.assertEqual(engineer.getUserType(),"Engineer")
        self.assertEqual(trainer.getUserType(),"Trainer")
    
    def test_name(self):
        hr = Person("John","Johnny","HR","testing")
        engineer = Person("Charlotte","JIJI","Engineer","testing1")
        trainer = Person("Macy","KIMKIM","Trainer","testing2")
        self.assertEqual(hr.getName(),"John")
        self.assertEqual(engineer.getName(),"Charlotte")
        self.assertEqual(trainer.getName(),"Macy")
    



    






if __name__ == "__main__":
    unittest.main()

