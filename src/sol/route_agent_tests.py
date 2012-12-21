'''
Created on Dec 17, 2012

@author: Assaf
'''
from src.osm_utils4 import CountryMap, DEFAULT_DB_FILE
from src.problem import ProblemAction
from src.problem_agent import ShortestRouteAgent, FastestRouteAgent, \
    FuelSavingRouteAgent, HybridRouteAgent
from src.sol.actionFactories import ShortestActionFactory, FastestActionFactory, \
    FuelSavingActionFactory, HybridActionFactory
from src.sol.route_problem import RouteProblemState
import unittest

class Test(unittest.TestCase):


    def setUp(self):
        self.map = CountryMap()
        self.map.LoadMap2("../../"+DEFAULT_DB_FILE)
        self.problem = self.map.GenerateProblem()

    def tearDown(self):
        pass


    def testShortestRoute(self):        
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          ShortestActionFactory(),self.problem[1])
        agent = ShortestRouteAgent()
        answer = agent.solve(problem_state)
        for n in answer:
            print(n)
            
    def testFastestRoute(self):
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          FastestActionFactory(),self.problem[1])
        agent = FastestRouteAgent()
        answer = agent.solve(problem_state)
        for n in answer:
            print(n)
            
    def testFuelSavingRoute(self):
        problem_state = RouteProblemState(0,self.map,\
                                          FuelSavingActionFactory(self.map),\
                                          40)
        agent = FuelSavingRouteAgent()
        answer = agent.solve(problem_state)
        for n in answer:
            print(n)
            
    def testHybrid(self):
        alpha = 0.3
        beta = 0.3
        
        problem_state = RouteProblemState(self.problem[0],self.map,\
            HybridActionFactory(alpha,beta,ShortestActionFactory(),\
                                FastestActionFactory(),FuelSavingActionFactory(self.map))\
                                          ,self.problem[1])
        
        agent = HybridRouteAgent(alpha,beta)
        answer = agent.solve(problem_state)
        for n in answer:
            print(n)
        
            
        
if __name__ == "__main__":
#    import sys;sys.argv = ['Test.testFuelSavingRoute']
    unittest.main()