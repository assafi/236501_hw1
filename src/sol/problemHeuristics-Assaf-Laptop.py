'''
Created on Dec 26, 2012

@author: Assaf
'''

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
        return FuelSavingActionFactory(route_problem_state.route_map).optimumPetrolConsumption(MAX_SPEED,distance)
#route_problem_state.route_map.OptimumConsumption()
                             
class HybridHeuristics():
    def __init__(self,alpha,beta):
        self.alpha = alpha
        self.beta = beta
    
    def evaluate(self,route_problem_state):
        return self.alpha * ShortestRouteHeuristics().evaluate(route_problem_state) + \
            self.beta * FastestRouteHeuristics().evaluate(route_problem_state) + \
            (1 - self.alpha - self.beta) * FuelSavingRouteHeuristics().evaluate(route_problem_state) 