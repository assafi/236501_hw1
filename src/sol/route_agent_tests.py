'''
Created on Dec 17, 2012

@author: Assaf
'''
from src.osm_utils4 import CountryMap, DEFAULT_DB_FILE
from src.problem_agent import ShortestRouteAgent, FastestRouteAgent, \
    FuelSavingRouteAgent, HybridRouteAgent
from src.sol.actionFactories import ShortestActionFactory, FastestActionFactory, \
    FuelSavingActionFactory, HybridActionFactory
from src.sol.route_problem import RouteProblemState
import unittest
import time
import math

MAX = 100
car1= "Peugeot 508"
car2= "Ford Focus"

class Test(unittest.TestCase):


    def setUp(self):
        self.map = CountryMap()
        self.map.LoadMap2("../../"+DEFAULT_DB_FILE)
        self.map.car = car1
        self.problem = [0,0]#only decleration...

    def tearDown(self):
        pass

    def isFeasibile(self):
        answer = self.findShortestRoute()
        return answer!=None
    def appendResult(self,list2,element):
        time = self.elapsedTime()
        sum2 = sum(temp.getCost() for temp in element)
        length2 = len(element)
        list2.append(length2)#pathLength
        list2.append(sum2 )#pathSum
        list2.append(time)#cpuTime
    def testRunAll(self):
        
        def add(l,name):
            header.append(name+' pathLength')
            header.append(name+' solutionDistance')
            header.append(name+' cpuTime')
            
        def writeLineToCsv(line,file2):
            #print line
            for st in line:
                #print st
                #print type(st)
                file2.write(str(st))
                file2.write(',')
            file2.write('\n')
            file2.flush()    
        '''
        def writeToCsv(results):
            file2 = open("results.csv", "w")
            for line in results:
                print line
                for st in line:
                    print st
                    #print type(st)
                    file2.write(str(st))
                    file2.write(',')
                file2.write('\n')
        '''            
        
        #prepare written csv header
        file2 = open("results.csv", "w")
        header = list()
        header.append('test#,src,dest,airDistance')
        add(header,'shortest')
        add(header,'fastest')
        add(header,'economic1')
        add(header,'economic2')
        add(header,'hybrid1')
        add(header,'hybrid2')
        writeLineToCsv(header, file2)
        for i in xrange(MAX):
            self.problem = self.map.GenerateProblem()
            
            while (False==self.isFeasibile()):
                print 'no solution for ({0},{1})'.format(self.problem[0],self.problem[1])
                self.problem = self.map.GenerateProblem()
            src = self.problem[0]
            dest = self.problem[1]
            print '({0},{1})'.format(src,dest)
            result = list()
            result.append(i)
            result.append(src)
            result.append(dest)
            result.append(dest)
            result.append(self.map.JunctionDistance(src,dest))
            #1
            self.appendResult(result,self.findShortestRoute())
            #2
            self.appendResult(result,self.findFastestRoute())
            
            #3
            self.map.car = car1
            self.appendResult(result,self.findFuelSavingRoute())
            
            #4
            self.map.car = car2
            self.appendResult(result,self.findFuelSavingRoute())
            #5
            self.map.car = car1
            self.appendResult(result,self.findHybrid(0.3,0.3))
            
            #6
            self.map.car = car2
            self.appendResult(result,self.findHybrid(0.3,0.3))
            
            print i
            writeLineToCsv(result, file2)
        print 'done'
        file2.close()
        #writeToCsv(results)
    def printResult(self,result):
        if (result != None):
            aerielDistance = self.map.JunctionDistance(self.problem[0],self.problem[1]) 
            print 'airDistance({0},{1})={2}'.format(self.problem[0],self.problem[1],aerielDistance)
            sum2 = sum(temp.getCost() for temp in result)
            length2 = len(result)
            print 'path length: {0} cost: {1}'.format(length2,sum2)
    def resetTimer(self):
        self.start= time.clock()
    def elapsedTime(self):
        return int(math.floor(time.clock()-self.start))
    
    
    ''' 
    def testAll(self):
        self.problem = [0,0]
        answer = self.findShortestRoute()
        self.printResult(answer)
        print 'stupid shortest done in {0}'.format(self.elapsedTime())
        
        
        self.problem = self.map.GenerateProblem()
        #self.problem = [452338,271665]
        answer = self.findShortestRoute()
        self.printResult(answer)
        print 'shortest done in {0}'.format(self.elapsedTime())
        answer = self.findFastestRoute()
        self.printResult(answer)
        print 'fastest done in {0}'.format(self.elapsedTime())
        answer = self.findFuelSavingRoute()
        self.printResult(answer)
        print 'economic done in {0}'.format(self.elapsedTime())
        answer = self.findHybrid(0.3,0.3)
        self.printResult(answer)
        print 'hybrid done in {0}'.format(self.elapsedTime())
    '''
    def findShortestRoute(self):
        self.resetTimer()        
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          ShortestActionFactory(),self.problem[1])
        agent = ShortestRouteAgent()
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        return answer
            
    def findFastestRoute(self):
        self.resetTimer()
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          FastestActionFactory(),self.problem[1])
        agent = FastestRouteAgent()
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        return answer
    
    #was (0,40)
    def findFuelSavingRoute(self):
        self.resetTimer()
        problem_state = RouteProblemState(self.problem[0],self.map,\
                                          FuelSavingActionFactory(self.map),\
                                          self.problem[1])
        agent = FuelSavingRouteAgent()
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        return answer    
    def findHybrid(self,alpha,beta):
        self.resetTimer()
        problem_state = RouteProblemState(self.problem[0],self.map,\
            HybridActionFactory(alpha,beta,ShortestActionFactory(),\
                                FastestActionFactory(),FuelSavingActionFactory(self.map))\
                                          ,self.problem[1])
        
        agent = HybridRouteAgent(alpha,beta)
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        return answer

if __name__ == "__main__":
#    import sys;sys.argv = ['Test.testFuelSavingRoute']
    unittest.main()