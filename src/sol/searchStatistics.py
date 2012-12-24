'''
Created on 2012-12-24

@author: Gal
'''

class SearchStatistics(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.expandCounter=0
    def incrementExpand(self):
        self.expandCounter= self.expandCounter + 1