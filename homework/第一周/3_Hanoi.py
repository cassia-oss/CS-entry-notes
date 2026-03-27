#汉诺塔移动过程
def hanoi(n, a, b, c):
    if n == 1:
        print( "move{} from {} to {}".format(n, a, c) )
    else:
        hanoi(n-1, "A", "C", "B")
        print( "move{} from{} to {}".format(n, a, c) )
        hanoi(n-1, "B", "A", "C")
print(hanoi(7, "A", "B", "C"))