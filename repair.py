import sys
from route import Route
class Repair:
    
    def __init__(self, instance, solution):
        self.instance = instance
        self.solution = solution 
    
    def executeGreedyInsertion(self, randomGen):
        # for node in self.solution.routes[0].nodes:
        #     print("CHEK SEC ", end = " ")
        #     print(node)
        # print(self.solution.routes[0].forwardTimeSlack)
        
        while len(self.solution.notServed) > 0:

            cus = randomGen.choice(self.solution.notServed)

            # random select the customer ... 
            curMinIncrement = sys.maxsize
            curBestRoute = None
            curBestRouteIdx = None
            
            for idx, potentialRoute in enumerate(self.solution.routes):
                # if idx == 3:
                #     print("MAIN CHECK")
                #     for node in potentialRoute.nodes:
                #         print(node)
                afterInsert, costIncrement = potentialRoute.greedyInsert(cus)
                if randomGen.random() < 0.99:
                    if afterInsert:
                        if costIncrement < curMinIncrement:
                            curMinIncrement = costIncrement
                            curBestRoute = afterInsert
                            curBestRouteIdx = idx

            if curBestRoute == None:
                # means cannot find a way to insert ... 
                print(f"Need to forge New route")
                tempCustomer = cus
                tempCustomer.serviceStartTime = max(cus.readyTime, self.instance.distMatrix[0][cus.id])
                tempCustomer.waitingTime = max(0, cus.readyTime - (self.instance.distMatrix[0][cus.id]))
                nodeList = [self.instance.depot, tempCustomer, self.instance.depot]
                newRoute = Route(self.instance, nodeList, set(nodeList))
                newRoute.adjustTW(1)
                newRoute.forgePushForward()
                self.solution.routes.append(newRoute)
                # print(f"Forge new, cus {cus.id}")
            else:
                # print(f"Process cus {cus.id} ...")
                self.solution.routes[curBestRouteIdx] = curBestRoute
            
            self.solution.notServed.remove(cus)
            self.solution.served.append(cus)
        print(self.solution)
            
            

# if __name__ == "__main__":
