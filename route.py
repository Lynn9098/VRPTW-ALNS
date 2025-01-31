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
            # check if route is feasible, and if yes, then formulate the distance with the serviceStartTime List
            self.distance = self.computeDistance()
            self.calculateTime()
            self.forgePushForward()
        else:
            self.distance = sys.maxsize
            self.load = sys.maxsize
            self.serviceStartTime = [-1 for _ in range(len(self.nodes))]

    def forgePushForward(self):
        """construct and rectify push forward procedure ... 
            details: 
            The Vehicle Routing Problem with Time Windows: Minimizing Route Duration by Martin W. P. Savelsbergh, 1992
        """
        # self.calculateTime()
        
        self.forwardTimeSlack = [0 for _ in range(len(self.nodes))]
        # we declare the push forward procedure of this route here!
        n = len(self.nodes)
        for i in range(n - 1, -1, -1):
            # from back to front
            if i == n - 1:
                self.forwardTimeSlack[i] = self.nodes[i].dueTime - (self.serviceStartTime[i - 1] + self.nodes[i - 1].serviceTime + self.instance.distMatrix[self.nodes[i - 1].id][0])
            else:
                self.forwardTimeSlack[i] = min(self.forwardTimeSlack[i + 1] + self.waitingTime[i + 1], self.nodes[i].dueTime - self.serviceStartTime[i])
        # self.nodesSet = set(self.nodes)

    def isFeasible(self):
        """check if the route is feasible
        """
        # check if the route starts and ends at depot 
        if self.nodes[0].id != 0 or self.nodes[-1].id != 0:
            print("FAIL: Head or Tail is not depot!")
            return False
        curTime = 0 # record current time
        curLoad = 0 # record load in vehicle 
        for i in range(1, len(self.nodes)):
            preID, postID = self.nodes[i - 1].id, self.nodes[i].id
            curTime += self.instance.distMatrix[preID][postID]
            if curTime > self.nodes[i].dueTime:
                # check timewindow
                print(f"FAIL: Cus {self.nodes[i].id} Break time window!!, {len(self.nodes)}, display it:")
                for node in self.nodes:
                    print(node)
                return False
            curTime = max(curTime, self.nodes[i].readyTime) + self.nodes[i].serviceTime
            curLoad += self.nodes[i].demand
            if curLoad > self.instance.capacity:
                # check capacity constraint
                print("FAIL: Break capacity capacity!!")
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
    
    def calculateTime(self):
        """calculate the begin of service time for each node of this route
        """
        self.serviceStartTime = [0 for _ in range(len(self.nodes))]
        self.waitingTime = [0 for _ in range(len(self.nodes))]
        # we declare the service start time of this route here!
        serviceStartTime = 0
        for i in range(1, len(self.nodes) - 1):
            prevNode = self.nodes[i - 1]
            curNode = self.nodes[i]
            dist = self.instance.distMatrix[prevNode.id][curNode.id]
            actualArrivalTime = serviceStartTime + prevNode.serviceTime + dist
            serviceStartTime = max(curNode.readyTime, actualArrivalTime)
            self.serviceStartTime[i] = serviceStartTime
            self.waitingTime[i] = max(0, self.nodes[i].readyTime - actualArrivalTime)
    
    def removeCustomer(self, customer):
        if customer not in self.nodesSet:
            print("FAIL! Trying to remove a non-exist customer!")
            return
        
        # if customer not in self.nodes:
        #     print(f"Customer : {str(customer)}")
        #     for node in self.nodes:
        #         print(node)
        #     print("===")
        #     for node in self.nodesSet:
        #         print(node)
        
        del_cus_idx = self.nodes.index(customer)
        prevNode = self.nodes[del_cus_idx - 1]
        succNode = self.nodes[del_cus_idx + 1]
        self.nodesSet.remove(customer)
        self.nodes.pop(del_cus_idx)
        self.serviceStartTime.pop(del_cus_idx)
        self.waitingTime.pop(del_cus_idx)
        self.distance -= (self.instance.distMatrix[prevNode.id][customer.id] + self.instance.distMatrix[customer.id][succNode.id] - self.instance.distMatrix[prevNode.id][succNode.id] )
        for j in range(del_cus_idx, len(self.nodes) - 1):
            prevNode = self.nodes[j - 1]
            currNode = self.nodes[j]
            curArrivalTime = self.serviceStartTime[j - 1] + self.instance.distMatrix[prevNode.id][currNode.id] + prevNode.serviceTime
            self.serviceStartTime[j] = max(curArrivalTime, currNode.readyTime) 
            self.waitingTime[j] = max(0, currNode.readyTime - curArrivalTime)
        self.forgePushForward()
    
    
    def greedyInsert(self, customer):
        """Greedily insert the customer into this route .. 

        Args:
            customer (node): node of customers ...
        """
        
        bestInsert = None # record the best insertion result ...
        minCost = sys.maxsize 
        
        for i in range(1, len(self.nodes)):
            prevNode = self.nodes[i - 1]
            succNode = self.nodes[i]
            newServiceStartTime = max(customer.readyTime,  self.serviceStartTime[i - 1] + prevNode.serviceTime + self.instance.distMatrix[prevNode.id][customer.id])
            if newServiceStartTime > customer.dueTime  \
                or customer.demand + self.load > self.instance.capacity  \
                or newServiceStartTime + customer.serviceTime + self.instance.distMatrix[customer.id][succNode.id] - self.serviceStartTime[i] >  self.forwardTimeSlack[i]:
                continue
            costIncrement = self.instance.distMatrix[prevNode.id][customer.id] + self.instance.distMatrix[customer.id][succNode.id] - self.instance.distMatrix[prevNode.id][succNode.id]

            if costIncrement < minCost:
                minCost = costIncrement
                tempRoute = self.nodes.copy()
                tempRoute.insert(i, customer) # VERY IMPORTANT
                bestInsert = tempRoute.copy()

        if bestInsert is not None:
            return bestInsert, minCost
        else:
            return None, minCost
        
    
    def copy(self):
        nodesCopy = self.nodes.copy()
        nodesSetCopy = self.nodesSet.copy()
        nodesForwardTimeSlackCopy = self.forwardTimeSlack.copy()
        newRoute = Route(self.instance, nodesCopy, nodesSetCopy)
        newRoute.forwardTimeSlack = nodesForwardTimeSlackCopy
        return newRoute
    
