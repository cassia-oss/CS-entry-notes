#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'defaultstr'
"""
基于字符级别RNN的姓名分类

参考：https://github.com/spro/practical-pytorch
"""

from tqdm import tqdm
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class RNN(nn.Module):
    """
    定义RNN模型
    """
    def __init__(self, vocab_size, embedding_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size
        self.embeddings = nn.Embedding(vocab_size, embedding_size)
        self.i2h = nn.Linear(embedding_size + hidden_size, hidden_size)
        self.non_linear = nn.ReLU()
        self.output = nn.Linear(embedding_size + hidden_size, output_size)

    def forward(self, input, hidden=None):
        input_embeddings = self.embeddings(input)
        if hidden is None:
            hidden = torch.zeros(1, self.hidden_size)
        combined = torch.cat((input_embeddings, hidden), 1)
        hidden = self.i2h(combined)
        hidden = self.non_linear(hidden)
        output = self.output(combined)
        return output, hidden


class RNNClassifier():
    def __init__(self, char2index, output_dim, embedding_dim=128, hidden_dim=128):
        """
        创建模型和优化器，初始RNN模型和优化器超参数
        """
        self.lr = 0.001
        self.epoches = 20

        self.num_chars = len(char2index)  # 用于将字符映射到整数的字典，其大小为字典大小
        self.char2index = char2index

        self.rnn = RNN(self.num_chars, embedding_dim, hidden_dim, output_dim)
        self.optimizer = torch.optim.SGD(self.rnn.parameters(), lr=self.lr)
        self.loss_function = nn.CrossEntropyLoss()

    def train(self, X, y):
        """
        训练模型
        输入:
            X: 训练数据,(N,),每个元素是包含名字信息的字符串
            y: 训练数据的真实分类, (N, 1), 每个元素是名字所属的类别
        返回:
            epoch_losses: 每个epoch的平均损失函数值
        """
        epoch_losses = []
        data_size = X.shape[0]
        for epoch in range(self.epoches):
            losses = []

            # 每轮训练前打乱数据的顺序
            shuffled_index = np.random.permutation(data_size)
            X, y = X[shuffled_index], y[shuffled_index]

            for i in tqdm(range(data_size)):
                # x.shape = (length, 1)
                x = torch.tensor([[self.char2index[c]] for c in X[i]], dtype=torch.long)
                # y_true.shape = (1, ), y 是一个{0, 1, ..., 17}范围内的整数，代表x属于的分类
                y_true = torch.tensor(y[i])

                # *循环*神经网络！
                hidden = None
                output = None
                for j in range(x.shape[0]):
                    output, hidden = self.rnn(x[j], hidden)
                # output.shape = (1, 18)
                loss = self.loss_function(output, y_true.to(torch.int64))

                # 反向传播，更新参数
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                # 记录loss
                losses.append(loss.item())

            # 计算每个epoch的平均loss并输出
            epoch_losses.append(sum(losses) / data_size)
            print("epoch: {}, avg loss is: {}".format(epoch, epoch_losses[-1]))

        return epoch_losses

    def test(self, X, y):
        """
        用训练好的模型做测试
        输入:
            X: 测试数据,(N,),每个元素是包含名字信息的字符串
            y: 测试数据的真实分类, (N, 1), 每个元素是名字所属的类别
        返回:
            y_pred: 测试数据的预测分类结果
            accuracy: 分类准确率
        """
        data_size = X.shape[0]
        y_pred = torch.empty(y.shape).long()  # 预测分类与真实分类的形状相同
        for i in range(data_size):
            x = torch.tensor([[self.char2index[c]] for c in X[i]], dtype=torch.long)

            # *循环*神经网络！
            hidden = None
            for j in range(x.shape[0]):
                output, hidden = self.rnn(x[j], hidden)
            # output.shape = (1, 18)
            top_n, top_i = output.topk(1)
            y_pred[i] = top_i[0]

        # 将y转化为tensor,并计算accuracy
        accuracy = self.accuracy(torch.from_numpy(y), y_pred)

        return y_pred, accuracy

    def accuracy(self, y_true, y_pred):
        return torch.where(y_true == y_pred, 1.0, 0.0).mean().item()


def read_data(filename):
    """
    读入数据
    输入：
        filename: 数据文件的文件名
    返回:
        X: 作为特征的人名字符串
        y: 作为预测目标的国名对应的类别（整数）
        index2char: 表示字符的整数到字符的映射
        char2index: 字符到表示字符的整数的映射
        index2country: 表示国名类别的整数到国名的映射
        country2index: 国名到表示国名类别的整数的映射
    """
    X = list()
    y = list()

    with open(filename, 'r') as fin:
        for line in fin:
            # print(line)
            name, country = line.strip().split(',')
            X.append(name)
            y.append(country)

    # 构造字符到整数的映射
    index2char = sorted(set(''.join(X)))
    char2index = {c: i for i, c in enumerate(index2char)}
    X = np.array(X)

    # 构造country到整数的映射
    index2country = sorted(set(y))
    country2index = {c: i for i, c in enumerate(index2country)}
    y = np.array([[country2index[c]] for c in y])

    return X, y, index2char, char2index, index2country, country2index


def split_data(X, y, split_ratio=0.7):
    """
    划分训练集和测试集
    输入:
        X: 特征
        y: 预测目标
        split_ration: 训练集所占比例(0 < split_ratio < 1)
    返回:
        X_train, y_train: 训练集特征和预测目标
        X_test, y_test: 测试集特征和预测目标
    """
    data_size = len(X)
    shuffled_index = np.random.permutation(data_size)
    X, y = X[shuffled_index], y[shuffled_index]

    assert(0.0 < split_ratio < 1.0)
    split_index = int(data_size * split_ratio)
    X_train = X[:split_index]
    y_train = y[:split_index]
    X_test = X[split_index:]
    y_test = y[split_index:]
    return X_train, y_train, X_test, y_test


def plot_confusion_matrix(y_pred, y_true, country2index):
    """
    绘制混淆矩阵
    输入:
        y_pred: 预测结果
        y_true: 真实分类
        country2index: 保存国名到表示类别的整数的映射关系的字典
    """
    n_categories = len(country2index)
    confusion = np.zeros((n_categories, n_categories))

    # confusion[i, j]： 将第i类样本预测为第j类样本的次数
    for i in range(len(y_true)):
        confusion[y_true[i][0], y_pred[i][0]] += 1.

    # 按行归一化，归一化后confusion[i, j]为将第i类样本预测为第j类样本的概率
    confusion = confusion / confusion.sum(axis=1).reshape(18, 1)

    # 绘制混淆矩阵
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(confusion)
    fig.colorbar(cax)

    ax.set_xticklabels([''] + index2country, rotation=90)
    ax.set_yticklabels([''] + index2country)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.show()



# 读取数据
X, y, index2char, char2index, index2country, country2index = read_data('names_of_different_countries.txt')
# 划分训练集和测试集
X_train, y_train, X_test, y_test = split_data(X, y)

# 定义RNN分类器
classifier = RNNClassifier(char2index, len(country2index))

# 训练RNN分类器
losses = classifier.train(X_train, y_train)

# 绘制损失函数变化曲线
plt.figure()
plt.plot(losses)
plt.show()

# 在训练集上进行测试
y_pred, accuracy = classifier.test(X_train, y_train)
print("Accuracy on training set: {}".format(accuracy))

# 绘制混淆矩阵
plot_confusion_matrix(y_pred, y_train, country2index)

# 在测试集上进行测试
y_pred, accuracy = classifier.test(X_test, y_test)
print("Accuracy on test set: {}".format(accuracy))

# 绘制混淆矩阵
plot_confusion_matrix(y_pred, y_test, country2index)
