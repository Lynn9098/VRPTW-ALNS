import random, time
from instance import Instance
from solution import Solution
from parameters import Parameters

class ALNS:
    """
    Class that models the ALNS algorithm. 

    Parameters
    ----------
    instance : Instance
        The problem instance that we want to solve.
    
    """

    def __init__(self, instance):
        self.instance = instance
        self.randomGen = random.random(Parameters.randomSeed) # for reproducibility

    def execute(self):
        starttime = time.time()
        self.constructInitialSolution()
        endtime = time.time()
        cpuTime = round(endtime - starttime, 3)
        print(f"Terminated! CPU times {cpuTime} seconds")
        self.display()
    
    def constructInitialSolution(self):
        """Construct the initial solution
        """
        # 1. based on Solomon's time-oriented Nearest Neighbur Heuristic 
        self.currentSolution = Solution(self.instance, list(), list(), self.instance.customers.copy())
        self.currentSolution.executeTimeNN()
        self.bestSolution = self.currentSolution.copy()
        test = [-1 for _ in range(101)]
        print(f"Total trucks: { len(self.currentSolution.routes) }")
        # for route in self.currentSolution.routes:
        #     for n in route.nodes:
        #         if test[n.id] == -1:
        #             test[n.id] = 0
                    
    def display(self, isbest = True):
        if isbest:
            num_route = len(self.bestSolution.routes)
            print(f"Solution objective: {self.bestSolution.distance}; \nTruck used: {len(self.bestSolution.routes)}\n\n")
            for i in range(num_route):
                print(f"Truck {i}")
                nodes = self.currentSolution.routes[i].nodes
                for m in nodes:
                    print(m)
                print("")
        else:
            num_route = len(self.currentSolution.routes)
            
            print(f"Solution objective: {self.currentSolution.distance}; \nTruck used: {len(self.currentSolution.routes)}\n\n")
            for i in range(num_route):
                print(f"Truck {i}")
                nodes = self.currentSolution.routes[i].nodes
                for m in nodes:
                    print(m)
                print("")
                
    
    
    def destroyAndRepair(self):
        # depict the destroy and repair process ... 
        pass
    