#上课用的模拟概率的估计方法
import random as r
import math

r.seed()#生成随机算子，随时间变化，每次生成都不一样

N=10000 #设置总的试验次数
hits=0 #设置初始击中次数

for i in range(1, N+1): #非常严格的1到N次
    x,y = r.random(),r.random()
    dist = math.sqrt(x**2+y**2)
    if dist <= 1.0:
        hits = hits + 1 #判定在圆内，击中次数加1

pi_1= 4 * (hits / N) #计算概率
print("Pi={0}.".format(pi_1))




