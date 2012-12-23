'''
Created on Dec 16, 2012

@author: Assaf
'''
from src.problem import ProblemState

class RouteProblemState(ProblemState):
    '''
    classdocs
    '''


    def __init__(self, junction_key, route_map, actionFactory, goal_junction):
        '''
        Constructor
        '''
        self.junction_key = junction_key
        self.route_map = route_map
        self.actionFactory = actionFactory
        self.goal_junction = goal_junction
    
    def getSuccessors(self):
        '''
        Generates all the actions that can be performed from this state, and
        the States those actions will create.
        
        @return: A dictionary containing each action as a key, and its state.
        '''
        currentJunc = self.route_map.GetJunction(self.junction_key)
        l = map(lambda l: 
                   (self.actionFactory.create(l),
                    RouteProblemState(l.target,self.route_map,self.actionFactory,self.goal_junction))
                    ,currentJunc.links)
        d = {}
        i=0
        for k,v in l:
            d[k] = v
            i = i+1
        '''
        if i!=len(d):
            print 'inserted {0} elements now {1} there are {2} links'.format(i,len(d),len(currentJunc.links))
            for k,v in l:
                print k,v
        '''
        return d
    
    def isGoal(self):
        '''
        @return: Whether this Problem state is the searched goal or not.
        '''
        return self.junction_key == self.goal_junction
    
    def __cmp__(self, other):
        '''
        The comparison method must be implemented to ensure deterministic results.
        @return: Negative if self < other, zero if self == other and strictly 
        positive if self > other.
        '''
        return self.junction_key - other.junction_key
    
    def __hash__(self):
        '''
        The hash method must be implemented for states to be inserted into sets 
        and dictionaries.
        @return: The hash value of the state.
        '''
        return self.junction_key
    
    def __str__(self):
        return str(self.junction_key)
    
    def __repr__(self):
        return self.__str__()