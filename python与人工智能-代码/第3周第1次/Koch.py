import turtle


def koch(size, n):
    if n == 0:
        turtle.fd(size)
    else:
        for angle in [0, 60, -120, 60]:
            turtle.left(angle)
            koch(size / 3, n - 1)#尺寸每次是原来的三分之一，递归深度减1


def main():
    turtle.setup(600, 600)
    turtle.speed(1)
    turtle.penup()
    turtle.goto(-200, 100)
    turtle.pendown()
    turtle.pensize(2)

    # 递归调用koch函数绘制雪花曲线，是主程序的核心部分。
    # 通过设置不同的递归深度，可以绘制出不同复杂程度的雪花曲线。
    level = 1
    koch(400, level)
    turtle.right(120)

    koch(400, level)
    turtle.right(120)

    koch(400, level)
    #为什么需要调用三次koch函数？因为雪花曲线是由三条相同的曲线组成的，每条曲线之间相隔120度，所以需要调用三次koch函数来绘制完整的雪花曲线。


    turtle.hideturtle()
    turtle.exitonclick()


main()