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
    
    def executeStringRemoval(self, avgCusRmvd, maxStringLen, randomGen):
        """_summary_

        Args:
            avgCusRmvd (_type_): _description_
            maxStringLen (_type_): _description_
            randomGen (_type_): _description_
        """
        routeNodes = [len(route.nodes) - 2 for route in self.solution.routes]
        avgNodesPerRoute = sum(routeNodes) // len(self.solution.routes)
        # record average number of nodes per route
        l_max_s = min(maxStringLen, avgNodesPerRoute)
        # max string length. cannot totally remove a route ?
        k_max_s = (4 * avgCusRmvd) / (1 + l_max_s) - 1
        # print(f"k_max_s {k_max_s}", end = " ")
        # the maximum number of strings
        k_s = int(randomGen.uniform(1, k_max_s + 1))
        # the number of strings to be removed for this solution ... 
        cus_seed = randomGen.choice(self.solution.served)
        cusSeedId = cus_seed.id
        # find the seed customer where the string removal begins
        visitedCusId = [-1 for _ in range(self.instance.numNodes)]
        # to restore deleted customers id that have been removed ...
        cusEnRouteList = [-1 for _ in range(self.instance.numNodes)]
        enRouteCusDict = dict()
        enRouteCusSeqDict = dict()
        # record the following: 
        # 1. the route of each customer,  
        # 2. the customers each route served ... 
        # 3. the sequence of customers each route served ...
        for idx, route in enumerate(self.solution.routes):
            enRouteCusDict[idx] = []
            enRouteCusSeqDict[idx] = []
            for node in route.nodes:
                if node.id != 0:
                    cusEnRouteList[node.id] = idx
                    enRouteCusDict[idx].append(node.id)
                enRouteCusSeqDict[idx].append(node.id)
        
        for nodeId in enRouteCusDict[cusEnRouteList[cusSeedId]]:
            visitedCusId[nodeId] = 1
        visitedCusId[0] = 1
            # keep track of visited customers ... 
        
        entireRouteRemoval = [] # record routes that are entirely removed ... 
        for i in range(k_s):
            # need to remove k_s routes ... 
            for customer_id in self.instance.adjDistMatrix[cusSeedId]:
                # iterate over all nodes ... 
                if visitedCusId[customer_id] == 1 or customer_id == 0:
                    # if the customer has been visited, or if the customer is depot, skip it ... 
                    continue
                else:
                    # if the customer has not been visited, add it to the visited list ... 
                    # this tour is the next string ... 
                    # determine the l_max_t, l_t (removed string length)
                    routeIdx = cusEnRouteList[customer_id]
                    l_max_t = min(len(enRouteCusDict[routeIdx]), l_max_s)
                    l_t = int(randomGen.uniform(1, l_max_t))
                    
                    curRoute = enRouteCusSeqDict[routeIdx]
                    # print(curRoute, l_t, routeIdx)
                    rmvdIdxes = self.chooseCusViaString(customer_id, enRouteCusSeqDict[routeIdx], l_t, randomGen)
                    if len(rmvdIdxes) == len(curRoute):
                        # The route is actually entirely removed ... 
                        entireRouteRemoval.append(routeIdx)
                    self.solution.removeRouteString(routeIdx, rmvdIdxes)
                    for sameRouteCusId in enRouteCusDict[routeIdx]:
                        visitedCusId[sameRouteCusId] = 1
                    # print(f"Current Visited Cus ID : {visitedCusId}")
                    cusSeedId = customer_id
                    break
        
        if len(entireRouteRemoval) > 0:
            sorted(entireRouteRemoval)
            for routeIdx in entireRouteRemoval[::-1]:
                # backward update to avoid index conflict ... 
                self.solution.routes.pop(routeIdx)
            
        
    def executeSplitStringRemoval(self, avgCusRmvd, maxStringLen, randomGen):
        routeNodes = [len(route.nodes) - 2 for route in self.solution.routes]
        avgNodesPerRoute = sum(routeNodes) // len(self.solution.routes)
        # record average number of nodes per route
        l_max_s = min(maxStringLen, avgNodesPerRoute)
        # max string length. cannot totally remove a route ?
        k_max_s = (4 * avgCusRmvd) / (1 + l_max_s) - 1
        # print(f"k_max_s {k_max_s}", end = " ")
        # the maximum number of strings
        k_s = int(randomGen.uniform(1, k_max_s + 1))
        # the number of strings to be removed for this solution ... 
        cus_seed = randomGen.choice(self.solution.served)
        cusSeedId = cus_seed.id
        # find the seed customer where the string removal begins
        visitedCusId = [-1 for _ in range(self.instance.numNodes)]
        # to restore deleted customers id that have been removed ...
        cusEnRouteList = [-1 for _ in range(self.instance.numNodes)]
        enRouteCusDict = dict()
        enRouteCusSeqDict = dict()
        # record the following: 
        # 1. the route of each customer,  
        # 2. the customers each route served ... 
        # 3. the sequence of customers each route served ...
        for idx, route in enumerate(self.solution.routes):
            enRouteCusDict[idx] = []
            enRouteCusSeqDict[idx] = []
            for node in route.nodes:
                if node.id != 0:
                    cusEnRouteList[node.id] = idx
                    enRouteCusDict[idx].append(node.id)
                enRouteCusSeqDict[idx].append(node.id)
        
        for nodeId in enRouteCusDict[cusEnRouteList[cusSeedId]]:
            visitedCusId[nodeId] = 1
        visitedCusId[0] = 1
        entireRouteRemoval = []
        for i in range(k_s):
            for customer_id in self.instance.adjDistMatrix[cusSeedId]:
                # print(f"Customer_id : {customer_id}")
                if visitedCusId[customer_id] == 1 or customer_id == 0:
                    # if the customer has been visited, or if the customer is depot, skip it ... 
                    continue
                else:
                    curRouteLen = len(enRouteCusDict[cusEnRouteList[customer_id]])
                    l_max_t = min(curRouteLen, l_max_s)
                    l_t = int(randomGen.uniform(1, l_max_t))
                    # decide if the remove is head-tail
                    augRmv = 1
                    if l_t != curRouteLen:
                        while l_t + augRmv < curRouteLen:
                            if randomGen.random() > 0.99:
                                break
                            augRmv += 1
                        if augRmv + l_t == curRouteLen:
                            # Head Tail removal ... only keeps augRmv Nodes which include customer seed 
                            routeIdx = cusEnRouteList[customer_id]
                            keptIdxes = self.chooseCusViaString(customer_id, enRouteCusSeqDict[routeIdx], augRmv , randomGen)
                            # since delete tail & head, current string is kept!
                            self.solution.keepRouteString(routeIdx, keptIdxes)
                            for sameRouteCusId in enRouteCusDict[routeIdx]:
                                visitedCusId[sameRouteCusId] = 1
                        else:
                            # remove l_t yet skip several node .. 
                            routeIdx = cusEnRouteList[customer_id]
                            rmvdIdxes = self.chooseCusViaStringSplit(customer_id, enRouteCusSeqDict[routeIdx], l_t + augRmv, augRmv, randomGen)
                            self.solution.removeRouteString(routeIdx, rmvdIdxes)
                            for sameRouteCusId in enRouteCusDict[routeIdx]:
                                visitedCusId[sameRouteCusId] = 1
                    else:
                        routeIdx = cusEnRouteList[customer_id]
                        l_max_t = min(len(enRouteCusDict[routeIdx]), l_max_s)
                        l_t = int(randomGen.uniform(1, l_max_t))
                        curRoute = enRouteCusSeqDict[routeIdx]
                        rmvdIdxes = self.chooseCusViaString(customer_id, enRouteCusSeqDict[routeIdx], l_t, randomGen)
                        if len(rmvdIdxes) == len(curRoute):
                            # The route is actually entirely removed ... 
                            entireRouteRemoval.append(routeIdx)
                        self.solution.removeRouteString(routeIdx, rmvdIdxes)
                        for sameRouteCusId in enRouteCusDict[routeIdx]:
                            visitedCusId[sameRouteCusId] = 1
                    cusSeedId = customer_id

        pass
    
    def executeRemoveByIndex(self, routeIdx, rmvdIdxes):
        """Remove customer by their index in route[routeIdx]

        Args:
            routeIdx (_type_): _description_
            rmvdIdxes (_type_): _description_
        """
        self.solution.removeRouteString(routeIdx, rmvdIdxes)
        
    
    def chooseCusViaString(self, cusId, cusSeq, rmvLen, randomGen):
        """Given cus seq, targeted_cus_id, choose cus via string, return a list of cus index

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
        if len(validSubLists) > 0:
            return randomGen.choice(validSubLists)
        else:
            return []
    
    def chooseCusViaStringSplit(self, cusId, cusSeq, rmvLen, keptLen, randomGen):
        """

        Args:
            cusId (_type_): _description_
            cusSeq (_type_): _description_
            rmvLen (_type_): _description_
            randomGen (_type_): _description_
        """
        validSubLists = []
        for i in range(len(cusSeq) - rmvLen + 1):
            cusIdList = cusSeq[i: i + rmvLen]
            if cusId in cusIdList and 0 not in cusIdList:
                # check if the string satisfy ... 
                validSubLists.append([k for k in range(i, i + rmvLen)])
        tempValidList = randomGen.choice(validSubLists)
        cnt = 0
        while cnt < keptLen:
            idx = randomGen.randint(0, len(tempValidList) - 1)
            if tempValidList[idx] != cusId:
                tempValidList.pop(idx)
                cnt += 1
        return tempValidList
    
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
        # self.solution.distance = self.solution.computeDistance()


    def __str__(self):
        return str(self.solution)