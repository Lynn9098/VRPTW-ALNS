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
    
    def executeForwardSlack(self):
        for route in self.routes:
            route.forgePushForward()
    
    def executeTimeNN(self):
        """Time-oriented NN in Solomon 1987, inital solution construction
        """
        sigma_1, sigma_2, sigma_3 = 1/3, 1/3, 1/3
        # determine the weight
        lastCusIdx = -1
        customers = self.instance.allNodes

        while len(self.notServed) > 0:
            # print(len(self.routes))
            if lastCusIdx == -1:
                # if have no route ... 
                # need to compare with the depot, choose the 'closest' one
                
                closeDist = []
                for nextCus in self.notServed:
                    closeDist.append(sigma_1 * self.instance.distMatrix[0][nextCus.id] + 
                                    sigma_2 * customers[nextCus.id].readyTime + 
                                    sigma_3 * (customers[nextCus.id].dueTime - self.instance.distMatrix[0][nextCus.id]))
                
                # find the minimum index of closeDist
                min_index, min_value = min(enumerate(closeDist), key = operator.itemgetter(1))
                choseCus = self.notServed[min_index]
                choseCus.serviceStartTime = max(choseCus.readyTime, self.instance.distMatrix[0][choseCus.id])
                choseCus.waitingTime = max(0, choseCus.readyTime - (self.instance.distMatrix[0][choseCus.id]))
                nodeList = [self.instance.depot, choseCus, self.instance.depot]
                newRoute = Route(self.instance, nodeList, set([choseCus]))
                # update start service time
                self.served.append(choseCus)
                self.notServed.pop(min_index)
                self.routes.append(newRoute)
                lastCusIdx = choseCus.id
                # update served customers / not-served customers
                # update routes of current solution
                # update last visited customer
            else:
                # have existing customers, which means existing routes
                # check every route and find the closest customer
                lastRoute = self.routes[-1]
                lastCustomer = lastRoute.nodes[-2]
                # store the close distance and target route ... 
                nxtCus = None; nxtRate = float('inf'); nxtCusIdx = -1
                for nextIdx, nextCus in enumerate(self.notServed):
                    # check feasibility
                    if lastCustomer.serviceStartTime + lastCustomer.serviceTime + self.instance.distMatrix[lastCustomer.id][nextCus.id] > nextCus.dueTime:
                        continue
                    if lastRoute.load + nextCus.demand > self.instance.capacity:
                        continue
                    curRate = sigma_1 * self.instance.distMatrix[lastCustomer.id][nextCus.id] + \
                            sigma_2 * (customers[nextCus.id].readyTime - (customers[lastCustomer.id].readyTime + customers[lastCustomer.id].serviceTime)) + \
                            sigma_3 * (customers[nextCus.id].dueTime - (customers[lastCustomer.id].readyTime + customers[lastCustomer.id].serviceTime + self.instance.distMatrix[lastCustomer.id][nextCus.id]))
                    if curRate < nxtRate:
                        nxtCus = nextCus
                        nxtRate = curRate
                        nxtCusIdx = nextIdx
                if nxtCus != None:
                    # find feasible customer! Just Insert it!
                    nxtCus.serviceStartTime = max(nxtCus.readyTime, self.instance.distMatrix[lastCustomer.id][nxtCus.id] + lastCustomer.serviceStartTime + lastCustomer.serviceTime)
                    nxtCus.waitingTime = max(0, nxtCus.readyTime - (self.instance.distMatrix[lastCustomer.id][nxtCus.id] + lastCustomer.serviceStartTime + lastCustomer.serviceTime))
                    lastCusIdx = nxtCus.id
                    self.routes[-1].nodes.insert(-1, nxtCus)
                    self.routes[-1].nodesSet.add(nxtCus)
                    self.routes[-1].load += nxtCus.demand
                    self.served.append(nxtCus)
                    self.notServed.pop(nxtCusIdx)
                else:
                    lastCusIdx = -1
                
    def removeCustomer(self, customer):
        deleteRoute = False 
        # judge whether to delete current route ... 
        for route in self.routes:
            if customer in route.nodesSet:
                # find it in this route... remove it
                # print(f"remove cus {customer.id}")
                route.removeCustomer(customer)
                break
        
        self.served.remove(customer)
        self.notServed.append(customer)

    def __str__(self):
        num_route = len(self.routes)
        cnt_customers = 0
        cost = 0
        phase1 = f"Truck used: {len(self.routes)}\n"
        for i in range(num_route):
            phase1 += f"Truck {i}\n"
            cnt_customers += (len(self.routes[i].nodes) - 2)
            nodes = self.routes[i].nodes
            cost += self.routes[i].distance
            for m in nodes:
                phase1 += (str(m) + "\n")
        phase1 += f"Cost: {cost}, Customers {cnt_customers}\n"
        return (phase1)
    
    # def executeRandomRemoval(self, nRemoval, randomGen):
    #     """execute the random removal
    #     Args:
    #         nRemoval (int): num of customers to remove
    #         randomGen (_type_): random generator
    #     """
    #     print(f"Random Removal: remove  {nRemoval} customers.")
    #     for _ in range(nRemoval):
    #         if len(self.served) == 0:
    #             break
    #         # pick a random customer and remove it from the solutoin
    #         cus = randomGen.choice(self.served)
    #         self.removeRequest(cus)
    
    def copy(self):
        """
        Method that creates a copy of the solution and returns it
        """
        # need a deep copy of routes because routes are modifiable
        routesCopy = list()
        for route in self.routes:
            routesCopy.append(route.copy())
        newCopy = Solution(self.instance, routesCopy, self.served.copy(), self.notServed.copy())
        newCopy.computeDistance()
        return newCopy
