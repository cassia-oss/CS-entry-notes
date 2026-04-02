import jieba
from collections import Counter
txt = open('D:\Vault\school\junior_last\python 与人工智能\python与人工智能-代码\第3周第2次\高瓴人工智能学院简介.txt', 'r', encoding='utf-8').read()
txt_list = jieba.lcut(txt)
txt_list_1 = list(filter(lambda x:len(x)>1,txt_list))

con = Counter(txt_list_1)

con_list = sorted(con.items(),key=lambda x: -x[1])

for i in con_list[:15]:
    print("{0:<10}{1:>5}".format(i[0],i[1]))