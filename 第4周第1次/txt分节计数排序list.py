# 用list做排序，体会差别
import jieba
txt = open('D:\Vault\school\junior_last\python 与人工智能\python与人工智能-代码\第3周第2次\高瓴人工智能学院简介.txt', 'r', encoding='utf-8').read()
test = jieba.lcut(txt)
print("=====提取分解数据=====")

words = []
numbers = []

for word in test:
    if len(word) < 2:
        continue
    else:
        if word not in words:
            words.append(word)
            numbers.append(1)
        else:
            index = words.index(word)
            numbers[index] += 1

print("============累加计数============")

#看起来似乎无法排序，只有直接输出结果

for i in range(15):
    print("{0:<15}{1:>5}".format(words[i],numbers[i]))