import sys
from route import Route
class Repair:
    
    def __init__(self, instance, solution):
        self.instance = instance
        self.solution = solution 
    
    def executeGreedyInsertion(self, randomGen):

        while len(self.solution.notServed) > 0:
            
            cus = randomGen.choice(self.solution.notServed)
            # random select the customer ... 
            curMinIncrement = sys.maxsize
            curBestRoute = None 
            curBestRouteIdx = None
            
            for idx, potentialRoute in enumerate(self.solution.routes):

                afterInsert, costIncrement = potentialRoute.greedyInsert(cus)
                if randomGen.random() < 0.99:
                    if afterInsert:
                        if costIncrement < curMinIncrement:
                            curMinIncrement = costIncrement
                            curBestRoute = afterInsert
                            curBestRouteIdx = idx

            if curBestRoute == None:
                # means cannot find a way to insert ... 
                nodeList = [self.instance.depot, cus, self.instance.depot]
                newRoute = Route(self.instance, nodeList, set(nodeList))
                self.solution.routes.append(newRoute)
                self.solution.distance += (self.instance.distMatrix[0][cus.id] + self.instance.distMatrix[cus.id][0])
            else:
                self.solution.routes[curBestRouteIdx] = Route(self.instance, curBestRoute, set(curBestRoute))
                self.solution.distance += curMinIncrement

            self.solution.notServed.remove(cus)
            self.solution.served.append(cus)


# if __name__ == "__main__":
