from instance import Instance

class Destroy:
    '''
    Class that represents destroy methods

    Parameters
    ----------
    instance : VRPTW
        The problem instance that we want to solve.
    solution : Solution
        The current solution in the ALNS algorithm
    '''

    def __init__(self, instance, solution):
        self.instance = instance
        self.solution = solution
    
    def executeRandomRemoval(self, nRemoval, randomGen):
        """Random removal operator
        """
        for _ in range(nRemoval):
            if len(self.solution.served) == 0:
                break
            cus = randomGen.choice(self.solution.served)
            if cus != None:
                self.solution.removeCustomer(cus)
        self.solution.distance = self.solution.computeDistance()
    
    def executeStringRemoval(self, nRemoval, randomGen):
        """_summary_

        Args:
            nRemoval (_type_): _description_
            randomGen (_type_): _description_
        """
        pass
    
    def executeShawRemoval(self, nRemoval, randomGen):
        """Shaw removal

        Args:
            nRemoval (_type_): number of removed customers
            randomGen (_type_): random generator
        """
        # targetCus = randomGen.choice(self.solution.served)
        # self.solution.notServed.append(targetCus)
        # calculate shaw relatedness ... 
        timeWindowRelateness = [0 for _ in range(self.instance.numNodes - 1)]
        loadRelateness = [0 for _ in range(self.instance.numNodes - 1)]
        distanceRelateness = [0 for _ in range(self.instance.numNodes - 1 )]
        
        pass
    
    def executeEntireRouteRemoval(self, randomGen):
        """Remove entire route for fleet minimization ... 

        Args:
            randomGen (_type_): _description_
        """
        
        rmvdRouteIdx = randomGen.randint(0, len(self.solution.routes) - 1)
        # choose the route index to be removed 
        self.solution.removeRoute(rmvdRouteIdx)
        self.solution.distance = self.solution.computeDistance()


    def __str__(self):
        return str(self.solution)