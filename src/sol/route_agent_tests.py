'''
Created on Dec 17, 2012

@author: Assaf
'''
import unittest
from src.search.astar import AStar
from roadsTester import RoadsTester

MAX = 100
car1= "Peugeot 508"
car2= "Ford Focus"

class Test(unittest.TestCase):


    def setUp(self):
        self.helper = RoadsTester(MAX,car1,car2,AStar())

    def tearDown(self):
        pass
        
    def testRunAll(self):
        self.helper.performRun4()
        
if __name__ == "__main__":
#    import sys;sys.argv = ['Test.testFuelSavingRoute']
    unittest.main()