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
        pass
    
    