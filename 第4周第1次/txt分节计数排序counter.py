import jieba
from collections import defaultdict
txt = open('D:\Vault\school\junior_last\python 与人工智能\python与人工智能-代码\第3周第2次\高瓴人工智能学院简介.txt', 'r', encoding='utf-8').read()
positions = defaultdict(list)

for word,start_point,end_point in jieba.tokenize(txt):
    if len(word) > 1:
        positions[word].append((start_point,end_point))

results = sorted(positions.items(),key=lambda x:(-len(x[1]),x[0]))

for word, pos_list in results[:15]:
    print("{0:<10}{1:>5}".format(word, len(pos_list)))

print(results)