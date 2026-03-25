# PythonDraw.py
import turtle
import turtle as t
#import tkinter as tk
#root = tk.Tk()
#root.wm_attributes('-topmost', 1)


t.setup(650, 350, 200, 200)

root = t.getcanvas().winfo_toplevel()  # 获取 turtle 的 tkinter 根窗口
root.wm_attributes('-topmost', 1)  # 将窗口置顶

t.showturtle()

t.penup()
t.fd(-250)
t.pendown()



t.pensize(25)
t.pencolor("purple")
t.seth(-40)

for i in range(4):
    t.circle(40, 80)
    t.circle(-40, 80)

t.circle(40, 80 / 2)
t.fd(40)
t.circle(16, 180)
t.fd(40 * 2 / 3)
t.done()
