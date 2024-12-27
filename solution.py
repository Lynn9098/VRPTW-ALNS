from route import Route
import operator
class Solution:
    
    def __init__(self, instance, routes, served, notServed):
        self.instance = instance
        self.routes = routes
        self.served = served
        self.notServed = notServed
        self.distance = self.computeDistance
    
    def computeDistance(self):
        self.distance = 0
        for route in self.routes:
            self.distance += route.distance
        return self.distance
    
    def executeTimeNN(self):
        """Time-oriented NN in Solomon 1987
        """
        sigma_1, sigma_2, sigma_3 = 1/3, 1/3, 1/3
        # determine the weight
        lastCusIdx = 0
        if len(self.served) == 0:
            # if have no route ... 
            # need to compare with the depot, choose the 'closest' one
            
            closeDist = []
            for nextCus in self.notServed:
                closeDist.append(sigma_1 * self.instance.distMatrix[0][nextCus.id] + 
                                 sigma_2 * self.instance.readyTime[nextCus.id] + 
                                 sigma_3 * (self.instance.dueTime[nextCus.id] - self.instance.distMatrix[0][nextCus.id]))
            
            # find the minimum index of closeDist
            min_index, min_value = min(enumerate(closeDist), key = operator.itemgetter(1))
            # put this into a new route
            nodeList = [self.instance.depot, self.notServed[min_index], self.instance.depot]
            newRoute = Route(self.instance, nodeList, set(nodeList))
            self.served.append(notServed[min_index])
            self.notServed.pop(min_index)
            self.routes.append(newRoute)
            # last
            # update served customers / not-served customers
            # update routes of current solution
        else:
            # have existing customers, which means existing routes
            # check every route and find the cloest customer
            closeDist = float('inf')
            closeRoute = -1
            # store the close distance and target route ... 
            for nextCus in self.notServed:
                # for those unServed:
                for route in self.routes:
                    # for every route
                    lastCus = route[-2]
                    # find the last customer in the route
                    # check if the customer can be visited
                    # TODO here.
                
            
    
    def copy(self):
        """
        Method that creates a copy of the solution and returns it
        """
        # need a deep copy of routes because routes are modifiable
        routesCopy = list()
        for route in self.routes:
            routesCopy.append(route.copy())
        newCopy = Solution(self.instance, routesCopy)
        newCopy.computeDistance()
        return newCopy
