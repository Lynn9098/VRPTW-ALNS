import random, time
from instance import Instance
from solution import Solution

class ALNS:
    """
    Class that models the ALNS algorithm. 

    Parameters
    ----------
    instance : Instance
        The problem instance that we want to solve.
    
    """

    def __init__(self, instance):
        self.problem = problem

    def execute(self):
        starttime = time.time()
        self.constructInitialSolution()
        endtime = time.time()
        cpuTime = round(endtime - starttime, 3)
        print(f"Terminated! Objective Function: {self.bestSolution.distance} \n CPU times {cpuTime} seconds")
    
    def constructInitialSolution(self):
        """Construct the initial solution
        """
        # 1. based on Solomon's time-oriented Nearest Neighbur Heuristic 
        self.currentSolution = Solution(self.problem, list(), list(), [self.problem.customers.copy()])
        self.currentSolution.executeTimeNN()
        # pass