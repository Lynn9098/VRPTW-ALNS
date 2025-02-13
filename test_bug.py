import os

# 查看当前工作目录
current_dir = os.getcwd()
print(f"当前工作目录: {current_dir}")

# 构建完整路径
path = os.path.join(current_dir, 'VRPTW-ALNS','benchmark', 'Gehring&Homberge')
print(path)

if os.path.exists(path):
    print("路径存在")
else:
    print("路径不存在")