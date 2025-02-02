from instance import Instance
from alns import ALNS
from visualizer import Visualizer

if __name__ == "__main__":
    # 跑通一个case的
    # folder = "./benchmark/Gehring&Homberge/"
    # instList = ["C2_2_4.txt"]
    # test list : C2_6_3.txt (checked)
    folder = "./benchmark/Solomon/"
    instList = ["rc101.txt"] # FIXME: BUG here! 
    
    for inst in instList:
        fileName = folder + inst
        curInstance = Instance.readInstance(fileName)
        alns_solver = ALNS(curInstance)
        alns_solver.execute()
        # vrptw_visualizer = Visualizer(curInstance, alns_solver.bestSolution)
        # vrptw_visualizer.show()
        