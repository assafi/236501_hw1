'''
Created on Dec 17, 2012

@author: Assaf
'''
from src.osm_utils4 import CountryMap, DEFAULT_DB_FILE
from src.problem import ProblemAction
from src.problem_agent import ShortestRouteAgent, FastestRouteAgent, \
    FuelSavingRouteAgent, HybridRouteAgent
from src.sol.actionFactories import ShortestActionFactory, FastestActionFactory, \
    FuelSavingActionFactory, HybridActionFactory
from src.sol.route_problem import RouteProblemState
import unittest

MAX = 100
car1= "Peugeot 508"
car2= "Ford Focus"

class Test(unittest.TestCase):


    def setUp(self):
        self.map = CountryMap()
        self.map.LoadMap2("../../"+DEFAULT_DB_FILE)
        #self.problem = self.map.GenerateProblem()

    def tearDown(self):
        pass

    def isFeasibile(self,src,dest):
        answer = self.findShortestRoute()
        return answer!=None
    def runAll(self):
        for i in xrange(MAX):
            srcDest = self.map.GenerateProblem()
            src = srcDest[0]
            dest = srcDest[1]
            
            while (False==self.isFeasibile(src,dest)):
                print 'no solution for ({0},{1})'.format(src,dest)
                srcDest = self.map.GenerateProblem()
                src = srcDest[0]
                dest = srcDest[1]
            self.problem = srcDest
            #1
            self.findShortestRoute()
            #2
            self.findFastestRoute()
            #3
            self.map.car = car1;
            self.findFuelSavingRoute()
            #4
            self.map.car = car2;
            self.findFuelSavingRoute()
            #5
            self.map.car = car1;
            self.findHybrid(0.3,0.3)
            #6
            self.map.car = car2;
            self.findHybrid(0.3,0.3)
            
            print i
        print 'done'
    
    def testAll(self):
        self.problem = self.map.GenerateProblem()
        self.findShortestRoute()
        print 'shortest done'
        self.findFastestRoute()
        print 'fastest done'
        self.findFuelSavingRoute()
        print 'economic done'
        self.findHybrid(0.3,0.3)
        print 'hybrid done'
    def findShortestRoute(self):        
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          ShortestActionFactory(),self.problem[1])
        agent = ShortestRouteAgent()
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        if (answer!=None):
            print (len(answer))
        return answer
            
    def findFastestRoute(self):
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          FastestActionFactory(),self.problem[1])
        agent = FastestRouteAgent()
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        if (answer!=None):
            print (len(answer))
        return answer
    
    #was (0,40)
    def findFuelSavingRoute(self):
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          FuelSavingActionFactory(self.map),\
                                          self.problem[1])
        agent = FuelSavingRouteAgent()
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        if (answer!=None):
            print (len(answer))
        return answer    
    def findHybrid(self,alpha,beta):
        problem_state = RouteProblemState(self.problem[0],self.map,\
            HybridActionFactory(alpha,beta,ShortestActionFactory(),\
                                FastestActionFactory(),FuelSavingActionFactory(self.map))\
                                          ,self.problem[1])
        
        agent = HybridRouteAgent(alpha,beta)
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        if (answer!=None):
            print (len(answer))
        return answer

if __name__ == "__main__":
#    import sys;sys.argv = ['Test.testFuelSavingRoute']
    unittest.main()