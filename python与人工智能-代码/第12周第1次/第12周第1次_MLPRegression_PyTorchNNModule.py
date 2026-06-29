import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

class MLPRegression(nn.Module):
    def __init__(self, input_dim, hidden_dim): #构造函数，需要调用nn.Mudule的构造函数
        super().__init__()       #等价于nn.Module.__init__()
        self.linear_hidden = nn.Linear(input_dim, hidden_dim)
        #nn.Parameter(torch.randn(input_dim + 1, hidden_dim))
        self.linear_output = nn.Linear(hidden_dim, 1) # four-dimensational ouptut
        #self.one_layer = nn.Linear(input_dim, 1)
        #self.activation = nn.Sigmoid() #Identity()
        self.activation = nn.Identity()

    def forward(self, x):
        #x = torch.cat([x, torch.ones((x.shape[0],1))], dim = 1)
        hidden_layer_output = self.activation(self.linear_hidden(x))
        output = self.activation(self.linear_output(hidden_layer_output))
        #output = self.activation(self.one_layer(x))
        return output


class MLP_Model():
    def __init__(self, input_dim, lr=0.01, epoches=10000, hidden_dim=3):
        """
        创建模型和优化器，初始化线性模型和优化器超参数
        """       
        # 模型超参数
        self.learning_rate = lr
        self.epoches = epoches
        self.hidden_dim = hidden_dim

        # 模型
        self.model = MLPRegression(input_dim, self.hidden_dim)
        # 优化器
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.learning_rate)
        # 损失函数
        self.loss_function = torch.nn.MSELoss()
    
    def train(self, x, y):
        """
        训练模型
        输入:
            x: 训练数据
            y: 回归真值
        返回: 
            losses: 所有迭代中损失函数值
        """
        losses = []

        for epoch in range(self.epoches):
            prediction = self.model(x)
            loss = self.loss_function(prediction, y)           

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            losses.append(loss.item())

            if epoch % 500 == 0:
                print("epoch: {}, loss is: {}".format(epoch, loss.item()))

        if x.shape[1]==1:
            plt.figure()
            plt.scatter(x.data, y.data)
            plt.scatter(x.data, prediction.data, color="r")
            plt.show()

        return losses
        
    def test(self, x, y, if_plot = True):
        """
        用训练好的模型做测试
        输入:
            x: 测试数据
            y: 测试数据的回归真值
        返回:
            prediction: 测试数据的预测值
        """
        prediction = self.model(x)
        testMSE = self.loss_function(prediction, y)
        
        if if_plot and x.shape[1]==1:
            plt.figure()
            plt.scatter(x.data, y.data)
            plt.scatter(x.data, prediction.data, color="r")
            plt.show()

        return prediction, testMSE


def create_data(data_size, input_dim, if_plot=True):
    """
    为线性模型生成数据
    输入:
        data_size: 样本数量
        input_dim: 输入维度（特征数）
    返回:
        x_train: 训练数据
        y_train: 训练数据回归真值
        x_test: 测试数据
        y_test: 测试数据回归真值
    """
    # 固定随机数生成器种子，保证每次运行结果一致
    np.random.seed(1125)
    torch.manual_seed(1125)
    torch.cuda.manual_seed(1125)

    # 生成随机数据
    x = 7.0 * torch.rand(data_size, in_dim) + 0.15
    random_error = 0.1 * torch.rand(data_size, 1) - 0.05
    y = 0.25 * torch.sum(torch.log(x), dim=1, keepdim=True) + 0.5 + random_error

    #print(y)

    # 划分训练集与测试集
    shuffled_index = np.random.permutation(data_size)
    shuffled_index = torch.from_numpy(shuffled_index).long()
    x = x[shuffled_index]
    y = y[shuffled_index]
    split_index = int(data_size * 0.7)
    x_train = x[:split_index]     # 训练集 x
    y_train = y[:split_index]     # 训练集 y
    x_test = x[split_index:]      # 测试集 x
    y_test = y[split_index:]      # 测试集 y
    
    if if_plot and input_dim == 1:
        plt.figure()
        plt.scatter(x_train.numpy(),y_train.numpy())
        plt.show()
    return x_train, y_train, x_test, y_test

# 生成数据
data_size = 100
in_dim = 1
x_train, y_train, x_test, y_test = create_data(data_size, in_dim, if_plot=True)

# 线性回归模型实例化
MLP = MLP_Model(in_dim, lr=0.1, epoches=20000, hidden_dim=10)
# 模型训练
losses = MLP.train(x_train, y_train)

# 画图
plt.figure()
plt.scatter(np.arange(len(losses)), losses, marker='o', c='green')
# plt.savefig('loss.jpg')   # 保存图片
#plt.show()
# 模型测试
prediction, testMSE = MLP.test(x_test, y_test)
print('测试集上MSE损失值:{}'.format(testMSE))

for name,parameter in MLP.model.named_parameters():
    print(name, parameter)

sys.exit(0)