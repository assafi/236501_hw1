'''
Created on Dec 16, 2012

@author: Assaf
'''
import unittest
from src.osm_utils4 import CountryMap, DEFAULT_DB_FILE
import os
from src.sol.route_problem import RouteProblemState
from src.sol.roadNet_Action import RoadNet_Action
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
        
        start = RouteProblemState(0,self.map,simpleCostActionFactory)
        neighbors = start.getSuccessors()
        for k in neighbors.keys():
            assert(k.getCost() == 2)
            assert(neighbors[k].junction_key == 906119)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()