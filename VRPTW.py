import numpy as np
import random
import math
import time
import os
import pandas as pd
# FIXME: Previous version. May delete when necessary.
class Customer:
    def __init__(self, idx, demand, ready_time, due_time, service_time, x, y):
        self.idx = idx
        self.demand = demand
        self.ready_time = ready_time
        self.due_time = due_time
        self.service_time = service_time
        self.x = x
        self.y = y

class Route:
    def __init__(self, vehicle_id, customers, distance, capacity):
        self.vehicle_id = vehicle_id
        self.customers = customers
        self.distance = distance
        self.capacity = capacity

    def __repr__(self):
        return f"Route(vehicle_id={self.vehicle_id}, customers={self.customers}, distance={self.distance:.2f})"


class VRPTW_LNS:
    def __init__(self, depot, customers, vehicle_capacity, max_vehicles):
        self.depot = depot
        self.customers = customers
        self.vehicle_capacity = vehicle_capacity
        self.max_vehicles = max_vehicles
        self.distance_matrix = self.calculate_distance_matrix()
        self.best_solution = None
        self.best_cost = float('inf')

    def calculate_distance_matrix(self):
        all_points = [self.depot] + self.customers
        n = len(all_points)
        distance_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                distance_matrix[i][j] = np.sqrt(
                    (all_points[i].x - all_points[j].x) ** 2 +
                    (all_points[i].y - all_points[j].y) ** 2
                )
        return distance_matrix

#修改贪心算法，减少车辆数
    def initialize_solution(self):  # 贪心算法生成初始解
        routes = []
        x = [c for c in range(1, len(self.customers) + 1)]
        random.shuffle(x)
        # print(x)
        unvisited = x
        for vehicle_id in range(1,self.max_vehicles+1):
            capacity = self.vehicle_capacity
            current_time = 0
            route = [0]  # Start from depot
            route_time=0
            while unvisited:  # 一次循环安排一个客户
                next_customer = None
                best_cost = float('inf')
                customer_judge=float('inf')
                current_judge=float('inf')
                pre_time=0
                for customer_id in unvisited:
                    #print(customer_id)
                    customer = self.customers[customer_id - 1]
                    pre_time=current_time + self.distance_matrix[route[-1]][customer_id]
                    if pre_time>customer.due_time:
                        continue
                    if customer.demand > capacity:
                        continue
                    current_judge=self.distance_matrix[route[-1]][customer_id]+max(0, customer.ready_time-pre_time)
                    if current_judge<customer_judge:
                        customer_judge=current_judge
                        next_customer=customer_id
                if next_customer is None:
                    break
                route.append(next_customer)
                unvisited.remove(next_customer)
                capacity -= self.customers[next_customer - 1].demand
                current_time = max(current_time + self.distance_matrix[route[-2]][next_customer],
                                   self.customers[next_customer - 1].ready_time) + \
                               self.customers[next_customer - 1].service_time
            route.append(0)  # Return to depot
            if len(route) > 2:
                routes.append(Route(vehicle_id, route, self.calculate_route_distance(route),self.vehicle_capacity-capacity))
        #print(routes)
        if sum(len(rou.customers)-2 for rou in routes) != len(self.customers):
            return ValueError
        return routes

    def calculate_route_distance(self, route):
        return sum(self.distance_matrix[route[i]][route[i + 1]] for i in range(len(route)-1))

    def calculate_capcity(self, customers, route):
        ca=0
        for cu in route:
            ca+=customers[cu-1].demand
        return ca

    def calculate_viotime(self, customers, route):
        route_time = 0
        vio_time = 0
        c = 0
        for i in route:
            if i == 0:
                continue
            arrival_time = route_time + self.distance_matrix[c][i]
            if arrival_time < customers[i - 1].ready_time:
                vio_time+=customers[i - 1].ready_time-arrival_time
            arrival_time = max(route_time + self.distance_matrix[c][i], customers[i - 1].ready_time)
            route_time = arrival_time + customers[i - 1].service_time
            c=i
        return vio_time

    def destroy_random(self, solution, per=2):  # 随机挑选破坏
        num_customers_to_remove = per
        # num_customers_to_remove = random.randint(1, num_customers_to_remove)
        removed_customers = random.sample([c for route in solution for c in route.customers if c != 0],num_customers_to_remove)
        remaining_routes = []
        for route in solution:
            remaining_customers = [c for c in route.customers if c not in removed_customers]
            # print(remaining_customers)
            if len(remaining_customers) > 2:
                remaining_routes.append(Route(route.vehicle_id, remaining_customers,
                                              self.calculate_route_distance(remaining_customers), self.calculate_capcity(customers,remaining_customers)))
        return remaining_routes, removed_customers

    def destroy_greedy(self, solution, par=1, per=2):  # 贪心破坏
        num_customers_to_remove = per
        # num_customers_to_remove = random.randint(1, num_customers_to_remove)
        removed_customers = []
        sequence_maxmin = []
        save = [0 for i in range(len(self.customers))]
        for route in solution:
            for i in route.customers:
                if i == 0:
                    continue
                # new_route = route.customers
                # new_route.remove(i)
                # new_distance = self.calculate_route_distance(new_route)
                # cur_distance = self.calculate_route_distance(route)
                x = route.customers.index(i)
                a = route.customers[x - 1]
                b = route.customers[x]
                c = route.customers[x + 1]
                save[i - 1] = self.distance_matrix[a][b] + self.distance_matrix[b][c] - self.distance_matrix[a][c]
        # print(save)
        for i in range(len(save)):
            idx = save.index(max(save)) + 1
            sequence_maxmin.append(idx)
            save[idx - 1] = 0
        for i in range(num_customers_to_remove):
            r=random.random()
            idx = math.floor(pow(r, par)*len(sequence_maxmin))
            removed_customers.append(sequence_maxmin[idx])
            sequence_maxmin.remove(sequence_maxmin[idx])
        '''''
        for i in range(num_customers_to_remove):
            idx = save.index(max(save)) + 1
            removed_customers.append(idx)
            save[idx - 1] = 0'''
        # print(removed_customers)
        remaining_routes = []
        for route in solution:
            remaining_customers = [c for c in route.customers if c not in removed_customers]
            if len(remaining_customers) > 2:
                remaining_routes.append(Route(route.vehicle_id, remaining_customers,
                                              self.calculate_route_distance(remaining_customers), self.calculate_capcity(customers,remaining_customers)))
        return remaining_routes, removed_customers

    def customer_related(self, cus1, cus2):
        a = 0
        a1 = 1 * (self.distance_matrix[cus1][cus2])
        a2 = 0.2 * (abs(self.customers[cus1 - 1].ready_time - self.customers[cus2 - 1].ready_time) + abs(
            self.customers[cus1 - 1].due_time - self.customers[cus2 - 1].due_time))
        a3 = 1 * (abs(self.customers[cus1 - 1].demand - self.customers[cus2 - 1].demand))
        a = a1 + a2 + a3
        return a

    def destroy_shaw(self, solution, per=2):
        num_customers_to_remove = per
        destroy = random.randint(1, len(self.customers))
        removed_customers = []
        remaining_customers = [c for c in range(1, len(self.customers) + 1)]
        removed_customers.append(destroy)
        remaining_customers.remove(destroy)
        for i in range(1, num_customers_to_remove - 1):
            related = []
            for j in range(1, len(self.customers) + 1):
                related.append(self.customer_related(destroy, j))
                if j not in remaining_customers:
                    related[j - 1] = 0
            related[destroy - 1] = 0
            destroy = related.index(max(related)) + 1
            removed_customers.append(destroy)
            remaining_customers.remove(destroy)
        remaining_routes = []
        for route in solution:
            remaining_customers = [c for c in route.customers if c not in removed_customers]
            if len(remaining_customers) > 2:
                remaining_routes.append(Route(route.vehicle_id, remaining_customers,
                                              self.calculate_route_distance(remaining_customers), self.calculate_capcity(customers,remaining_customers)))
        return remaining_routes, removed_customers

    def repair_random(self, partial_solution, removed_customers):
        num_route = len(partial_solution)
        for customer_id in removed_customers:
            insert_route = random.randint(1, num_route) - 1
            x = len(partial_solution[insert_route].customers)
            partial_solution[insert_route].customers.insert(random.randint(1, x - 1), customer_id)
            partial_solution[insert_route].distance = self.calculate_route_distance(partial_solution[insert_route].customers)

    def repair_greed(self, partial_solution, removed_customers, par=1):  # 贪心修补
        for customer_id in removed_customers:
            best_route = None
            best_position = None
            increases = []
            increases_route = []
            best_increase = float('inf')
            for route in partial_solution:
                for i in range(1, len(route.customers)):
                    new_route = route.customers[:i] + [customer_id] + route.customers[i:]
                    new_distance = self.calculate_route_distance(new_route)
                    increase = new_distance - route.distance
                    increases.append(increase)
                    increases_route.append([route.vehicle_id, i, customer_id])
            increase_sort = increases
            increase_sort.sort(reverse=True)
            r = random.random()
            idx_increase =0# math.floor(pow(r, par) * len(increase_sort))
            best_route, best_position, insert_id = increases_route[increases.index(increase_sort[idx_increase])]
            partial_solution[best_route-1].customers.insert(best_position, insert_id)
            partial_solution[best_route-1].distance=self.calculate_route_distance(partial_solution[best_route-1].customers)
            #best_route.distance += increase_sort[idx_increase]

    def repair_regret(self, partial_solution, removed_customers):
        while removed_customers != []:
            rem_name = []
            regret = []
            re_route = []
            re_position = []
            re_increase = []
            for customer_id in removed_customers:
                best_route = None
                best_position = None
                best_increase = float('inf')
                next_increase = float('inf')
                for route in partial_solution:
                    for i in range(1, len(route.customers)):
                        new_route = route.customers[:i] + [customer_id] + route.customers[i:]
                        new_distance = self.calculate_route_distance(new_route)
                        increase = new_distance - route.distance
                        if increase < best_increase:
                            next_increase = best_increase
                            best_increase = increase
                            best_route = route
                            best_position = i
                        elif increase < next_increase:
                            next_increase = increase
                rem_name.append(customer_id)
                regret.append(next_increase - best_increase)
                re_route.append(best_route)
                re_position.append(best_position)
                re_increase.append(best_increase)
            # 插入
            idx = regret.index(max(regret))
            name = rem_name[idx]
            insert_route = re_route[idx]
            insert_position = re_position[idx]
            insert_increase = re_increase[idx]
            index_route = partial_solution.index(insert_route)
            partial_solution[index_route].customers.insert(insert_position, name)
            partial_solution[index_route].distance=self.calculate_route_distance(partial_solution[index_route].customers)
            #partial_solution[index_route].distance += insert_increase
            removed_customers.remove(name)

    def accept(self, customers, partial_solution, vehicle_capacity):
        arrival_time = 0
        acc = 0
        for route in partial_solution:
            route_capcity = 0
            route_time = 0
            c = 0
            for i in route.customers:
                if i == 0:
                    continue
                route_capcity += customers[i - 1].demand
                arrival_time = max(route_time + self.distance_matrix[c][i], customers[i - 1].ready_time)
                if arrival_time > customers[i - 1].due_time:
                    acc += 1
                route_time = arrival_time + customers[i - 1].service_time
                c = i
            if route_capcity>vehicle_capacity:
                acc+=1
        x = [c for route in partial_solution for c in route.customers if c != 0]
        if len(x) != len(customers):
            acc += 1
        if acc > 0:
            return False
        elif acc == 0:
            return True

    def clear_0(self, partial_solution):
        for i in range(len(partial_solution)):
            partial_solution[i].vehicle_id = i + 1

    def check_feasibility(self, best_solution):
        error_route=[]
        error_cus = []
        have_customers = []#检查是否有重复客户
        for route in best_solution:
            ar_time = 0
            c = 0
            ca = 0
            for cu in route.customers:
                if cu == 0:
                    continue
                have_customers.append(cu)
                ca += self.customers[cu - 1].demand
                arrival_time = max(ar_time + vrptw.distance_matrix[c][cu], self.customers[cu - 1].ready_time)
                # if arrival_time<=customers[cu-1].due_time:
                #    print('客户'+str(cu)+'到达时间为：'+str(arrival_time)+' due为：'+str(customers[cu-1].due_time)+' 达成要求')
                if arrival_time > self.customers[cu - 1].due_time:
                    print('客户' + str(cu) + '到达时间为：' + str(arrival_time) + ' due为：' + str(
                        self.customers[cu - 1].due_time) + ' 未达成要求')
                    error_cus.append([route.vehicle_id,cu,'时间不合理'])
                c = cu
            if ca > vehicle_capacity:
                print('车辆' + str(route.vehicle_id) + '不合理')
                error_route.append([route,'容量不合理'])
        for cus in self.customers:
            if cus.idx not in have_customers:
                error_cus.append([id,'缺少该客户'])
        return error_route, error_cus

    def get_per(self,iterations):
        per_low=min(math.ceil(0.02*len(self.customers)),10)
        per_high=min(math.ceil(0.02*len(self.customers)),30)
        per_r=random.random()
        #per_r=pow(per_r,iterations/100)
        per=int(per_r*per_low+(1-per_r)*per_high)
        #print(per)
        return per

    def search(self, initialize_solution, instance_name, iterations=500):
        des_score = [0, 0, 0]  # [random. greedy, shaw]
        des_use = [0, 0, 0]
        rep_score = [0, 0, 0]
        rep_use = [0, 0, 0]
        b = 0.5
        w_des = [10, 10, 10]
        w_rep = [10, 10, 10]
        p_des_ran = w_des[0] / sum(w_des)
        p_des_gre = w_des[1] / sum(w_des)
        p_des_sha = w_des[2] / sum(w_des)
        p_rep_ran = w_rep[0] / sum(w_rep)
        p_rep_gre = w_rep[1] / sum(w_rep)
        p_rep_reg = w_rep[2] / sum(w_rep)
        a = 0.97
        j = 0
        #per=random.uniform(0.1,0.3)
        current_solution = initialize_solution
        current_cost = sum(route.distance for route in current_solution)
        #current_cost = current_cost+sum(self.calculate_viotime(customers,cus.customers) for cus in current_solution)#等待时间惩罚
        history_cost = []
        self.best_solution = current_solution
        self.best_cost = current_cost
        print(f"Instance: {instance_name}, Iteration {0}, Best Cost: {self.best_cost}")
        for iteration in range(iterations):
            # print(iteration+1)
            T = 100
            print(
                f"Instance: {instance_name}, Iteration {iteration + 1},T: {T}，Best Cost: {self.best_cost}，Vehicles: {len(self.best_solution)}")
            while T > 10:
                # print(T)
                acc_bad=0
                if j > 50:
                    acc_bad=1
                p_des_ran = w_des[0] / sum(w_des)
                p_des_gre = w_des[1] / sum(w_des)
                p_des_sha = w_des[2] / sum(w_des)
                ran = random.random()
                per=self.get_per(iterations=iteration)
                if ran < p_des_ran or acc_bad==1:  # 选择destroy算子
                    partial_solution, removed_customers = self.destroy_random(current_solution, per=per)
                    use = 0
                    des_use[use] += 1
                elif ran < p_des_ran + p_des_gre:
                    partial_solution, removed_customers = self.destroy_greedy(current_solution,par=2, per=per)
                    use = 1
                    des_use[use] += 1
                else:
                    partial_solution, removed_customers = self.destroy_shaw(current_solution, per=per)
                    use = 2
                    des_use[use] += 1
                self.clear_0(partial_solution)
                # 修复
                p_rep_ran = w_des[0] / sum(w_rep)
                p_rep_gre = w_des[1] / sum(w_rep)
                p_rep_reg = w_des[2] / sum(w_rep)
                ran = random.random()
                if ran < p_rep_ran or acc_bad==1:
                    self.repair_random(partial_solution, removed_customers)
                    use_r = 0
                    rep_use[use_r] += 1
                elif ran < p_rep_gre + p_rep_ran:
                    self.repair_greed(partial_solution, removed_customers,par=2)
                    use_r = 1
                    rep_use[use_r] += 1
                else:
                    self.repair_regret(partial_solution, removed_customers)
                    use_r = 2
                    rep_use[use_r] += 1

                # print(self.best_solution)
                # print(self.best_cost)
                new_cost = sum(route.distance for route in partial_solution)

                if self.accept(self.customers, partial_solution, vehicle_capacity) == False:
                    des_score[use] += 0.3
                    rep_score[use_r] += 0.3
                    T = a * T
                    continue
                    # des_use[use]-=1
                    # rep_use[use_r]-=1
                elif new_cost<self.best_cost or len(partial_solution)<len(self.best_solution):
                #if new_cost < self.best_cost or len(partial_solution) < len(self.best_solution):
                    current_solution = partial_solution
                    current_cost = new_cost
                    self.best_solution = partial_solution
                    self.best_cost = new_cost
                    print(f"Instance: {instance_name}, Iteration {iteration + 1},T: {T}，Best Cost: {self.best_cost}，Vehicles: {len(self.best_solution)}")
                    self.clear_0(partial_solution)
                    j = 0
                    des_score[use] += 1.5
                    rep_score[use_r] += 1.5
                #elif new_cost < current_cost and new_cost not in history_cost \
                elif new_cost+sum(self.calculate_viotime(customers, cus.customers) for cus in partial_solution) < \
                                current_cost+sum(self.calculate_viotime(customers, cus.customers) for cus in current_solution):
                    current_solution = partial_solution
                    current_cost = new_cost
                    des_score[use] += 1.2
                    rep_score[use_r] += 1.2
                elif random.random() < math.exp(-(new_cost - current_cost) / T) or acc_bad==1:
                    current_solution = partial_solution
                    current_cost = new_cost
                    des_score[use] += 0.8
                    rep_score[use_r] += 0.8
                    j = 0
                else:
                    des_score[use] += 0.6
                    rep_score[use_r] += 0.6
                #if des_use[use] != 0 and rep_use[use_r] != 0:
                w_des[use] = b * w_des[use] + (1 - b) * des_score[use] / des_use[use]  # 更新权重
                w_rep[use_r] = b * w_rep[use_r] + (1 - b) * rep_score[use_r] / rep_use[use_r]
                #history_cost.append(new_cost)
                #print(f"Instance: {instance_name}, Iteration {iteration + 1},T: {T}，Current Cost: {current_cost}，Vehicles: {len(current_solution)}")
                T = a * T
            j += 1
        print(f'使用destroy_random: {des_use[0]}次')
        print(f'使用destroy_greedy: {des_use[1]}次')
        print(f'使用destroy_shaw  : {des_use[2]}次')
        print(f'使用repair_random : {rep_use[0]}次')
        print(f'使用repair_greedy : {rep_use[1]}次')
        print(f'使用repair_regret : {rep_use[2]}次')



#读取文件数据
random.seed(12138)
results=[]
filePath = r'D:\Python\VRPTW-ALNS\solomon-100'
#instances_vrptw=os.listdir(filePath)
instances_vrptw=['r101.txt']#,'r102.txt','r103.txt']#,'r104.txt','r105.txt','r106.txt',
                 #'r107.txt','r108.txt','r109.txt','r110.txt','r111.txt','r112.txt',]
for instance_name in instances_vrptw:
    start = time.time()
    file_path = r'D:\Python\VRPTW-ALNS\solomon-100'+'\\'+ instance_name
    with open(file_path, 'r') as file:
        data0 = file.read()
    data = []
    for line in data0.strip().split('\n'):
        data.append(line.split())
    while [] in data:
        data.remove([])

    best_vehicles = int(data[0][1])
    best_cost=float(data[0][2])
    max_vehicles, vehicle_capacity = data[data.index(['NUMBER', 'CAPACITY'])+1]
    max_vehicles=int(max_vehicles)
    vehicle_capacity=int(vehicle_capacity)
    print('vehicle_capacity:', vehicle_capacity)

    num=data.index(['CUSTOMER'])+2
    customers=[]
    for i in range(num, len(data)):
        cur=data[i]
        idx=int(cur[0])
        demand=int(cur[3])
        ready_time=int(cur[4])
        due_time=int(cur[5])
        service_time=int(cur[6])
        x=int(cur[1])
        y=int(cur[2])
        if i == num:
            depot = Customer(idx, demand, ready_time, due_time, service_time, x, y)
        else :
            customers.append(Customer(idx, demand, ready_time, due_time, service_time, x, y))

    #to do list
    #Worst Case Removal算子
    #不同案例的批量运行

    result_one=[]   #算例、客户数、成本、车辆、运算时间、具体路线
    best_cost_all=float('inf')
    vrptw = VRPTW_LNS(depot, customers, vehicle_capacity, max_vehicles)
    initialize_solution=vrptw.initialize_solution()
    for segment in range(5):
        vrptw.search(initialize_solution,instance_name, iterations=200)
        best_cost_current=vrptw.best_cost
        if best_cost_current<best_cost_all:
            best_cost_all=best_cost_current
            error_route, error_cus = vrptw.check_feasibility(vrptw.best_solution)
            result = [instance_name, len(customers), best_cost_all,float(best_cost), len(initialize_solution),
                      len(vrptw.best_solution), int(best_vehicles), 0, vrptw.best_solution,error_route, error_cus]
    end = time.time()
    use_time=round(float(end-start),2)
    #print ('运行时间：'+str(end-start)+'秒')
    result[7]=use_time
    results.append(result)
# list转dataframe
df = pd.DataFrame(results, columns=['算例','客户数','成本','最佳成本','初始解车辆数', '车辆数', '最佳车辆数', '运算时间', '具体路线','错误路线','错误客户'])
# 保存到本地excel
save_path=r'D:/Python/VRPTW-ALNS/算例结果.xlsx'
df.to_excel(save_path, index=False)

#print(results)
#print(max(results[:][1]))
''''
xx=vrptw.initialize_solution()
print(xx)
print(vrptw.best_solution)
print(len(vrptw.best_solution))
def check_feasibility():
    for route in vrptw.best_solution:
        ar_time=0
        c=0
        ca=0
        for cu in route.customers:
            if cu == 0 :
                continue
            ca+=customers[cu-1].demand
            arrival_time = max(ar_time + vrptw.distance_matrix[c][cu], customers[cu - 1].ready_time)
            #if arrival_time<=customers[cu-1].due_time:
            #    print('客户'+str(cu)+'到达时间为：'+str(arrival_time)+' due为：'+str(customers[cu-1].due_time)+' 达成要求')
            if arrival_time>customers[cu-1].due_time:
                print('客户'+str(cu)+'到达时间为：'+str(arrival_time)+' due为：'+str(customers[cu-1].due_time)+' 未达成要求')
            c=cu
        if ca>vehicle_capacity:
            print('车辆' + str(route.vehicle_id) + '不合理')'''
