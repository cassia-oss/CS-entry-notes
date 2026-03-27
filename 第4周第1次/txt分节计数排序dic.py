#自己写一次词频统计的代码
import jieba
txt = open('D:\Vault\school\junior_last\python 与人工智能\python与人工智能-代码\第3周第2次\高瓴人工智能学院简介.txt', 'r', encoding='utf-8').read()

test = jieba.lcut(txt)

print("切分单词===={}=====".format(test))

count = {}

for word in test:
    if len(word) < 2:
        continue
    else:
        count[word] = count.get(word,0) + 1

print("count======{}=========".format(count))

#order_list = count.sort(key= lambda y:(-y[1],-len(y[0]))) 
#不能直接对字典做排序

items = list(count.items()) #提取成为二元数组
items.sort(key = lambda y:(-y[1],-len(y[0])))

print("========results of sorting:{}=======".format(items))

# 已经排好序只需要打印前面15个数字即可
for i in range(15):
    word,number = items[i]
    print("{0:<10}{1:>5}".format(word,number))