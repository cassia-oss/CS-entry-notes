#TempConvert.py

TempStr = input("请输入带有符号的温度值: ")

print("TempStr[-1] = ", TempStr[-1])

if TempStr[-1] in ['F', 'f']:
    #print(type(TempStr))
    #print(TempStr[-1] in ['F', 'f'])
    #print("TempStr[0:-1] = ", TempStr[0:-1])
    #print("eval(TempStr[0:-1]) = ", eval(TempStr[0:-1]))
    C = (eval(TempStr[0:-1]) - 32)/1.8
    print("转换后的温度是{:.2f}C".format(C))

elif TempStr[-1] in ['C', 'c']:
    F = 1.8*eval(TempStr[0:-1]) + 32
    print("转换后的温度是{:.2f}F".format(F))
else:
    print("输入格式错误")