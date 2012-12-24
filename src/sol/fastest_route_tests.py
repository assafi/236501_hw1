'''
Created on Dec 16, 2012

@author: Assaf
'''
import unittest
from src.osm_utils4 import CountryMap, DEFAULT_DB_FILE
import os
from src.sol.roadNet_State import RoadNet_State
from src.sol.roadNet_Action import RoadNet_Action
from src.sol.searchStatistics import SearchStatistics
class Test(unittest.TestCase):
    
    def setUp(self):
        self.map = CountryMap()
        self.map.LoadMap2("../../"+DEFAULT_DB_FILE)

    def tearDown(self):
        pass


#    def testCheckMapLoad(self):
#        assert(len(self.map.junctions) == 944800)
    
    def testRouteProblemState(self):
        
        def simpleCostActionFactory(aLink):
            return RoadNet_Action(2,aLink.target)
        
        start = RoadNet_State(0,self.map,simpleCostActionFactory, None)
        neighbors = start.getSuccessors()
        for k in neighbors.keys():
            assert(k.getCost() == 2)
            assert(neighbors[k].junction_key == 906119)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()