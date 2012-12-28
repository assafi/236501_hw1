'''
Created on 2012-12-26

@author: Gal
'''
import unittest
from roadsTester import RoadsTester
from weightedAStar import WeightedAStar

MAX = 10
car1 = "Peugeot 508"
car2 = None
class Test(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testWeightedAStar(self):
        
        self.helper = RoadsTester(MAX,car1,car2,WeightedAStar(0.5))
        self.helper.performRun5()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testWeightedAStar']
    unittest.main()