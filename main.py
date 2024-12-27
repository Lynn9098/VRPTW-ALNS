from instance import Instance

if __name__ == "__main__":
    # 跑通一个case的
    folder = "./benchmark/Solomon/"
    instList = ["c101.txt"]
    for inst in instList:
        fileName = folder + inst
        Instance.readInstance(fileName)
    