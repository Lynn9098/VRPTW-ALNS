from instance import Instance
from alns import ALNS
from visualizer import Visualizer
import os
from datetime import datetime

def get_timestamped_filename(prefix="results", extension=".md"):
    """
    Generate a time-stampled filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 获取当前时间
    return f"{prefix}_{timestamp}{extension}"

if __name__ == "__main__":
    # folder = "./benchmark/Gehring&Homberge/"
    # instList = ["RC2_6_1.txt"]
    # category = "Gehring&Homberge"
    
    # test list : C2_6_3.txt (checked)
    folder = "./benchmark/Solomon/"
    instList = [
        "c101.txt",
        "c102.txt",
        "c103.txt",
        "c104.txt",
        "c105.txt",
        "c106.txt",
        "c107.txt",
        "c108.txt",
        "c109.txt",
        "c201.txt",
        "c202.txt",
        "c203.txt",
        "c204.txt",
        "c205.txt",
        "c206.txt",
        "c207.txt",
        "c208.txt",
        "r101.txt",
        "r102.txt",
        "r103.txt",
        "r104.txt",
        "r105.txt",
        "r106.txt",
        "r107.txt",
        "r108.txt",
        "r109.txt",
        "r110.txt",
        "r111.txt",
        "r112.txt",
        "r201.txt",
        "r202.txt",
        "r203.txt",
        "r204.txt",
        "r205.txt",
        "r206.txt",
        "r207.txt",
        "r208.txt",
        "r209.txt",
        "r210.txt",
        "r211.txt",
        "rc101.txt",
        "rc102.txt",
        "rc103.txt",
        "rc104.txt",
        "rc105.txt",
        "rc106.txt",
        "rc107.txt",
        "rc108.txt",
        "rc201.txt",
        "rc202.txt",
        "rc203.txt",
        "rc204.txt",
        "rc205.txt",
        "rc206.txt",
        "rc207.txt",
        "rc208.txt"]
    category = "Solomon"
    
    os.makedirs("./Logger", exist_ok=True)

    file_path = os.path.join("./Logger", get_timestamped_filename())
    file_exists = os.path.exists(file_path)

    # for inst in instList[1:]:
    for inst in instList:
        fileName = folder + inst
        curInstance = Instance.readInstance(fileName)
        curInstance.updateBKS(category, inst.split(".")[0] ) # Update Best Known Solution ... 
        alns_solver = ALNS(curInstance)
        alns_solver.execute()
        tempResult = alns_solver.returnBrief()
        
        with open(file_path, "a") as file:
            if not file_exists:
                file.write("| Inst   |  Obj     | #.Truck | CPU (s) | Gap to BKS | BKS #. Trucks |\n")
                file.write("| :----: | :------: | :-----: | :-----: | :--------: | :-----------: |\n")
                file_exists = True
            file.write(f"| {inst[:-4]} | {round(tempResult[0],2)} | {tempResult[1]} | {round(tempResult[2],2)} | {round(tempResult[3],2)} | {tempResult[4]} |\n")

        # vrptw_visualizer = Visualizer(curInstance, alns_solver.bestSolution)
        # vrptw_visualizer.show()
        