'''
Created on Dec 26, 2012

@author: Assaf
'''
import unittest
from src.sol.roadNet_State import RoadNet_State
from src.sol.actionFactories import ShortestActionFactory
from src.sol.problemAgents import ShortestRouteAgent
from src.sol.UpdatableAStarComplex import AStarWithUpdatesComplex
from src.osm_utils4 import CountryMap, DEFAULT_DB_FILE
from src.sol.UpdatableAStarBaseline import AStarWithUpdatesBaseline
import time

class Test(unittest.TestCase):

    def setUp(self):   
        self.map = CountryMap()
        self.map.LoadMap2("../../"+DEFAULT_DB_FILE)
        self.problem = self.map.GenerateProblem()
    
    def testComplexUpdatableAStar(self):
        for i in xrange(1,2):
#            problem_state = RoadNet_State(self.problem[0],self.map,\
#                                              ShortestActionFactory(),self.problem[1],None)
            problem_state = RoadNet_State(918327,self.map,\
                                              ShortestActionFactory(),572887,None)
            start = time.clock()
            agent = ShortestRouteAgent(AStarWithUpdatesComplex())
            agent.solve(problem_state)
            elapsed = time.clock() - start
            print "Complex took: "+str(elapsed)
            start = time.clock()
            agent = ShortestRouteAgent(AStarWithUpdatesBaseline())
            agent.solve(problem_state)
            elapsed = time.clock() - start
            print "Baseline took: "+str(elapsed)

#    def testBaselineUpdatableAStar(self):
#        for i in xrange(1,2):
#            problem_state = RoadNet_State(self.problem[0],self.map,\
#                                              ShortestActionFactory(),self.problem[1],None)
#            agent = ShortestRouteAgent(AStarWithUpdatesBaseline())
#            agent.solve(problem_state)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testUpdatableAStar']
    unittest.main()