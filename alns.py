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
        self.avgCusRmved = Parameters.avgCusRmved
        self.maxStringLen = Parameters.maxStringLen

    def execute(self):
        starttime = time.time()
        self.constructInitialSolution()
        endtime = time.time()
        cpuTime = round(endtime - starttime, 3)

        print(f"Terminated! CPU times {cpuTime} seconds, cost : {self.currentSolution.distance}")

        self.tempSolution = copy.deepcopy(self.currentSolution)
        totalIter = 15000
        
        starttime = time.time()
        for cnt in range(totalIter):
        
            removaln = self.randomGen.randint(1, int(0.1 * self.instance.numNodes - 1))
            if cnt == 0:
                chooseDestroy = self.randomGen.randint(1, 8)
            else:
                chooseDestroy = self.randomGen.randint(1, 8)
            # print(f"Iter {cnt}, destroy method:  {chooseDestroy}")
            if chooseDestroy <= 3:
                repairSolution = self.destroyAndRepair(1, 1, removaln)
            elif chooseDestroy <= 6:
                repairSolution = self.destroyAndRepair(2, 1, removaln)
            else:
                repairSolution = self.destroyAndRepair(3, 1, removaln)
            
            # repairSolution = self.destroyAndRepair(1, 1, removaln)
            # repairSolution = self.destroyAndRepair(2, 1, removaln)
            # repairSolution = self.destroyAndRepair(3, 1, removaln)
            # repairSolution = self.destroyAndRepair(chooseDestroy, 1, removaln)
            self.ifAccept(repairSolution, cnt, chooseDestroy, 1)

            if cnt < totalIter * 0.25:
                self.executeFleetMin(cnt)
        
        endtime = time.time()
        cpuTimeIteration = round(endtime - starttime, 3)
        self.currentSolution.checkFeasibility()
            # print("Pass Feasibility Check!")
        # print(self.currentSolution)
        print(f"Iteration Time: {cpuTimeIteration}")
        self.CPUTime = cpuTimeIteration
    
    def constructInitialSolution(self):
        """Construct the initial solution
        """
        # 1. based on Solomon's time-oriented Nearest Neighbur Heuristic 
        self.currentSolution = Solution(self.instance, list(), list(), self.instance.customers.copy())
        # self.currentSolution.executeTimeNN()
        # 2. based on each route per customer ...
        # self.currentSolution.executeNaive()
        # 3. based on C-W saving Heuristic (seems very efficient!)
        self.currentSolution.executeCWsaving(self.randomGen)


    def display(self, isbest = True):
        """Display the current Solution.

        Args:
            isbest (bool, optional): _description_. Defaults to True.
        """
        if isbest:
            print(self.bestSolution)
        else:
            print(self.currentSolution)
                
    
    def executeFleetMin(self, iterNum = 0):
        """Fleet Minimization Procedure: Remove entire route and 
        check if all customers it served can be inserted to other routes

        Args:
            iterNum (int, optional): Current Iteration Number. Defaults to 0.
        """
        # self.tempSolution = copy.deepcopy(self.currentSolution)
        self.tempSolution = self.currentSolution.copy()
        destroySolution = Destroy(self.instance, self.tempSolution)
        destroySolution.executeEntireRouteRemoval(self.randomGen)
        originalFleetSize = len(destroySolution.solution.routes)
        tempSolution2 = destroySolution.solution.copy() # This is very important! 
        repairSolution = Repair(self.instance, tempSolution2)
        repairSolution.executeMultiGreedyInsertion(self.randomGen)
        if len(repairSolution.solution.routes) <= originalFleetSize:
            self.currentSolution = repairSolution.solution
            print(f"Found Shorter Route!!! Obj: {repairSolution.solution.distance}, IterNum : {iterNum} , trucks: {len(repairSolution.solution.routes)} complete! ")

    
    def destroyAndRepair(self, destroyOptNo, repairOptNo, removaln):
        """To conduct a full Destroy and Repair Procedure ... 

        Args:
            destroyOptNo (_type_): _description_
            repairOptNo (_type_): _description_
            removaln (_type_): _description_

        Returns:
            _type_: _description_
        """
        # depict the destroy and repair process ... 
        self.tempSolution = copy.deepcopy(self.currentSolution)
        destroySolution = Destroy(self.instance, self.tempSolution)
        if destroyOptNo == 1:
            destroySolution.executeRandomRemoval(removaln, self.randomGen)
        elif destroyOptNo == 2:
            destroySolution.executeStringRemoval(self.avgCusRmved, self.maxStringLen, self.randomGen)
        elif destroyOptNo == 3:
            destroySolution.executeSplitStringRemoval(self.avgCusRmved, self.maxStringLen, self.randomGen)
            # strangly, this seems not that ... efficient ... ?? 
        
        tempSolution2 = destroySolution.solution.copy() # This is very important! 
        repairSolution = Repair(self.instance, tempSolution2)
        
        if repairOptNo == 1:
            repairSolution.executeMultiGreedyInsertion(self.randomGen)

        return repairSolution
    
    
    def ifAccept(self, repairSolution, iterNum = 0, chooseDestroy = 0, chooseRepair = 0):
        """check if this repaired solution should be accepted

        Args:
            repairSolution (Class Repair): the repaired solution.
            iterNum (int, optional): iteration number. Defaults to 0.
        """
        if self.currentSolution.distance - repairSolution.solution.distance >= 1e-3:
            if len(repairSolution.solution.routes) > len(self.currentSolution.routes):
                return
            self.currentSolution = repairSolution.solution
            print(f"Found!! Obj: {repairSolution.solution.distance}, IterNum : {iterNum} , trucks: {len(repairSolution.solution.routes)}, DesOpt: {chooseDestroy}, RepOpt: {chooseRepair},", end = " ")
            
            if self.instance.withBKS:
                print(f"Gap to BKS : { round((repairSolution.solution.distance - self.instance.BKSDistance) * 100 / self.instance.BKSDistance, 2)}%, BKS Trucks {self.instance.BKSTrucks}")
            else:
                print("")
                
    
    def returnBrief(self):
        """Reture Brief to mian function 
        """
        if self.instance.withBKS:
            return [self.currentSolution.distance, len(self.currentSolution.routes), self.CPUTime, round((self.currentSolution.distance - self.instance.BKSDistance) * 100 / self.instance.BKSDistance, 3),  self.instance.BKSTrucks]
        else:
            return [self.currentSolution.distance, len(self.currentSolution.routes), self.CPUTime]