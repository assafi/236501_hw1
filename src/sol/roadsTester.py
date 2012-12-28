'''
Created on 2012-12-27

@author: Gal
'''

from src.osm_utils4 import CountryMap, DEFAULT_DB_FILE, CAR_PETROL_PROFILE
from actionFactories import ShortestActionFactory, FastestActionFactory, \
    FuelSavingActionFactory, HybridActionFactory
from roadNet_State import RoadNet_State
import time
import math
from searchStatistics import SearchStatistics
from problemAgents import ShortestRouteAgent, FastestRouteAgent,\
    FuelSavingRouteAgent, HybridRouteAgent

def add(header,name):
    header.append(name+' solutionDistance')
    header.append(name+' sumDistance')
    header.append(name+' sumTime')
    header.append(name+' sumFuel')
    header.append(name+' callsToExpand')
    header.append(name+' cpuTime')
    header.append(name+' pathLength')
    
def writeLineToCsv(line,file2):
    #print line
    for st in line:
        #print st
        #print type(st)
        file2.write(str(st))
        file2.write(',')
    file2.write('\n')
    file2.flush()    


class RoadsTester(object):
    '''
    classdocs
    '''
    
    def __init__(self,maxRuns, car1, car2,alg):
        self.max = maxRuns
        self.alg = alg
        self.car1 = car1
        self.car2 = car2
        self.map = CountryMap()
        self.map.LoadMap2("../../"+DEFAULT_DB_FILE)
        self.map.car = car1
        self.problem = [0,0]#only decleration...
        self.statistics = SearchStatistics()
        
        #TODO: remove this is only to compare to Facebook
        problemKeys = {}
        problemKeys[0]=[452338,271665]
        problemKeys[1]=[774284,635241]
        problemKeys[2]=[674439,701233]
        problemKeys[3]=[902060,317092]
        problemKeys[4]=[307014,26939]
        problemKeys[5]=[579958,81815]
        problemKeys[6]=[425252,349512]
        problemKeys[7]=[918327,572887]
        problemKeys[8]=[710147,336195]
        problemKeys[9]=[327020,188803]
        
        self.problemKeys = problemKeys
        '''
        Constructor
        '''
    def performRun4(self):
        #prepare written csv header
        file2 = open("results.csv", "w")
        header = list()
        header.append('test#,src,dest,airDistance')
        add(header,'shortest')
        add(header,'fastest')
        add(header,'economic1')
        if self.car2!=None:
            add(header,'economic2')
        add(header,'hybrid1')
        if self.car2!=None:
            add(header,'hybrid2')
        
        writeLineToCsv(header, file2)
        for i in xrange(self.max):
            #TODO: remove this is only to compare to Facebook
            if self.problemKeys.has_key(i):
                self.problem = self.problemKeys[i]
            else:
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
            result.append(self.map.JunctionDistance(src,dest))
            #1
            self.appendResult(result,self.findShortestRoute())
            #2
            self.appendResult(result,self.findFastestRoute())
            
            #3
            self.map.car = self.car1
            self.appendResult(result,self.findFuelSavingRoute())
            
            if (self.car2!=None):
                #4
                self.map.car = self.car2
                self.appendResult(result,self.findFuelSavingRoute())
            #5
            self.map.car = self.car1
            self.appendResult(result,self.findHybrid(0.3,0.3))
            
            if self.car2!=None:
            #6
                self.map.car = self.car2
                self.appendResult(result,self.findHybrid(0.3,0.3))
            
            print i
            writeLineToCsv(result, file2)
        print 'done'
        file2.close()
        
    def performRun5(self):
        #prepare written csv header
        file2 = open("results.csv", "w")
        header = list()
        header.append('test#,src,dest,airDistance,w')
        add(header,'shortest')
        add(header,'fastest')
        add(header,'economic1')
        add(header,'hybrid1')
        
        writeLineToCsv(header, file2)
        for w in map(lambda x: x/40.0,xrange(1,40)):
            self.alg.setWeight(w)
            for i in xrange(self.max):
                #TODO: remove this is only to compare to Facebook
                if self.problemKeys.has_key(i):
                    self.problem = self.problemKeys[i]
                else:
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
                result.append(self.map.JunctionDistance(src,dest))
                result.append(w)
                #1
                self.appendResult(result,self.findShortestRoute())
                #2
                self.appendResult(result,self.findFastestRoute())
                
                #3
                self.map.car = self.car1
                self.appendResult(result,self.findFuelSavingRoute())
                
                #5
                self.map.car = self.car1
                self.appendResult(result,self.findHybrid(0.3,0.3))
                
                print i
                writeLineToCsv(result, file2)
            print 'done' + str(w)
        file2.close()
    def isFeasibile(self):
        answer = self.findShortestRoute()
        return answer!=None
    def appendResult(self,list2,element):
        time = self.elapsedTime()
        sum2 = sum(temp.getCost() for temp in element)
        length2 = len(element)
        
        callsToExpand = self.statistics.getCounter()
        src= self.problem[0]
        pathKeys = [src] + map(lambda x: x.getTargetKey(),element)

        def getLink(map2,s,t):
            sJunction = map2.GetJunction(s)
            for link in sJunction.links:
                if link.target == t:
                    return link
            print 'did not find for ({0},{1})'.format(s,t)

        
        sumDistance = sum([getLink(self.map,i, j).distance for i, j in zip(pathKeys[:-1], pathKeys[1:])])
        sumTime = sum([(getLink(self.map,i, j).distance/1000.0)*(1.0/getLink(self.map, i, j).speed) for i, j in zip(pathKeys[:-1], pathKeys[1:])])

        #this is only the fuel for the fastest (shortest) metric not for the economy (fuel saving) one...
        sumFuel = sum([(getLink(self.map,i, j).distance/1000.0)/CAR_PETROL_PROFILE[self.map.car][getLink(self.map, i, j).speed] for i, j in zip(pathKeys[:-1], pathKeys[1:])])
        
        list2.append(sum2 )#pathSum
        list2.append(sumDistance)
        list2.append(sumTime)
        list2.append(sumFuel)
        list2.append(callsToExpand)
        list2.append(time)#cpuTime
        list2.append(length2)#pathLength

    def printResult(self,result):
        if (result != None):
            aerielDistance = self.map.JunctionDistance(self.problem[0],self.problem[1]) 
            print 'airDistance({0},{1})={2}'.format(self.problem[0],self.problem[1],aerielDistance)
            sum2 = sum(temp.getCost() for temp in result)
            length2 = len(result)
            print 'path length: {0} cost: {1}'.format(length2,sum2)
    def resetStatistics(self):
        self.statistics = SearchStatistics()
        self.start= time.clock()
    def elapsedTime(self):
        return int(math.floor(time.clock()-self.start))
    
    
    def findShortestRoute(self):
        self.resetStatistics()        
        problem_state = RoadNet_State(self.problem[0],self.map,\
                                          ShortestActionFactory(),self.problem[1],self.statistics)
        agent = ShortestRouteAgent(self.alg)
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        return answer
            
    def findFastestRoute(self):
        self.resetStatistics()
        problem_state = RoadNet_State(self.problem[0],self.map,\
                                          FastestActionFactory(),self.problem[1],self.statistics)
        agent = FastestRouteAgent(self.alg)
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        return answer
    
    #was (0,40)
    def findFuelSavingRoute(self):
        self.resetStatistics()
        problem_state = RoadNet_State(self.problem[0],self.map,\
                                          FuelSavingActionFactory(self.map),\
                                          self.problem[1],self.statistics)
        agent = FuelSavingRouteAgent(self.alg)
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        return answer    
    def findHybrid(self,alpha,beta):
        self.resetStatistics()
        problem_state = RoadNet_State(self.problem[0],self.map,\
            HybridActionFactory(alpha,beta,ShortestActionFactory(),\
                                FastestActionFactory(),FuelSavingActionFactory(self.map))\
                                          ,self.problem[1],self.statistics)
        
        agent = HybridRouteAgent(self.alg,alpha,beta)
        answer = agent.solve(problem_state)
        '''for n in answer:
            print(n)
        '''
        return answer
