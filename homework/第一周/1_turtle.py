
import turtle as t

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


