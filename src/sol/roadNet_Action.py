'''
Created on 2012-12-23

@author: Gal
'''
from src.problem import ProblemAction
class RoadNet_Action(ProblemAction):
    '''
    classdocs
    '''

    def __init__(self, cost, targetKey):
        '''
        Initiates this Action with a cost.
        Default cost is 1.
        
        @param cost: (Optional) the cost of this Action. Default is 1.
        '''
        ProblemAction.__init__(self, cost)
        #self.cost = cost
        self.targetKey = targetKey
        
    def __cmp__(self, other):
        '''
        The comparison method must be implemented to ensure deterministic results.
        @return: Negative if self < other, zero if self == other and strictly 
        positive if self > other.
        '''
        
        if self.cost != other.cost:
            return self.cost - other.cost
        return self.targetKey - other.targetKey
    
    def __hash__(self):
        '''
        The hash method must be implemented for actions to be inserted into sets 
        and dictionaries.
        @return: The hash value of the action.
        '''
        return int(self.cost * 1000)+ self.targetKey
    
    def __str__(self):
        '''
        @return: The string representation of this object when *str* is called.
        '''
        return str(self.cost) +' '+ str(self.targetKey)
    
    def __repr__(self):
        '''
        Same as __str__, unless overridden.
        
        @return: The string representation of this object when *printed*.
        '''
        return str(self.cost) +' ' +str(self.targetKey)
    def __eq__(self, other):
        return self.cost == other.cost and self.targetKey == other.targetKey