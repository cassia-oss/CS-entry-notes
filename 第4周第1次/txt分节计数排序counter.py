import jieba
from collections import defaultdict
txt = open('D:\Vault\school\junior_last\python 与人工智能\python与人工智能-代码\第3周第2次\高瓴人工智能学院简介.txt', 'r', encoding='utf-8').read()
positions = defaultdict(list) # 默认值是list函数返回的一个空列表

for word,start_pots,end_pots in jieba.tokenize(txt):
    if len(word) > 1:
           positions[word].append((start_pots,end_pots))

results = sorted(positions.items(),key= lambda x:(-len(x[1]),x[0]))

for word,position in results[:15]:
    print(word)
    print(positions)