'''
Created on Dec 26, 2012

@author: Assaf
'''
import unittest
from src.sol.roadNet_State import RoadNet_State
from src.sol.actionFactories import ShortestActionFactory
from src.sol.problemAgents import ShortestRouteAgent
from src.sol.astar_with_updates import AStar2


class Test(unittest.TestCase):


    def testUpdatableAStar(self):
        problem_state = RoadNet_State(self.problem[0],self.map,\
                                          ShortestActionFactory(),self.problem[1],self.statistics)
        agent = ShortestRouteAgent(AStar2())
        return agent.solve(problem_state)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testUpdatableAStar']
    unittest.main()