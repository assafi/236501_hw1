'''
Created on Dec 18, 2012

@author: Assaf
'''
from src.sol.roadNet_Action import RoadNet_Action
from src.osm_utils4 import CAR_PETROL_PROFILE, DEFAULT_PETROL
from consts import SHORTEST_NORMALIZATION_FACTOR,\
    FASTEST_NORMALIZATION_FACTOR, ECO_NORMALIZATION_FACTOR

#returns the optimum consumption in liters
#routeMap - map
#maxSpeed - the maximum speed for this link km/h
#distance - the distance on this link - km

class ActionFactory():
    def create(self, aLink):
        raise NotImplementedError()

class ShortestActionFactory(ActionFactory):
    def create(self, aLink):
        return RoadNet_Action(aLink.distance,aLink.target)
    
class FastestActionFactory(ActionFactory):
    def create(self, aLink):
        return RoadNet_Action((aLink.distance/1000.0) / \
                                 (aLink.speed),aLink.target)
#bug: double(aLink.DefaultSpeed(aLink.highway_type)))

class FuelSavingActionFactory(ActionFactory):
    def __init__(self, route_map):
        self.map = route_map
    
    def optimumPetrolConsumption(self,maxSpeed,distance):
        if self.map.car in CAR_PETROL_PROFILE:
            return min(map(lambda x: distance/(1.0*x), CAR_PETROL_PROFILE[self.map.car][1:maxSpeed]))
        return (1.0/DEFAULT_PETROL)*distance
                
    def create(self, aLink):
        return RoadNet_Action(self.optimumPetrolConsumption(aLink.speed,aLink.distance/1000.0),aLink.target)
        #this is another bug...
        '''return ProblemAction(1.0/self.PetrolConsumption(aLink.speed) * \
                                  aLink.distance)
        '''    
class HybridActionFactory(ActionFactory):
    def __init__(self, alpha, beta, actionFactory1, actionFactory2, actionFactory3):
        self.w1 = alpha * SHORTEST_NORMALIZATION_FACTOR
        self.w2 = beta * FASTEST_NORMALIZATION_FACTOR
        self.w3 = (1 - alpha - beta) * ECO_NORMALIZATION_FACTOR
        self.actionFactory1 = actionFactory1
        self.actionFactory2 = actionFactory2
        self.actionFactory3 = actionFactory3
    def create(self, aLink):
        cost1 = self.actionFactory1.create(aLink).getCost()
        cost2 = self.actionFactory2.create(aLink).getCost()
        cost3 = self.actionFactory3.create(aLink).getCost()
        return RoadNet_Action(self.w1 * cost1 + self.w2 * cost2 + \
                              self.w3* cost3,aLink.target)
            
