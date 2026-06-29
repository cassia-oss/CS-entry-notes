# Pytorch实现逻辑回归.py 函数、变量及作用说明

这份脚本使用 PyTorch 手动实现了一个二分类逻辑回归模型。整体流程是：

1. 导入依赖库
2. 定义逻辑回归模型 `LogisticsRegression`
3. 定义训练与测试封装类 `Logistics_Model`
4. 使用 `create_linear_data()` 生成模拟二分类数据
5. 训练模型、绘制 loss 曲线、测试准确率、打印模型参数

---

## 1. 导入库与环境设置

```python
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
```

### 变量与模块说明

| 名称 | 作用 |
|---|---|
| `torch` | PyTorch 主库，用于张量计算、自动求导、模型训练 |
| `torch.nn` | PyTorch 神经网络模块，提供 `Module`、`Parameter` 等工具 |
| `numpy` | 用于生成模拟数据、打乱索引等 |
| `matplotlib.pyplot` | 用于绘制训练过程中的 loss 曲线 |
| `os.environ["KMP_DUPLICATE_LIB_OK"]` | 临时解决某些环境中 numpy / torch 的 OpenMP 冲突问题 |

---

## 2. `LogisticsRegression` 类

```python
class LogisticsRegression(nn.Module):
```

这个类是真正的逻辑回归模型。它继承自 `nn.Module`，因此可以被 PyTorch 管理参数、执行前向传播、自动计算梯度。

### `__init__(self, in_dim)`

```python
def __init__(self, in_dim):
    super().__init__()
    self.w = nn.Parameter(torch.zeros(in_dim, 1))
    self.b = nn.Parameter(torch.zeros(1))
```

#### 参数说明

| 名称 | 作用 |
|---|---|
| `in_dim` | 输入特征的维度，也就是每个样本有几个特征 |
| `self.w` | 逻辑回归的权重参数，形状是 `[in_dim, 1]` |
| `self.b` | 偏置参数，形状是 `[1]` |

#### 关键点

`nn.Parameter(...)` 表示这是一个需要训练的参数。PyTorch 会自动把它加入模型参数列表中，因此：

```python
self.model.parameters()
```

会包含 `self.w` 和 `self.b`。

---

### `sigmoid(self, z)`

```python
def sigmoid(self, z):
    return 1 / (1 + torch.exp(-z))
```

这是 sigmoid 函数，用来把任意实数映射到 `0` 到 `1` 之间。

逻辑回归中，输出值可以理解为属于正类的概率：

```text
y_hat 越接近 1，越倾向于预测为正类
y_hat 越接近 0，越倾向于预测为负类
```

---

### `forward(self, x)`

```python
def forward(self, x):
    z = torch.mm(x, self.w) + self.b
    y_hat = self.sigmoid(z)
    return y_hat
```

这是模型的前向传播函数。

#### 输入输出说明

| 名称 | 形状 | 作用 |
|---|---|---|
| `x` | `[样本数, in_dim]` | 输入数据，每一行是一个样本 |
| `self.w` | `[in_dim, 1]` | 权重参数 |
| `self.b` | `[1]` | 偏置参数 |
| `z` | `[样本数, 1]` | 线性计算结果 |
| `y_hat` | `[样本数, 1]` | sigmoid 后的预测概率 |

核心公式是：

```text
z = xw + b
y_hat = sigmoid(z)
```

---

## 3. `Logistics_Model` 类

```python
class Logistics_Model():
```

这个类不是神经网络本身，而是一个训练和测试的封装类。它里面包含模型、优化器、训练轮数、学习率等。

---

### `__init__(self, in_dim)`

```python
self.learning_rate = 0.0001
self.epoch = 2000
self.model = LogisticsRegression(in_dim)
self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.learning_rate)
```

#### 变量说明

| 名称 | 作用 |
|---|---|
| `self.learning_rate` | 学习率，控制每次参数更新的步长 |
| `self.epoch` | 训练轮数，这里训练 2000 轮 |
| `self.model` | 逻辑回归模型实例 |
| `self.optimizer` | 优化器，这里使用随机梯度下降 SGD |

`self.model.parameters()` 会把模型中的 `w` 和 `b` 交给优化器管理。

---

### `train(self, x, y)`

```python
def train(self, x, y):
    losses = []
    for epoche in range(self.epoch):
        self.optimizer.zero_grad()
        y_hat = self.model(x)
        loss = -torch.mean(y * torch.log(y_hat) + (1 - y) * torch.log(1 - y_hat))
        loss.backward()
        self.optimizer.step()
        losses.append(loss.item())
    return losses
```

这是训练函数。

#### 输入输出说明

| 名称 | 作用 |
|---|---|
| `x` | 训练数据，形状一般是 `[训练样本数, in_dim]` |
| `y` | 真实标签，形状一般是 `[训练样本数, 1]`，取值为 0 或 1 |
| `losses` | 保存每一轮训练后的 loss 数值，用于画图 |

#### 每一步的作用

```python
self.optimizer.zero_grad()
```

清空上一轮残留的梯度。PyTorch 默认会累加梯度，所以每轮训练前要清零。

```python
y_hat = self.model(x)
```

执行前向传播，得到预测概率。

```python
loss = -torch.mean(y * torch.log(y_hat) + (1 - y) * torch.log(1 - y_hat))
```

计算二分类交叉熵损失。预测越接近真实标签，loss 越小。

```python
loss.backward()
```

反向传播，计算 loss 对 `w`、`b` 的梯度。

```python
self.optimizer.step()
```

优化器根据梯度更新参数。

```python
losses.append(loss.item())
```

把当前 loss 从 Tensor 转成普通 Python 数字，保存起来用于画图。

---

### `test(self, x, y)`

```python
def test(self, x, y):
    y_hat = self.model(x)
    prediction = (y_hat >= 0.5).float()
    accuracy = torch.mean((prediction == y).float())
    return prediction, accuracy
```

这是测试函数，用训练好的模型预测测试集，并计算准确率。

#### 变量说明

| 名称 | 作用 |
|---|---|
| `y_hat` | 模型输出的概率值 |
| `prediction` | 根据阈值 0.5 得到的预测类别，结果为 0 或 1 |
| `accuracy` | 预测正确的比例 |

```python
prediction = (y_hat >= 0.5).float()
```

如果预测概率大于等于 0.5，就预测为 1，否则预测为 0。

```python
accuracy = torch.mean((prediction == y).float())
```

先判断每个样本是否预测正确，再取平均值作为准确率。

---

## 4. `create_linear_data(data_size, in_dim)` 函数

这个函数用于生成一个模拟的二分类数据集。

```python
def create_linear_data(data_size, in_dim):
```

### 参数说明

| 名称 | 作用 |
|---|---|
| `data_size` | 总样本数量 |
| `in_dim` | 每个样本的特征维度 |

### 随机种子

```python
np.random.seed(426)
torch.manual_seed(426)
torch.cuda.manual_seed(426)
```

固定随机种子，使每次运行生成的数据尽量一致，方便复现实验结果。

---

### 正负样本数量

```python
m_pos = data_size // 2
m_neg = data_size - m_pos
```

| 名称 | 作用 |
|---|---|
| `m_pos` | 正类样本数量 |
| `m_neg` | 负类样本数量 |

如果 `data_size = 200`，那么：

```text
m_pos = 100
m_neg = 100
```

---

### 初始化数据矩阵

```python
X = np.zeros((in_dim, data_size))
Y = np.zeros((1, data_size))
```

| 名称 | 形状 | 作用 |
|---|---|---|
| `X` | `[in_dim, data_size]` | 保存所有样本的特征 |
| `Y` | `[1, data_size]` | 保存所有样本的标签 |

注意：后面会执行 `X.T`，所以最终送入模型的数据形状会变成：

```text
[data_size, in_dim]
```

---

### 生成正类样本

```python
x1 = np.random.normal(loc=-1, scale=3, size=(1, m_pos))
X[0:1, 0:m_pos] = x1
X[1:2, 0:m_pos] = 2 * x1 + 10 + 0.1 * x1 ** 2
X[1:2, 0:m_pos] += np.random.normal(loc=0, scale=5, size=(1, m_pos))
Y[0, 0:m_pos] = 1
```

这里生成正类样本。

| 代码 | 作用 |
|---|---|
| `np.random.normal(loc=-1, scale=3, size=(1, m_pos))` | 从均值为 -1、标准差为 3 的正态分布中生成第一维特征 |
| `X[0:1, 0:m_pos] = x1` | 把 `x1` 放入第 0 个特征维度 |
| `X[1:2, 0:m_pos] = ...` | 根据 `x1` 生成第 1 个特征维度 |
| `+= np.random.normal(...)` | 给数据加入噪声，使分类任务不至于过于简单 |
| `Y[0, 0:m_pos] = 1` | 正类标签设为 1 |

---

### 生成负类样本

```python
x1 = np.random.normal(loc=1, scale=3, size=(1, m_neg))
X[0:1, -m_neg:] = x1
X[1:2, -m_neg:] = 2 * x1 - 5 - 0.1 * x1 ** 2
X[1:2, -m_neg:] += np.random.normal(loc=0, scale=5, size=(1, m_neg))
```

这里生成负类样本。

负类和正类的主要区别是第二维特征的生成公式不同，所以两类点在二维平面上的分布位置不同。

负类标签默认保持为 0，因为 `Y` 一开始就是全 0。

---

### 转换成 PyTorch Tensor

```python
X = torch.Tensor(X.T)
Y = torch.Tensor(Y.T)
```

原来的 `X` 形状是：

```text
[in_dim, data_size]
```

转置后变成：

```text
[data_size, in_dim]
```

这正好符合模型输入要求：每一行是一个样本。

---

### 打乱数据

```python
shuffled_index = np.random.permutation(data_size)
shuffled_index = torch.from_numpy(shuffled_index).long()
X = X[shuffled_index]
Y = Y[shuffled_index]
```

| 代码 | 作用 |
|---|---|
| `np.random.permutation(data_size)` | 生成一个随机排列的索引 |
| `torch.from_numpy(...)` | 把 numpy 数组转换成 PyTorch Tensor |
| `.long()` | 转成整数索引类型 |
| `X[shuffled_index]` | 按随机索引打乱样本顺序 |

因为前面是先生成全部正类，再生成全部负类，所以必须打乱，否则训练集和测试集可能类别分布不均匀。

---

### 划分训练集和测试集

```python
split_index = int(data_size * 0.7)
x_train = X[:split_index]
y_train = Y[:split_index]
x_test = X[split_index:]
y_test = Y[split_index:]
```

这里按照 70% / 30% 划分数据：

```text
训练集：前 70%
测试集：后 30%
```

如果 `data_size = 200`，那么：

```text
训练集 140 个样本
测试集 60 个样本
```

---

## 5. 主程序部分

```python
data_size = 200
in_dim = 3
x_train, y_train, x_test, y_test = create_linear_data(data_size, in_dim)
```

### 变量说明

| 名称 | 作用 |
|---|---|
| `data_size` | 总样本数，这里是 200 |
| `in_dim` | 输入特征维度，这里是 3 |
| `x_train` | 训练数据 |
| `y_train` | 训练标签 |
| `x_test` | 测试数据 |
| `y_test` | 测试标签 |

注意：当前数据生成函数只明显使用了 `X[0]` 和 `X[1]` 两个特征维度。因为 `in_dim = 3`，所以第三个特征维度会保持为 0。也就是说，模型输入是 3 维，但真正有信息的主要是前 2 维。

---

### 创建并训练模型

```python
logistics = Logistics_Model(in_dim)
losses = logistics.train(x_train, y_train)
```

| 名称 | 作用 |
|---|---|
| `logistics` | 训练/测试封装对象 |
| `losses` | 训练过程中每一轮的损失值 |

---

### 绘制 loss 曲线

```python
plt.figure()
plt.scatter(np.arange(len(losses)), losses, marker='o', c='green')
plt.show()
```

这部分用散点图显示训练过程中 loss 的变化。

| 代码 | 作用 |
|---|---|
| `plt.figure()` | 创建新图像窗口 |
| `np.arange(len(losses))` | 生成横坐标，表示第几轮训练 |
| `losses` | 纵坐标，表示每一轮的 loss |
| `marker='o'` | 点的形状为圆点 |
| `c='green'` | 颜色为绿色 |
| `plt.show()` | 显示图像 |

---

### 测试模型

```python
prediction, accuracy = logistics.test(x_test, y_test)
print('测试集上accuracy:{}'.format(accuracy))
```

| 名称 | 作用 |
|---|---|
| `prediction` | 模型对测试集每个样本的预测结果 |
| `accuracy` | 测试集准确率 |

---

### 打印模型参数

```python
for name, parameter in logistics.model.named_parameters():
    print(name, parameter)
```

这会打印模型中所有可训练参数的名字和值。

本模型中主要有两个参数：

```text
w: 权重参数
b: 偏置参数
```

`named_parameters()` 会返回参数名和参数本身，方便检查模型训练后的结果。

---

## 6. 整体数据流总结

```text
create_linear_data()
生成 x_train, y_train, x_test, y_test

Logistics_Model(in_dim)
创建逻辑回归模型和优化器

logistics.train(x_train, y_train)
前向传播 -> 计算 loss -> 反向传播 -> 更新参数

logistics.test(x_test, y_test)
预测测试集 -> 根据 0.5 阈值分类 -> 计算准确率
```

---

## 7. 需要特别注意的地方

### 1. 这是二分类，不是多分类

模型最后输出的是一个概率值：

```text
接近 1：预测为正类
接近 0：预测为负类
```

所以标签应该是 `0` 或 `1`。

### 2. `in_dim = 3` 但数据主要只有两个有效特征

当前代码中只对 `X[0]` 和 `X[1]` 赋了有意义的值，第三个维度大多为 0。因此如果只是为了二维分类实验，`in_dim` 也可以设为 2，并对应调整数据矩阵。

### 3. `torch.log(y_hat)` 可能有数值稳定性问题

如果 `y_hat` 非常接近 0 或 1，`torch.log(...)` 可能产生极端值。更标准的做法通常是使用 PyTorch 自带的损失函数，例如：

```python
nn.BCELoss()
```

或者让模型输出未经过 sigmoid 的 logits，然后使用：

```python
nn.BCEWithLogitsLoss()
```

不过对于本作业的小规模实验，当前写法通常可以运行。

### 4. `Logistics_Model` 不是 `nn.Module`

`LogisticsRegression` 才是真正的 PyTorch 模型；`Logistics_Model` 只是把训练和测试过程包起来的普通 Python 类。