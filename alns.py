import random, time
from instance import Instance
from solution import Solution
from destroy import Destroy
from repair import Repair
from parameters import Parameters
import copy

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
        # cnt = 0
        self.tempSolution = copy.deepcopy(self.currentSolution)
        totalIter = 2000
        # print(self.tempSolution)
        for cnt in range(totalIter):
            
            # removaln = self.randomGen.randint(5, 12)
            self.tempSolution = copy.deepcopy(self.currentSolution)
            destroySolution = Destroy(self.instance, self.tempSolution)

            destroySolution.executeRandomRemoval(4, self.randomGen)
            tempSolution2 = destroySolution.solution.copy() # This is very important! 
            repairSolution = Repair(self.instance, tempSolution2)
            # repairSolution.executeGreedyInsertion(self.randomGen)
            repairSolution.executeMultiGreedyInsertion(self.randomGen)
            # print(len(tempSolution2.notServed), end = " ")
            # print(len(repairSolution.solution.served), end = "/|")
            if self.currentSolution.distance - repairSolution.solution.distance >= 1e-3:
                if len(repairSolution.solution.routes) > len(self.currentSolution.routes):
                    continue
                self.currentSolution = repairSolution.solution
                print(f"Found!! Obj: {repairSolution.solution.distance}, cnt : {cnt} , trucks: {len(repairSolution.solution.routes)} complete! ")
            
            # if cnt < totalIter:
            #     self.tempSolution = copy.deepcopy(self.currentSolution)
            #     destroySolution = Destroy(self.instance, self.tempSolution)
            #     destroySolution.executeEntireRouteRemoval(self.randomGen)
            #     originalFleetSize = len(destroySolution.solution.routes)
            #     tempSolution2 = destroySolution.solution.copy() # This is very important! 
            #     repairSolution = Repair(self.instance, tempSolution2)
            #     repairSolution.executeMultiGreedyInsertion(self.randomGen)
            #     # print(len(repairSolution.solution.routes), originalFleetSize, end = "/|")
            #     if len(repairSolution.solution.routes) <= originalFleetSize:
            #         self.currentSolution = repairSolution.solution
            #         print(f"Found Shorter Route!!! Obj: {repairSolution.solution.distance}, cnt : {cnt} , trucks: {len(repairSolution.solution.routes)} complete! ")
                    
                

            
        
        if self.currentSolution.checkFeasibility():
            print("Pass Feasibility Check!")
            # print(self.currentSolution)
        
    
    def constructInitialSolution(self):
        """Construct the initial solution
        """
        # 1. based on Solomon's time-oriented Nearest Neighbur Heuristic 
        self.currentSolution = Solution(self.instance, list(), list(), self.instance.customers.copy())
        # self.currentSolution.executeTimeNN()
        # 2. based on each route per customer ...
        # self.currentSolution.executeNaive()
        # 3. based on C-W saving Heuristic
        self.currentSolution.executeCWsaving(self.randomGen)


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
        
    