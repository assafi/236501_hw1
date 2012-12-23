'''
Created on Dec 18, 2012

@author: Assaf
'''
from src.osm_utils4 import *
from src.sol.roadNet_Action import RoadNet_Action

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
                
    def create(self, aLink):
        #returns the optimum consumption in liters
        def optimumPetrolConsumption(routeMap,maxSpeed,distance):
            if routeMap.car in CAR_PETROL_PROFILE:
                return min(map(lambda x: (distance*1.0)/x, CAR_PETROL_PROFILE[routeMap.car][1:maxSpeed]))
            return (1.0/DEFAULT_PETROL)*distance
        return RoadNet_Action(optimumPetrolConsumption(self.map,aLink.speed,aLink.distance/1000.0),aLink.target)
        #this is another bug...
        '''return ProblemAction(1.0/self.PetrolConsumption(aLink.speed) * \
                                  aLink.distance)
        '''
    
    
    #shouldn't we normalize the values here?
class HybridActionFactory(ActionFactory):
    def __init__(self, alpha, beta, actionFactory1, actionFactory2, actionFactory3):
        self.alpha = alpha
        self.beta = beta
        self.actionFactory1 = actionFactory1
        self.actionFactory2 = actionFactory2
        self.actionFactory3 = actionFactory3
    def create(self, aLink):
        cost1 = self.actionFactory1.create(aLink).getCost()
        cost2 = self.actionFactory2.create(aLink).getCost()
        cost3 = self.actionFactory3.create(aLink).getCost()
        return RoadNet_Action(self.alpha * cost1 + self.beta * cost2 + \
                             (1 - self.alpha - self.beta) * cost3,aLink.target)
            
