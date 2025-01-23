import sys
import copy

class Route:
    def __init__(self, instance, nodes, nodesSet):
        """_summary_

        Args:
            instance (Instance): current instance
            nodes (list[Node]): the sequence of visiting
            nodesSet (set(Node)): restore set of customers index of the route
        """
        self.instance = instance
        self.nodes = nodes
        self.nodesSet = nodesSet
        self.feasible = self.isFeasible()
        if self.feasible:
            # 事先check路径是否可行
            self.distance = self.computeDistance()
        else:
            self.distance = sys.maxsize
            self.load = sys.maxsize

    def forgePushForward(self):
        """construct and rectify push forward procedure ... 
            details: 
            The Vehicle Routing Problem with Time Windows: Minimizing Route Duration by Martin W. P. Savelsbergh, 1992
        """
        self.forwardTimeSlack = [0 for _ in range(len(self.nodes))]
        n = len(self.nodes)
        for i in range(n - 1, -1, -1):
            if i == n - 1:
                self.forwardTimeSlack[i] = self.nodes[i].dueTime - (self.nodes[i - 1].serviceStartTime + self.nodes[i - 1].serviceTime + self.instance.distMatrix[self.nodes[i - 1].id][0])
            else:
                self.forwardTimeSlack[i] = min(self.forwardTimeSlack[i + 1] + self.nodes[i + 1].waitingTime, self.nodes[i].dueTime - self.nodes[i].serviceStartTime)

    def isFeasible(self):
        """check if the route is feasible
        """
        # check if the route starts and ends at depot 
        if self.nodes[0].id != 0 or self.nodes[-1].id != 0:
            print("Head & Tail")
            return False
        curTime = 0 # record current time
        curLoad = 0 # record load in vehicle 
        for i in range(1, len(self.nodes)):
            preID, postID = self.nodes[i - 1].id, self.nodes[i].id
            curTime += self.instance.distMatrix[preID][postID]
            if curTime > self.nodes[i].dueTime:
                print(f"Cus {self.nodes[i].id} Break time window!!, {len(self.nodes)}")
                for node in self.nodes:
                    print(node)
                return False
            curTime = max(curTime, self.nodes[i].readyTime) + self.nodes[i].serviceTime
            curLoad += self.nodes[i].demand
            if curLoad > self.instance.capacity:
                # check capacity constraint
                print("Break capacity capacity!!")
                return False
        self.load = curLoad
        return True
    
    def computeDistance(self):
        """calculate total distance of the route

        Returns:
            _type_: _description_
        """
        totalDist = 0
        for i in range(1, len(self.nodes)):
            prevID, postID = self.nodes[i - 1].id, self.nodes[i].id
            totalDist += self.instance.distMatrix[prevID][postID]
        return totalDist
    
    def calculateServiceStartTime(self):
        """calculate the begin of service time for each customer of this route
        """
        curTime = 0
        for i in range(1, len(self.nodes) - 1):
            prevNode = self.nodes[i - 1]
            curNode = self.nodes[i]
            dist = self.instance.distMatrix[prevNode.id][curNode.id]
            curTime = max(curNode.readyTime, curTime + prevNode.serviceTime + dist)
            self.nodes[i].serviceStartTime = curTime
    
    def removeCustomer(self, customer):
        if customer not in self.nodesSet:
            print("WARNING! Trying to remove a non-existing customer!")
            return

        del_cus_idx = self.nodes.index(customer)
        self.nodesSet.remove(customer)
        self.nodes.pop(del_cus_idx)
        
        for j in range(del_cus_idx, len(self.nodes) - 1):
            prevNode = self.nodes[j - 1]
            curArrivalTime = self.nodes[j - 1].serviceStartTime + \
                self.instance.distMatrix[self.nodes[j - 1].id][self.nodes[j].id] + \
                self.nodes[j - 1].serviceTime
            self.nodesSet.remove(self.nodes[j])
            self.nodes[j].serviceStartTime = max(curArrivalTime, self.nodes[j].readyTime)
            # print(f"{j} {self.nodes[j].serviceStartTime}")
            self.nodes[j].waitingTime = max(0, self.nodes[j].readyTime - (self.instance.distMatrix[prevNode.id][self.nodes[j].id] + prevNode.serviceStartTime + prevNode.serviceTime))
            self.nodesSet.add(self.nodes[j])
    
    def adjustTW(self, index):
        """adjust time windows afterwards

        Args:
            index (_type_): _description_
        """
        prevNode = self.nodes[index - 1]
        currNode = self.nodes[index]
        succNode = self.nodes[index + 1]
        self.distance -= (
            self.instance.distMatrix[prevNode.id][currNode.id] + self.instance.distMatrix[currNode.id][succNode.id] - \
            self.instance.distMatrix[prevNode.id][succNode.id])
        for i in range(index, len(self.nodes) - 1):
            prevNode = self.nodes[i - 1]
            currNode = self.nodes[i]
            curArrivalTime = prevNode.serviceStartTime + self.instance.distMatrix[prevNode.id][currNode.id] + prevNode.serviceTime
            self.nodesSet.remove(self.nodes[i])
            self.nodes[i].serviceStartTime = max(curArrivalTime, self.nodes[i].readyTime)
            self.nodes[i].waitingTime = max(0, currNode.readyTime - (self.instance.distMatrix[prevNode.id][currNode.id] + prevNode.serviceStartTime + prevNode.serviceTime))
            self.nodesSet.add(self.nodes[i])
            
        return
    
    def greedyInsert(self, customer):
        """Greedily insert the customer into this route .. 

        Args:
            customer (node): node of customers ...
        """
        nodesSetCopy = self.nodesSet
        nodesSetCopy.add(customer)
        bestInsert = None # record the best insertion result ...
        bestInsertIdx = None
        minCost = sys.maxsize 
        
        # iterate over all possible locations for insertion ... 
        # if customer.id == 13:
        #     print("SECOND CHECK")
        #     # [129.0, 79, 57, 44.88275723137633, 44.88275723137633, 105.67338451907767]
        #     for node in self.nodes:
        #         print(node)
        for i in range(1, len(self.nodes)):
            prevNode = self.nodes[i - 1]
            succNode = self.nodes[i]
            newServiceStartTime = max(customer.readyTime,  prevNode.serviceStartTime + prevNode.serviceTime + self.instance.distMatrix[prevNode.id][customer.id])
            # if self.nodes[1].id == 24 and customer.id == 73:
            #     print(f"EHRE {i}")
            #     for k in self.nodes:
            #         print(k)
            if newServiceStartTime > customer.dueTime or \
                newServiceStartTime + customer.serviceTime + self.instance.distMatrix[customer.id][succNode.id] - self.nodes[i].serviceStartTime >  self.forwardTimeSlack[i] \
                or customer.demand + self.load > self.instance.capacity:
                continue

            costIncrement = self.instance.distMatrix[prevNode.id][customer.id] + self.instance.distMatrix[customer.id][succNode.id]

            if costIncrement < minCost:
                minCost = costIncrement
                tempCus = copy.deepcopy(customer)
                tempCus.serviceStartTime = newServiceStartTime
                tempCus.waitingTime = max(0, tempCus.readyTime - newServiceStartTime)
                routeCopy = copy.deepcopy(self.nodes) # VERY IMPORTANT
                routeCopy.insert(i, tempCus)
                bestInsert = routeCopy
                bestInsertIdx = i

            
        if bestInsert is not None:
            bestRoute = Route(self.instance, bestInsert, set(bestInsert))
            bestRoute.adjustTW(bestInsertIdx)
            bestRoute.forgePushForward()
            # if customer.id == 71:
            #     print("I GUESS THIS IS FAILED!")
            #     # print(bestInsert)
            #     for node in bestInsert:
            #         print(node)
            return bestRoute, minCost
        else:
            return None, minCost
        
    
    def copy(self):
        nodesCopy = self.nodes.copy()
        nodesSetCopy = self.nodesSet.copy()
        nodesForwardTimeSlackCopy = self.forwardTimeSlack.copy()
        newRoute = Route(self.instance, nodesCopy, nodesSetCopy)
        newRoute.forwardTimeSlack = nodesForwardTimeSlackCopy
        return newRoute
    
