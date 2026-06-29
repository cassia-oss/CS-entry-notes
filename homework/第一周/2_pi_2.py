# 泰勒展开

N = 10000
pi = 0

for i in range(N+1):#从0开始到N结束，包含N的循环
    a = (-1) ** i
    b = a / (2 * i + 1)
    pi += b

print("Pi = {}".format(pi*4))
