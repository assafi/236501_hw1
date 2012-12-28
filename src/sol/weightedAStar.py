#############################
##                         ##
##   weighted A* Search Algorithm   ##
##                         ##
#############################

# This is an implementation of the SearchAlgorithm interface for the following
# search algorithms:
# - weighted A*

from src.search.utils import *
from src.search.algorithm import Heuristic, SearchAlgorithm
from src.search.graph import GraphSearch


class WeightedAStar (SearchAlgorithm):
    '''
    Implementation of the A* search algorithm for the Problem.
    It may also take a maximum depth at which to stop, if needed.
    '''

    def __init__(self, w, max_depth=infinity):
        '''
        Constructs the A* search.
        Optionally, a maximum depth may be provided at which to stop looking for
        the goal state.
        '''
        self.max_depth = max_depth
        self.w = w
    def setWeight(self,w):
        self.w = w
    def find(self, problem_state, heuristic):
        '''
        A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search.
        Uses the pathmax trick: f(n) = max(f(n), g(n)+h(n)).

        @param problem_state: The initial state to start the search from.
        @param heuristic: A heuristic function that scores the Problem states.
        '''
        # This is the node evaluation function for the given heuristic.
        def evaluator(node):
            return node.path_cost + heuristic.evaluate(node.state)
    
        # This is a generator for the PriorityQueue we need.
        def queue_generator():
            return PriorityQueue(evaluator)

        # Use a graph search with a minimum priority queue to conduct the search.
        search = GraphSearch(queue_generator, self.max_depth)
        return search.find(problem_state)