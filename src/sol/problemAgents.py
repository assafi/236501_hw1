'''
Created on Dec 26, 2012

@author: Assaf
'''
from src.problem_agent import ProblemAgent
from src.sol.problemHeuristics import ShortestRouteHeuristics,\
    FastestRouteHeuristics, FuelSavingRouteHeuristics, HybridHeuristics

class ShortestRouteAgent(ProblemAgent):
    def __init__(self,alg):
        self.alg = alg
        
    def solve(self, problem_state, time_limit = float("inf")):
        return self.alg.find(problem_state,ShortestRouteHeuristics())

class FastestRouteAgent(ProblemAgent):
    def __init__(self,alg):
        self.alg = alg
        
    def solve(self, problem_state, time_limit = float("inf")):
        return self.alg.find(problem_state,FastestRouteHeuristics())

class FuelSavingRouteAgent(ProblemAgent):   
    def __init__(self,alg):
        self.alg = alg
        
    def solve(self, problem_state, time_limit = float("inf")):
        return self.alg.find(problem_state,FuelSavingRouteHeuristics())

class HybridRouteAgent(ProblemAgent):
    def __init__(self,alg,alpha,beta):
        self.alg = alg
        self.heuristics = HybridHeuristics(alpha,beta)
        
    def solve(self, problem_state, time_limit = float("inf")):
        return self.alg.find(problem_state,self.heuristics)