from src.search.astar import AStar
from src.osm_utils4 import *
from src.sol.actionFactories import optimumPetrolConsumption
NO_LIMIT = -1
MAX_SPEED = 120
class ProblemAgent ():
    '''
    This is an interface for a Problem Solving Agent.
    '''
    
    def solve(self, problem_state, time_limit = NO_LIMIT):
        '''
        This is the method called by the runner of this agent.
        It includes the code that solves the problem.
        
        @param problem_state: Initial problem state.
        @param time_limit: The time limit for this agent.
        @return: A list of ProblemActions that solves the given problem.
        '''
        raise NotImplementedError()
    
class ShortestRouteAgent(ProblemAgent):
    def solve(self, problem_state, time_limit = float("inf")):
        alg = AStar(time_limit)            
        return alg.find(problem_state,ShortestRouteHeuristics())

class FastestRouteAgent(ProblemAgent):
    def solve(self, problem_state, time_limit = float("inf")):
        alg = AStar(time_limit)            
        return alg.find(problem_state,FastestRouteHeuristics())

class FuelSavingRouteAgent(ProblemAgent):   
    def solve(self, problem_state, time_limit = float("inf")):
        alg = AStar(time_limit)            
        return alg.find(problem_state,FuelSavingRouteHeuristics())

class HybridRouteAgent(ProblemAgent):
    def __init__(self,alpha,beta):
        self.heuristics = HybridHeuristics(alpha,beta)
        
    def solve(self, problem_state, time_limit = float("inf")):
        alg = AStar(time_limit)            
        return alg.find(problem_state,self.heuristics)

        
class ShortestRouteHeuristics():
    def evaluate(self,route_problem_state):  
        return route_problem_state.route_map.\
            JunctionDistance(route_problem_state.junction_key,\
                             route_problem_state.goal_junction)
    
class FastestRouteHeuristics():     
    def evaluate(self,route_problem_state):
        return route_problem_state.route_map.\
            JunctionDistance(route_problem_state.junction_key,\
                             route_problem_state.goal_junction) / (MAX_SPEED*1.0)
'''
def OptimumConsumption(routeMap):
        if routeMap.car in CAR_PETROL_PROFILE:
            minimum = 0
            for val in (CAR_PETROL_PROFILE[routeMap.car]):
                if ((minimum == 0 or val<=minimum) and val != 0):
                    minimum = val
            return minimum
        return DEFAULT_PETROL
'''    
class FuelSavingRouteHeuristics():
    def evaluate(self,route_problem_state):
        distance = route_problem_state.route_map. \
            JunctionDistance(route_problem_state.junction_key, \
                             route_problem_state.goal_junction)
        return optimumPetrolConsumption(route_problem_state.route_map,MAX_SPEED,distance)
#route_problem_state.route_map.OptimumConsumption()
                             
class HybridHeuristics():
    def __init__(self,alpha,beta):
        self.alpha = alpha
        self.beta = beta
    
    def evaluate(self,route_problem_state):
        return self.alpha * ShortestRouteHeuristics().evaluate(route_problem_state) + \
            self.beta * FastestRouteHeuristics().evaluate(route_problem_state) + \
            (1 - self.alpha - self.beta) * FuelSavingRouteHeuristics().evaluate(route_problem_state) 