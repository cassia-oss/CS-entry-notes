
import turtle as t
print("====正在启动画图程序...====")

t.setup(650, 350, 200, 200)#设置画布大小和位置

t.showturtle()#显示画笔

t.pendown()#落笔

#设置画笔属性
t.pensize(2)
t.pencolor("purple")
t.seth(90)

for i in range(100):
    t.forward(i*2)
    t.left(90)


print("===画完了，准备进入等待状态...===")

