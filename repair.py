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
            curBestRouteIdx = -1
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
                print(f"Insert cus {cus.id} to route {curBestRouteIdx}")
                cus.serviceStartTime = max(cus.readyTime, self.instance.distMatrix[0][cus.id])
                cus.waitingTime = max(0, cus.readyTime - (self.instance.distMatrix[0][cus.id]))
                nodeList = [self.instance.depot, cus, self.instance.depot]
                newRoute = Route(self.instance, nodeList, set([cus]))
                newRoute.adjustTW(cus)
                newRoute.forgePushForward()
                self.solution.routes.append(newRoute)
            else:
                self.solution.routes[curBestRouteIdx] = curBestRoute
            self.solution.notServed.remove(cus)
            self.solution.served.add(cus)

        print(self.solution)

# if __name__ == "__main__":
