import math
import random
import pickle

# A set of utilities for using a map imported from the openstreetmap project
# Written by Shaul Markovitch
# 
DEFAULT_PICKLED_FILE = "israel2.pickled"
DEFAULT_DB_FILE = "israel4"


DRIVEABLE_HIGHWAYS=['motorway','motorway_link','trunk','trunk_link',
                    'primary','primary_link','secondary','secondary_link',
                    'tertiary','tertiary_link','living_street','residential',
                    'unclassified']


SPEED_RANGES = [
                (80,120),   #'motorway'
                (80,100),   #'motorway_link'
                (70,110),   #'trunk'
                (70,90),    #'trunk_link'
                (60,100),   #'primary'
                (60,80),    # 'primary_link'
                (50,90),    #'secondary'
                (50,70),    # 'secondary_link'
                (40,80),    #'tertiary'
                (40,60),    # 'tertiary_link'
                (20,50),    #'living_street'
                (20,50),    #'residential'
                (30,90)     #'unclassified'
                ]
DEFAULT_HIGHWAY_TYPE =    12     #'unclassified'
DEFAULT_MINIMUM_DISTANCE = 50

DEFAULT_PETROL = 8
CAR_PETROL_PROFILE = {
    "Peugeot 508":
     [0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
         7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
         8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
         10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
         12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
         11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],

    "Mazda 3": 
         [0, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7,
         7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9,
         9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 
         11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12,
         12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11,
         11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    
    "Citroen C1": 
         [0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
         10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
         12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
         14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
         16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
         14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13],

    "Toyota Rav4": 
         [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
         4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
         6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
         7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
         6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],

    "Ford Focus": 
         [0, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7,
         7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10,
         10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 
         12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 14, 14, 14, 13, 12, 12, 12,
         12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11,
         11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
         
         
    "Skoda Fabia":
         [0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
          8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9,
          10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11,
          12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
          14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
          12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11] 
                    }
DEFAULT_CAR = "Peugeot 508"

CHANGE_PROBABILITY = 0.1
MAX_NUMBER_OF_CHANGE_EVENTS = 5
MAX_CHANGE = 0.5
GLOBAL_CHANGE_PROBABILITY = 0.1

class link:
    """
    Contains information about a link from a junction to another junction.
    If the road is two-way, there will be a separate link from the other junction.
    The target is the key of the taget junction.
    The distance is in KM.
    The name is the english name taken from openstreetmap database.  Many roads
    do not have a name.  The highway type is one of the keys in the SPEED_RANGES list.
    """
    def __init__(self, target, distance, highway_type = None, speed = None):
        self.target = target
        self.distance = distance
        #self.name = name
        if highway_type == None:
            self.highway_type = DEFAULT_HIGHWAY_TYPE
        else:   
            self.highway_type = highway_type
        if speed == None:
            self.speed = self.DefaultSpeed(self.highway_type)
        else:
            self.speed = speed
            
    def DefaultSpeed(self,type):
        limits = SPEED_RANGES[type]
        return (limits[0]+limits[1])/2


            
class junction: 
    """
    Contains information about a single junction.  The latitude and
    longitude, the name (as taken from openstreetmap db), the type,
    and the list of links to other junctions
    """ 
    def __init__(self,lat,lon,links=[]):
        self.lat = lat
        self.lon = lon
        #self.name = name
        #self.junction_type = junction_type
        self.links = links
        
        


class CountryMap:
    """
    The main class.  All the information is stored in the self.junctions
    dictionary, which contains the set of all junction instances, hashed by their keys.
    The keys are the ids (integers interpreted as strings) given in the openstreetmap
    db to allow debugging.
    """
    def __init__(self):
        self.junctions = []
        self.speed_ranges = SPEED_RANGES
        self.minimum_distance_for_problem = DEFAULT_MINIMUM_DISTANCE
        self.car = DEFAULT_CAR   
    
    def GetJunction(self,junction_key):
        return self.junctions[junction_key]
                
        
    def ComputeDistance(self,lat1, long1, lat2, long2):
        """
        The code for the ComputeDistance function was borrowed from 
        http://www.johndcook.com/python_longitude_latitude.html
        """
        if (lat1 == lat2 and long1 == long2):
            return 0.0
        if max(abs(lat1-lat2),abs(long1-long2)) < 0.00001:
            return 0.001
        #print lat1, "  ,  ", long1, "  ,  ",lat2,"  ,  ", long2
        # The code for this function was borrowed from here
        # http://www.johndcook.com/python_longitude_latitude.html
        #
        # Convert latitude and longitude to 
        # spherical coordinates in radians.
        degrees_to_radians = math.pi/180.0
        # phi = 90 - latitude
        phi1 = (90.0 - lat1)*degrees_to_radians
        phi2 = (90.0 - lat2)*degrees_to_radians
        #
        # theta = longitude
        theta1 = long1*degrees_to_radians
        theta2 = long2*degrees_to_radians
        #
        # Compute spherical distance from spherical coordinates.
        # 
        # For two locations in spherical coordinates 
        # (1, theta, phi) and (1, theta, phi)
        # cosine( arc length ) = 
        #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
        # distance = rho * arc length
        #
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
               math.cos(phi1)*math.cos(phi2))
        arc = math.acos( cos )
        #
        # Remember to multiply arc by the radius of the earth 
        # in your favorite set of units to get length.
        return arc * 6373

    def JunctionDistance(self,j1_key,j2_key):
        j1 = self.GetJunction(j1_key)
        j2 = self.GetJunction(j2_key)
        return self.ComputeDistance(j1.lat,j1.lon,j2.lat,j2.lon)

    def PetrolConsumption(self,speed):
        """
        Returns the petrol consumption (km per liter) of the current
        car according to its petrol profile.  The petrol profile lists
        the consumption for each integer speed between 0 and 120
        """
        car = self.car
        if car in CAR_PETROL_PROFILE:
            profile = CAR_PETROL_PROFILE[car]
            if speed >= len(profile):
                return profile[-1]
            else:
                return profile[speed]
        else:
            return DEFAULT_PETROL
    
    def OptimumConsumption(self):
        if self.car in CAR_PETROL_PROFILE:
            return min(CAR_PETROL_PROFILE[self.car])
        return DEFAULT_PETROL
            
    def GenerateRandomTraficReport(self):
        """
        Simulates trafic reports (Waze style).  Each link is assigned
        a speed generated randomly uniformly over the range of speeds
        associated with the particular road type.
        """
        random.seed()
        for j in self.junctions:
            for l in j.links:
                limits = self.speed_ranges[l.highway_type]
                l.speed = random.randrange(limits[0],limits[1]+1)
                
    def GetSpeedUpdates(self, list_of_links):
        """
        Simulates real-time updates.
        The route planing routine can call this function 
        during execution.
        The input is a list of tuples [(source-key1,target-key1),...]
        representing the links the caller is interested in.
        The algorithm returns a (possibly empty) list of changed links
        with the percentage (in [0,1]) of change
        since last report.
        [[(s1,t1), 0.1],[(s5,t5),-0.2]
        
        Parameters that affect the result:
        MAX_NUMBER_OF_CHANGE_EVENT - there is a limit on the number of change events 
        that take place during one search. (make sure to call self.ZeroCHangeCounter()
        before the search starts).
        GLOBAL_CHANGE_PROBABILITY - the probability that a change event will take place.
        CHANGE_PROBABILITY - the probability of one link speed to be changed.
        MAX_CHANGE - the maximal and minimal change (a number between 0 and 1).
        if the last speed of link l was 46 and the change is -0.3, the new speed is
        0.7*46=32.2    (should be int(last_speed * (1 + change))
        """
        if random.uniform(0,1) > GLOBAL_CHANGE_PROBABILITY:
            return []

        self.change_counter += 1
        if self.change_counter > MAX_NUMBER_OF_CHANGE_EVENTS:
            return []
        return [[l, random.uniform(-MAX_CHANGE,MAX_CHANGE)] for l in list_of_links
                  if  random.uniform(0,1) <= CHANGE_PROBABILITY]
    
    
    
    def ZeroChangeCounter(self):
        """
        This function MUST be called before a particular search run starts
        so that the number of times a a change occurs is bounded
        """
        self.change_counter = 0
        
        

    def GenerateProblem(self):
        l = len(self.junctions)
        return [random.randrange(0,l),random.randrange(0,l)]

# Old version!      
#     def GenerateProblem(self,min_distance = None):
#         """
#         Generates a problem (a pair of source junction key and target 
#         junction key).
#         It selects a random source.
#         To make sure the problem is solvable, it performs a random walk,
#         avoiding cycles.  Its main parameter is min_distance which makes
#         sure the problem is not too easy - it sets a lower bound on the aerial
#         distance between the source and the target
#         """
#         if min_distance == None:
#             min_distance = self.minimum_distance_for_problem
#         keys = self.junctions.keys()
#         trials = 0
#         while trials < 1000:
#             trials += 1
#             path = []
#             source_key = random.choice(keys)
#             current = source_key
#             legal_links = [l for l in self.GetJunction(current).links if [current,l.target] not in path]
#             #legal_links = [l for l in legal_links if [l.target,current] not in path]
#             while legal_links != []:
#                 #selected_link = random.choice(legal_links)
#                 selected_link = max(legal_links, key = lambda l: self.JunctionDistance(current,l.target))
#                 print selected_link.name, selected_link.highway_type, selected_link.distance
#                 next = selected_link.target
#                 dist = self.JunctionDistance(source_key,next) 
#                 print dist
#                 #print selected_link.name, "  ", selected_link.distance
#                 #print path
#                 if dist >= min_distance:
#                     return [source_key, next]
#                 path.append([current,next])
#                 current = next
#                 legal_links = [l for l in self.GetJunction(current).links if [current,l.target] not in path]
#                 #legal_links = [l for l in legal_links if [l.target,next] not in path]
#                 
#             print "Generation failed"
#         return "Fail"


    def LoadMap2(self,filename=DEFAULT_DB_FILE):
        for line in open(filename):
            junc = line.strip().split(",")
            junc[0] = float(junc[0])
            junc[1] = float(junc[1])
            j = junction(junc[0],junc[1])
            raw_links = junc[2].split("#")
            if raw_links == ['']:
                raw_links = []
                #print links
            interpreted_links = [[int(i) for i in l.split("@")] for l in raw_links]
            j.links = [link(l[0],l[1],l[2]) for l in interpreted_links]
            self.junctions.append(j)
        self.GenerateRandomTraficReport()
        self.MapStat()
    
    def LoadMap(self,filename=DEFAULT_PICKLED_FILE):
        f = open(filename)
        print "Loading pickled file.  This may take awhile..."
        self.junctions = pickle.load(f)
        print "Done. Generating trafic report."
        self.GenerateRandomTraficReport()
        self.MapStat()


    def MapStat(self):
        values = self.junctions
        branching = [len(v.links) for v in values]
        print "Number of junctions: ", len(values)
        print "Total links: ",  sum(branching)
        print "Max branch factor: ", max(branching)
        print "Average branchin factor: ", sum(branching)/(len(values)*1.0)
        distances = [l.distance  for j in values  for l in j.links]
        print "Max distance: ", max(distances)
        print "Min distance: ", min(distances)
        print "Average distance: ", sum(distances)/len(distances)
        speeds = [l.speed for j in values for l in j.links ]
        print "Max speed: ", max(speeds)
        print "Min speed: ", min(speeds)
        print "Average speed: ", sum(speeds)/len(speeds)
        for k in range(len(DRIVEABLE_HIGHWAYS)):
            print DRIVEABLE_HIGHWAYS[k], " :" , len([l for v in values for l in v.links if l.highway_type == k])
    
  
  
        
    
        
    

