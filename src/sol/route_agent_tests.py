'''
Created on Dec 17, 2012

@author: Assaf
'''
import unittest
from src.osm_utils4 import CountryMap, DEFAULT_DB_FILE
from src.sol.route_problem import RouteProblemState
from src.problem import ProblemAction
from src.problem_agent import ShortestRouteAgent, FastestRouteAgent,\
    FuelSavingRouteAgent, HybridRouteAgent
from src.sol.costs import shortestRouteCost, fastestRouteCost,\
    fuelSavingRouteCost

class Test(unittest.TestCase):


    def setUp(self):
        self.map = CountryMap()
        self.map.LoadMap2("../../"+DEFAULT_DB_FILE)
        self.problem = self.map.GenerateProblem()

    def tearDown(self):
        pass


    def testShortestRoute(self):        
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          shortestRouteCost,self.problem[1])
        agent = ShortestRouteAgent()
        answer = agent.solve(problem_state)
        for n in answer:
            print(n)
            
    def testFastestRoute(self):
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          fastestRouteCost,self.problem[1])
        agent = FastestRouteAgent()
        answer = agent.solve(problem_state)
        for n in answer:
            print(n)
            
    def testFuelSavingRoute(self):
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          fuelSavingRouteCost,self.problem[1])
        agent = FuelSavingRouteAgent()
        answer = agent.solve(problem_state)
        for n in answer:
            print(n)
            
    def testHybrid(self):
        alpha = 0.3
        beta = 0.3
        
        def hybridCost(aLink, route_map):
            return ProblemAction(alpha * shortestRouteCost(aLink, route_map).getCost() + \
                beta * fastestRouteCost(aLink, route_map).getCost() + \
                (1 - alpha - beta) * fuelSavingRouteCost(aLink, route_map).getCost())
        
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          hybridCost,self.problem[1])
        
        agent = HybridRouteAgent(alpha,beta)
        answer = agent.solve(problem_state)
        for n in answer:
            print(n)
        
            
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testShortestRoute']
    unittest.main()