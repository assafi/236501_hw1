'''
Created on Dec 18, 2012

@author: Assaf
'''
from src.problem import ProblemAction

def shortestRouteCost(aLink, route_map):
    return ProblemAction(aLink.distance)

def fastestRouteCost(aLink, route_map):
            return ProblemAction(aLink.distance / \
                                 float(aLink.DefaultSpeed(aLink.highway_type)))
            
def fuelSavingRouteCost(aLink, route_map):
            return ProblemAction(route_map.PetrolConsumption(aLink.speed) * \
                                  aLink.distance)            