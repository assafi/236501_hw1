'''
Created on Dec 18, 2012

@author: Assaf
'''
from src.problem import ProblemAction

class ActionFactory():
    def create(self, aLink):
        raise NotImplementedError()

class ShortestActionFactory(ActionFactory):
    def create(self, aLink):
        return ProblemAction(aLink.distance)
    
class FastestActionFactory(ActionFactory):
    def create(self, aLink):
        return ProblemAction(aLink.distance / \
                                 float(aLink.DefaultSpeed(aLink.highway_type)))

class FuelSavingActionFactory(ActionFactory):
    def __init__(self, route_map):
        self.route_map = route_map
    def create(self, aLink):
        return ProblemAction(self.route_map.PetrolConsumption(aLink.speed) * \
                                  aLink.distance)
            
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
        return ProblemAction(self.alpha * cost1 + self.beta * cost2 + \
                             (1 - self.alpha - self.beta) * cost3)
            
