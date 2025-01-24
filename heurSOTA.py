from pyvrp import Model
from pyvrp.stop import MaxRuntime
from instance import Instance
from node import Node

if __name__ == "__main__":
    folder = "./benchmark/Solomon/"
    folder = "./benchmark/Gehring&Homberge/"
    instList = ["C1_2_1.txt"]
    COORDS = []
    DEMANDS = []
    DURATION_MATRIX = []
    TIME_WINDOWS = []
    SERVICE_DURATION = []
    NODES = []
    m =  Model()
    for inst in instList:
        fileName = folder + inst
        curInstance = Instance.readInstance(fileName)
        for node in curInstance.allNodes:
            tmp_dist = []
            COORDS.append((node.x, node.y))
            DEMANDS.append((node.demand))
            TIME_WINDOWS.append((node.readyTime, node.dueTime))
            SERVICE_DURATION.append(node.serviceTime)
            for node_ in curInstance.allNodes:
                if node.id == node_.id:
                    tmp_dist.append(0)
                else:
                    tmp_dist.append(Node.getDistance(node, node_))
            DURATION_MATRIX.append(tmp_dist)
            if node.id > 0:
                NODES.append(m.add_client(
                        x = node.x,
                        y = node.y,
                        delivery = node.demand,
                        tw_early = node.readyTime, 
                        tw_late = node.dueTime, 
                    )
                )
        # print(len(COORDS), len(DURATION_MATRIX), len(DURATION_MATRIX[0]))
        depot = m.add_depot(x = curInstance.depot.x, y = curInstance.depot.y)
        NODES = [depot] + NODES
        for node in curInstance.allNodes:
            for node_ in curInstance.allNodes:
                if node.id == node_.id:
                    continue
                m.add_edge(NODES[node.id], NODES[node_.id], distance = DURATION_MATRIX[node.id][node_.id], duration = DURATION_MATRIX[node.id][node_.id])

        print(curInstance.capacity, curInstance.numVehicle)
        print([curInstance.capacity for _ in range(curInstance.numVehicle)])
        m.add_vehicle_type(
            num_available = curInstance.numVehicle,
            capacity = curInstance.capacity

        )
        res = m.solve(stop = MaxRuntime(60), display=True)  # 60 s
