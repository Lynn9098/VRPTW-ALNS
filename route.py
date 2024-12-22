import sys

class Route:
    def __init__(self, instance, nodes, feasible):
        self.instance = instance
        self.nodes = nodes
        self.feasible = feasible
        self.distance = 0
        
    
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
                # check time window
                return False
            curTime = max(curTime, self.nodes[i].readyTime) + self.nodes[i].serviceTime
            curLoad += self.nodes[i].demand
            if curLoad > self.instance.capacity:
                # check capacity constraint
                return False
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
        return round(totalDist, 2)
            