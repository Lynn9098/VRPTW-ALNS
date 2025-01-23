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
        
        self.tempSolution = self.currentSolution.copy()
        
        print(self.tempSolution.distance)
            
        destroySolution = Destroy(self.instance, self.tempSolution)

        destroySolution.executeRandomRemoval(70, self.randomGen)

        tempSolution2 = destroySolution.solution.copy()
        
        repairSolution = Repair(self.instance, tempSolution2)
        
        repairSolution.executeGreedyInsertion(self.randomGen)

        self.tempSolution = repairSolution.solution
            # self.display(isbest= False)
        
    
    def constructInitialSolution(self):
        """Construct the initial solution
        """
        # 1. based on Solomon's time-oriented Nearest Neighbur Heuristic 
        self.currentSolution = Solution(self.instance, list(), list(), self.instance.customers.copy())
        self.currentSolution.executeTimeNN()
        self.currentSolution.executeForwardSlack()
        # for route in self.currentSolution.routes:
        #     print(route.forwardTimeSlack)
        self.bestSolution = self.currentSolution.copy()
        # test = [-1 for _ in range(101)]
        # for route in self.bestSolution.routes:
        #     print(route.forwardTimeSlack)
        print(f"Total trucks: { len(self.currentSolution.routes) }")


    def display(self, isbest = True):
        if isbest:
            print(self.bestSolution)

        else:
            print(self.currentSolution)
            
                
    
    
    def destroyAndRepair(self, destroyOptNo, repairOptNo, size):
        # depict the destroy and repair process ... 
        self.tempSolution = self.currentSolution.copy()
        destroySolution = Destroy(self.instance, self.tempSolution)
        destroySolution.executeRandomRemoval(size, self.randomGen)
        print("...")
        print(destroySolution)
        
    