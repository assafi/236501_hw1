'''
Created on Dec 26, 2012

@author: Assaf
'''
from src.sol.actionFactories import FuelSavingActionFactory
from consts import SHORTEST_NORMALIZATION_FACTOR,\
    FASTEST_NORMALIZATION_FACTOR, ECO_NORMALIZATION_FACTOR,\
    MAX_SPEED,MIN_SPEED


class ShortestRouteHeuristics():
    def evaluate(self,route_problem_state):  
        return route_problem_state.route_map.\
            JunctionDistance(route_problem_state.junction_key,\
                             route_problem_state.goal_junction)*1000
class FastestRouteHeuristics():     
    def evaluate(self,route_problem_state):
        return route_problem_state.route_map.\
            JunctionDistance(route_problem_state.junction_key,\
                             route_problem_state.goal_junction)*1000 / (MAX_SPEED*1.0)
  
class FuelSavingRouteHeuristics():
    def evaluate(self,route_problem_state):
        distance = route_problem_state.route_map. \
            JunctionDistance(route_problem_state.junction_key, \
                             route_problem_state.goal_junction)*1000
        return FuelSavingActionFactory(route_problem_state.route_map).optimumPetrolConsumption(MIN_SPEED,MAX_SPEED,distance)

class HybridHeuristics():
    def __init__(self,alpha,beta):
        self.w1 = alpha*SHORTEST_NORMALIZATION_FACTOR
        self.w2 = beta*FASTEST_NORMALIZATION_FACTOR
        self.w3 = (1 - alpha - beta)*ECO_NORMALIZATION_FACTOR
    
    def evaluate(self,route_problem_state):
        return self.w1 * ShortestRouteHeuristics().evaluate(route_problem_state) + \
            self.w2 * FastestRouteHeuristics().evaluate(route_problem_state) + \
             self.w3* FuelSavingRouteHeuristics().evaluate(route_problem_state) \
