from instance import Instance

class Destroy:
    '''
    Class that represents destroy methods

    Parameters
    ----------
    instance : PDPTW
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
        for i in range(nRemoval):
            if len(self.solution.served) == 0:
                break
            cus = randomGen.choice(self.solution.served)
            if cus != None:
                self.solution.removeCustomer(cus)
        
    
    def __str__(self):
        return str(self.solution)