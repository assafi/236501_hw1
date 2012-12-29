'''
Created on Dec 21, 2012

@author: Assaf
'''
from src.search.utils import infinity, PriorityQueue, LIFOQueue
from src.search.algorithm import SearchAlgorithm
from src.search.graph import Node

class AStarWithUpdatesComplex():
    '''
    This is the modified version of AStar, capable of
    receiving a bound number of cost updates. Upon each 
    update of links in Closed, it will reinstate the links 
    to Open, and thus the algorithm will recalculate the path. 
    '''

    def __init__(self, max_depth=infinity):
        '''
        Constructs the A* search.
        Optionally, a maximum depth may be provided at which to stop looking for
        the goal state.
        '''
        self.max_depth = max_depth

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
        search = UpdatableGraphSearch(queue_generator, self.max_depth)
        return search.find(problem_state)

LINK_ID=0
CHANGE=1
   
class UpdatableGraphSearch (SearchAlgorithm):
    '''
    Implementation of a simple generic graph search algorithm for the Problem.
    It takes a generator for a container during construction, which controls the
    order in which open states are handled (see documentation in __init____).
    It may also take a maximum depth at which to stop, if needed.
    '''

    def __init__(self, container_generator, max_depth=infinity):
        '''
        Constructs the graph search with a generator for the container to use
        for handling the open states (states that are in the open list).
        The generator may be a class type, or a function that is expected to
        create an empty container.
        This may be used to effect the order in which to address the states,
        such as a stack for DFS, a queue for BFS, or a priority queue for A*.
        Optionally, a maximum depth may be provided at which to stop looking
        for the goal state.
        '''
        self.container_generator = container_generator
        self.max_depth = max_depth

    def find(self, problem_state, heuristic=None):
        '''
        Performs a full graph search, expanding the nodes on the fringe into
        the queue given at construction time, and then goes through those nodes
        at the order of the queue.
        If a maximal depth was provided at construction, the search will not
        pursue nodes that are more than that depth away in distance from the
        initial state.
                
        @param problem_state: The initial state to start the search from.
        @param heuristic: Ignored.
        '''
        m = problem_state.route_map
        m.ZeroChangeCounter()
        open_nodes = self.container_generator()
        closed_states = {}
        traversed_links = []
        open_nodes.append(Node(problem_state))
        while open_nodes and len(open_nodes) > 0:
            updated_links = m.GetSpeedUpdates(traversed_links)
            for ul in updated_links:
                junction_key = ul[LINK_ID][0]
                node = closed_states[junction_key][0]
                self.updateLink(node.state,ul)
                print "link #"+str(ul[LINK_ID])+" changed: "+str(ul[CHANGE])
                if (ul[CHANGE] < 0):
                    open_nodes.append(node)
                if (ul[CHANGE] > 0):
                    open_nodes = self.updateSubTree(node,closed_states,open_nodes)
                    
            node = open_nodes.pop()
            
            if node.depth > self.max_depth:
                print 'bug?'
                continue
            
            if node.state.isGoal(): 
                return node.getPathActions()
            
            if (node.state.junction_key not in closed_states) or (node.path_cost < closed_states[node.state.junction_key][1]):
                closed_states[node.state.junction_key] = (node,node.path_cost)
                traversed_links.extend(node.state.getLinks())
                successors = node.expand()
                open_nodes.extend(successors)
        print 'failed to find'
        return None
    
    def updateSubTree(self,root,tree,front):
        '''This function updates all the path_cost (with diff) of the sub-tree in tree that starts in root, until it reaches the front.
            This is done in DFS style'''
        open_nodes = []
        closed_states = {}
        open_nodes.append(root)
        update_open_list = []
        while open_nodes and len(open_nodes) > 0:
            node = open_nodes.pop() 
            if node.state in map(lambda x: x[1].state, front.q) and node.state not in map(lambda x: x.state,update_open_list):
                update_open_list += [node]
                continue
            if (node.state.junction_key not in closed_states) or (node.path_cost < closed_states[node.state.junction_key]):
                closed_states[node.state.junction_key] = node.path_cost
                tree[node.state.junction_key] = (node,node.path_cost)
                successors = node.expand()
                open_nodes.extend(successors)
        new_front = self.container_generator()
        new_front.extend(update_open_list)
        new_front.extend(filter(lambda x: x.state not in map(lambda y: y.state, update_open_list),map(lambda y: y[1],front.q)))
        return new_front
    
    def updateLink(self,state,ul):
        junction = state.route_map.GetJunction(ul[LINK_ID][0])
        linkToUpdate = filter(lambda l: l.target == ul[LINK_ID][1],junction.links)[0]          
        linkToUpdate.speed *= (1 + ul[CHANGE])        
                