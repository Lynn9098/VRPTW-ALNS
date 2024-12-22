from node import Node
import numpy as np

class Instance:
    """_summary_
    class that represent an instance, such as C101
    """
    def __init__(self, name, numVehicle, capacity, depot, customers):
        """_summary_

        Args:
            name (str): name of instance
            numVehicle (int): number of vehicles
            capacity (int): capacity of vehicles
            depot (Node): depot info of instance
            customers (list of Node): customers info of instance
        """
        self.name = name
        self.numVehicle = numVehicle
        self.capacity = capacity
        self.depot = depot
        self.customers = customers 

        self.distMatrix = np.zeros((len(self.customers) + 1, len(self.customers) + 1))  # distance matrix
        # save all nodes 
        self.allNodes = [depot] + customers
        self.numNodes = len(self.allNodes) 
        # compute distance matrix
        for i in range(self.numNodes):
            for j in range(self.numNodes):
                if i == j:
                    continue
                else:
                    self.distMatrix[i][j] = Node.getDistance(self.allNodes[i], self.allNodes[j])
    
    def readInstance(fileName):
        with open(fileName, 'r') as f:
            lines = f.readlines()
        numVehicle = 0 
        capacity = 0 
        depot = None 
        customers = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("VEHICLE"):
                # read vehicle data
                i += 2  # jump the headlines
                numVehicle, capacity = map(int, lines[i].split())
                i += 2
            elif line.startswith("CUSTOMER"):
                # read customers data
                i += 3  # jump the headlines
                while i < len(lines) and lines[i].strip():
                    data = list(map(int, lines[i].split()))
                    if depot == None:
                        depot = Node(
                            id =data[0],
                            x = data[1],
                            y = data[2],
                            demand = data[3],
                            readyTime = data[4],
                            dueTime = data[5],
                            serviceTime = data[6]
                        )
                    else:
                        customers.append(Node(
                            id =data[0],
                            x = data[1],
                            y = data[2],
                            demand = data[3],
                            readyTime = data[4],
                            dueTime = data[5],
                            serviceTime = data[6]
                        ))
                    i += 1
            else:
                i += 1
        
        # for cus in customers[:5]:
        #     print(cus)
        # print(depot)
        # print(type(customers))
        return Instance(fileName, numVehicle, capacity, depot, customers)
        
    
    
if __name__ == "__main__":
    # only for test ... 
    folder = "./benchmark/Solomon/"
    instList = ["c101.txt"]
    for inst in instList:
        fileName = folder + inst
        Instance.readInstance(fileName)
    