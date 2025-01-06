import sys


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
        """

        self.forwardTimeSlack = [0 for _ in range(len(self.nodes))]
        n = len(self.nodes)
        for i in range(n - 1, -1, -1):
            if i == n - 1:
                self.forwardTimeSlack[i] = self.nodes[i].dueTime - (self.nodes[i - 1].serviceStartTime + self.nodes[i - 1].serviceTime + self.instance.distMatrix[self.nodes[i - 1].id][0])
            else:
                self.forwardTimeSlack[i] = min(self.forwardTimeSlack[i + 1] + self.nodes[i + 1].waitingTime, self.nodes[i].dueTime - self.nodes[i].serviceStartTime)

        for idx, node in enumerate(self.nodes):
            print(node)
            print(float(self.forwardTimeSlack[idx]))


    def isFeasible(self):
        """check if the route is feasible
        """
        # check if the route starts and ends at depot 
        if self.nodes[0] != self.instance.depot or self.nodes[-1] != self.instance.depot:
            return False
        curTime = 0 # record current time
        curLoad = 0 # record load in vehicle 
        for i in range(1, len(self.nodes)):
            preID, postID = self.nodes[i - 1].id, self.nodes[i].id
            curTime += self.instance.distMatrix[preID][postID]
            if curTime > self.nodes[i].dueTime:
                print("Break time window!!")
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
        self.adjustTW(customer)
        self.nodesSet.remove(customer)
        self.nodes.remove(customer)
    
    def adjustTW(self, customer):
        """An efficient way to adjust the start service timestamp, together with the distance of the route:
        following :https://mp.weixin.qq.com/s/rcnppKJLegzCirictTItFA

        Args:
            customer (_type_): _description_
        """
        rmvCusIdx = self.nodes.index(customer)
        prevIdx = rmvCusIdx - 1; postIdx = rmvCusIdx + 1
        # get the previous node and the post node
        postNode = self.nodes[postIdx]
        postServiceStartTime = postNode.serviceStartTime
        self.distance -= (self.instance.distMatrix[self.nodes[prevIdx].id][customer.id] + \
            self.instance.distMatrix[customer.id][self.nodes[postIdx].id] - self.instance.distMatrix[self.nodes[prevIdx].id][self.nodes[postIdx].id])
        
        if postServiceStartTime == postNode.readyTime:
            # No need to adjust the time windows
            print("No need to adjust!")
            return
        else:
            # need to adjust the service time of nodes afterwards ... 
            for j in range(rmvCusIdx + 1, len(self.nodes) - 1):
                curServiceStartTime = self.nodes[prevIdx].serviceStartTime + \
                    self.instance.distMatrix[self.nodes[prevIdx].id][self.nodes[j].id] + \
                    self.nodes[prevIdx].serviceTime
                # print(self.nodes[j])
                self.nodesSet.remove(self.nodes[j])
                self.nodes[j].serviceStartTime = max(curServiceStartTime, self.nodes[j].readyTime)
                self.nodesSet.add(self.nodes[j])
                prevIdx = j
        return 
    
    def greedyInsert(self, customer):
        """Greedy insert the customer into this route .. 

        Args:
            customer (node): node of customers ...
        """
        nodesSetCopy = self.nodesSet.copy()
        nodesSetCopy.add(customer)
        minDist = sys.maxsize
        bestInsert = None # record the best insertion result ...
        minCost = sys.maxsize 
        
        # iterate over all possible locations for insertion ... 
        # for i in range(1, len(self.nodes)):
        # according to bi-search of Time Windows
            
            
        pass
        
    
    def copy(self):
        nodesCopy = self.nodes.copy()
        nodesSetCopy = self.nodesSet.copy()
        return Route(self.instance, nodesCopy, nodesSetCopy)
    
