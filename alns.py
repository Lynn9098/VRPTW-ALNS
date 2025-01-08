import random, time
from instance import Instance
from solution import Solution
from destroy import Destroy
from repair import Repair
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
        self.randomGen = random.Random(Parameters.randomSeed) # for reproducibility

    def execute(self):
        starttime = time.time()
        self.constructInitialSolution()
        endtime = time.time()
        cpuTime = round(endtime - starttime, 3)
        print(f"Terminated! CPU times {cpuTime} seconds")
        # print(self.route)
        # self.destroyAndRepair(0,0,30)
        self.tempSolution = self.currentSolution.copy()
        destroySolution = Destroy(self.instance, self.tempSolution)
        destroySolution.executeRandomRemoval(5, self.randomGen)
        repairSolution = Repair(self.instance, self.tempSolution)
        repairSolution.executeGreedyInsertion(self.randomGen)
        # self.display(isbest= False)
        
    
    def constructInitialSolution(self):
        """Construct the initial solution
        """
        # 1. based on Solomon's time-oriented Nearest Neighbur Heuristic 
        self.currentSolution = Solution(self.instance, list(), list(), self.instance.customers.copy())
        self.currentSolution.executeTimeNN()
        self.currentSolution.executeForwardSlack()
        self.bestSolution = self.currentSolution.copy()
        # test = [-1 for _ in range(101)]
        print(f"Total trucks: { len(self.currentSolution.routes) }")

        # for route in self.currentSolution.routes:
        #     for n in route.nodes:
        #         if test[n.id] == -1:
        #             test[n.id] = 0
                    
    def display(self, isbest = True):
        if isbest:
            print(self.bestSolution)
            # num_route = len(self.bestSolution.routes)
            # print(f"Solution objective: {self.bestSolution.distance}; \nTruck used: {len(self.bestSolution.routes)}\n\n")
            # for i in range(num_route):
            #     print(f"Truck {i}")
            #     print(self.bestSolution.routes[i])
                # nodes = self.currentSolution.routes[i].nodes
                # for m in nodes:
                #     print(m)
                # print("")
        else:
            print(self.currentSolution)
            # num_route = len(self.currentSolution.routes)
            # print(f"Solution objective: {self.currentSolution.distance}; \nTruck used: {len(self.currentSolution.routes)}\n\n")
            # for i in range(num_route):
            #     print(f"Truck {i}")
            #     print(self.bestSolution.routes[i])
                # nodes = self.currentSolution.routes[i].nodes
                # for m in nodes:
                #     print(m)
                # print("")
                
    
    
    def destroyAndRepair(self, destroyOptNo, repairOptNo, size):
        # depict the destroy and repair process ... 
        self.tempSolution = self.currentSolution.copy()
        destroySolution = Destroy(self.instance, self.tempSolution)
        destroySolution.executeRandomRemoval(size, self.randomGen)
        print("...")
        print(destroySolution)
        
    