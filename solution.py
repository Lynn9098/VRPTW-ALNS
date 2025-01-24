from route import Route
import operator
class Solution:
    
    def __init__(self, instance, routes, served, notServed):
        self.instance = instance
        self.routes = routes
        self.served = served
        self.notServed = notServed
        self.distance = self.computeDistance()
    
    def computeDistance(self):
        distance = 0
        for route in self.routes:
            distance += route.distance
        return distance
    
    def executeForwardSlack(self):
        self.served = []
        self.notServed = []
        for i in range(len(self.routes)):
            self.routes[i].forgePushForward()
            self.served += self.routes[i].nodes[1: -1]
    
    def executeNaive(self):
        """Naive initial solution construction, forge a route for each customer. 100 customer, 100 routes.
        """
        for customer in self.notServed:
            nodeList = [self.instance.depot, customer, self.instance.depot]
            newRoute = Route(self.instance, nodeList, set(nodeList))
            self.served.append(customer)
            self.routes.append(newRoute)
            self.distance += newRoute.distance
        self.notServed = []

    
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
                nodeList = [self.instance.depot, choseCus, self.instance.depot]
                newRoute = Route(self.instance, nodeList, set(nodeList))
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
                    # if nextCus.id == 3:
                    #     print(lastRoute.serviceStartTime[-2] , lastCustomer.serviceTime , self.instance.distMatrix[lastCustomer.id][nextCus.id])
                    if lastRoute.serviceStartTime[-2] + lastCustomer.serviceTime + self.instance.distMatrix[lastCustomer.id][nextCus.id] > nextCus.dueTime:
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
                    lastCusIdx = nxtCus.id
                    self.routes[-1].nodes.insert(-1, nxtCus)
                    self.routes[-1].nodesSet.add(nxtCus)
                    self.routes[-1].load += nxtCus.demand
                    self.routes[-1].serviceStartTime.insert(-1, max(nxtCus.readyTime, self.instance.distMatrix[lastCustomer.id][nxtCus.id] + lastRoute.serviceStartTime[-2] + lastCustomer.serviceTime))
                    self.routes[-1].waitingTime.insert(-1, max(0, nxtCus.readyTime - (self.instance.distMatrix[lastCustomer.id][nxtCus.id] + lastRoute.serviceStartTime[-2] + lastCustomer.serviceTime)))
                    self.routes[-1].distance += (self.instance.distMatrix[lastCustomer.id][nxtCus.id] + self.instance.distMatrix[nxtCus.id][0] - self.instance.distMatrix[lastCustomer.id][0])
                    self.served.append(nxtCus)
                    self.notServed.pop(nxtCusIdx)
                    lastRoute = self.routes[-1]
                else:
                    lastCusIdx = -1
        
        for route in self.routes:
            route.calculateTime()
            route.forgePushForward()
            self.distance += route.distance
                
    def removeCustomer(self, customer):
        # remove customer from Solution ... 
        # executed = False
        for i in range(len(self.routes)):
            if customer in self.routes[i].nodesSet:
                # print(f"Remove customer {customer.id}")
                # executed = True
                if len(self.routes[i].nodes) == 3:
                    self.routes.remove(self.routes[i])
                    self.distance -= (self.instance.distMatrix[customer.id][0] + self.instance.distMatrix[0][customer.id])
                    # delete the entire route ... 
                    break
                # print(f"length of nodes before: {len(self.routes[i].nodes)}")
                self.routes[i].removeCustomer(customer)
                # self.routes[i].forgePushForward()
                # print(f"length of nodes after: {len(self.routes[i].nodes)}")
                break
            
                
        # if not executed:
        #     print(f"WRONG!! {str(customer)}") 
        #     print(self)
        #     print("+++++")
        #     for node in self.routes[13].nodesSet:
        #         print(node == customer, node, customer)
        
        self.served.remove(customer)
        self.notServed.append(customer)

    def __str__(self):
        # num_route = len(self.routes)
        cnt_customers = 0
        cost = 0
        visited = [0 for _ in range(self.instance.numNodes)]
        phase1 = f"Truck used: {len(self.routes)}\n"
        for idx, route in enumerate(self.routes):
            phase1 += f"Truck {idx}\n"
            cnt_customers += (len(self.routes[idx].nodes) - 2)
            nodes = route.nodes
            cost += route.distance
            for j, node in enumerate(nodes):
                phase1 += (str(node) + "waitingTime: " + str(route.waitingTime[j]) + "; serviceStartTime: " + str(route.serviceStartTime[j]) + "; forwardTimeSlack:" + str(route.forwardTimeSlack[j]) + "\n")
                if node.id != 0:
                    visited[node.id] += 1
        
        phase1 += f"Cost: {cost}, Customers {cnt_customers}, check {self.distance}\n"
        for i in range(1, self.instance.numNodes):
            if visited[i] > 1:
                phase1 += f"Customer {i} visited {visited[i]} times\n"
            elif visited[i] < 1:
                phase1 += f"Customer {i} is not visited.\n"
                
        return (phase1)

    def checkFeasibility(self):
        """check feasibility of the solution
        """
        visited = [0 for _ in range(self.instance.numNodes)]
        isFeas = True
        for idx, route in enumerate(self.routes):
            if route.nodes[0].id != 0 or route.nodes[-1].id != 0:
                print(f"FATAL: route {idx} start/end != depot!")
                isFeas = False
                break
            curLoad = 0
            for j, node in enumerate(route.nodes):
                if node.id != 0:
                    visited[node.id] += 1
                curLoad += node.demand
                if curLoad > self.instance.capacity:
                    print(f"FATAL: route {idx} exceed capacity!")
                    isFeas = False
        for i in range(1, len(visited)):
            if visited[i] > 1:
                print(f"Cus {i} is visited multiple times!")
                isFeas = False
            elif visited[i] < 1:
                print(f"Cus {i} is not visited!")
                isFeas = False
        return isFeas
    
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

