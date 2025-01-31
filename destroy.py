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
    
    def executeWorseRemoval(self, nRemoval, randomGen):
        """Worse case removal ... 

        Args:
            nRemoval (_type_): _description_
            randomGen (_type_): _description_
        """
        pass
    
    def executeStringRemoval(self, nRemoval, avgCusRmvd, maxStringLen, randomGen):
        """_summary_

        Args:
            nRemoval (_type_): _description_
            randomGen (_type_): _description_
        """
        routeNodes = [len(route.nodes) - 2 for route in self.solution.routes]
        avgNodesPerRoute = sum(routeNodes) // len(self.solution.routes)
        # record average number of nodes per route
        maxNodesOfRoute = max(routeNodes)
        # record maximum number of nodes served by a route
        l_max_s = min(maxStringLen, avgNodesPerRoute)
        # max string length. cannot totally remove a route ?
        k_max_s = (4 * avgCusRmvd) / (1 + l_max_s) - 1
        # the maximum number of strings
        k_s = int(randomGen.uniform(1, k_max_s + 1))
        # the number of strings to be removed for this solution ... 
        cus_seed = randomGen.choice(self.solution.served)
        # find the seed customer where the string removal begins
        visitedCusId = set()
        # to restore deleted customers id that have been removed ...
        cusEnRouteList = [-1 for _ in range(self.instance.numNodes)]
        enRouteCusDict = dict()
        enRouteCusSeqDict = dict()
        # record the following: 
        # 1. the route of each customer,  
        # 2. the customers each route served ... 
        # 3. the sequence of customers each route served ...
        for idx, route in enumerate(self.instance.routes):
            enRouteCusDict[idx] = []
            enRouteCusSeqDict[idx] = []
            for node in route.nodes:
                if node.id != 0:
                    cusEnRouteList[node.id] = idx
                    enRouteCusDict[idx].append(node.id)
                enRouteCusSeqDict[idx].append(node.id)
        
        for nodeId in enRouteCusDict[cusEnRouteList[cus_seed.id]]:
            visitedCusId.add(nodeId)
            # keep track of visited customers ... 
        
        for i in range(k_s):
            # need to remove k_s routes ... 
            for customer_id in self.instance.adjDistMatrix[cus_seed.id]:
                # iterate over all nodes ... 
                if customer_id in visitedCusId:
                    # if the customer has been visited, skip it ... 
                    continue
                else:
                    # if the customer has not been visited, add it to the visited list ... 
                    # this tour is the next string ... 
                    # determine the l_max_t, l_t (removed string length)
                    l_max_t = min(len(enRouteCusDict[cusEnRouteList[cus_seed.id]]), l_max_s)
                    l_t = int(randomGen.uniform(1, l_max_t + 1))
                pass
            pass
        
        
        pass
    
    def chooseCusViaString(self, cusId, cusSeq, rmvLen, randomGen):
        """Given cus seq, targeted_cus_id, choose cus via string

        Args:
            cusId (_type_): _description_
            cusSeq (_type_): _description_
            randomGen (_type_): random generator
        """
        
        validSubLists = []
        for i in range(len(cusSeq) - rmvLen + 1):
            cusIdList = cusSeq[i: i + rmvLen]
            if cusId in cusIdList and 0 not in cusIdList:
                # check if the string satisfy ... 
                validSubLists.append([k for k in range(i, i + rmvLen)])
            # pass
        if len(validSubLists) > 0:
            return randomGen.choice(validSubLists)
        else:
            return []
        
    
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