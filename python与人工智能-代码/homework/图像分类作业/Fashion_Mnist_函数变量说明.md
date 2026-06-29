# 1. `FashionDataset` 类

```python
class FashionDataset(Dataset):
```

这是自定义数据集类，用来从本地 `data` 文件夹中读取 FashionMNIST 原始压缩文件。

它和 `torchvision.datasets.FashionMNIST(root=...)` 的区别是：这里没有直接使用 torchvision 已封装好的数据集，而是手动读取 `.gz` 文件。因此代码中需要自己写 `load_data()`。

### `__init__(self, datadir, transform, is_train=True)`

```python
def __init__(self, datadir, transform, is_train=True):
    super().__init__()
    self.datadir = datadir
    self.img, self.label = self.load_data(self.datadir, is_train=is_train)
    self.len_data = len(self.img)
    self.transform = transform
```

| 名称 | 作用 |
|---|---|
| `datadir` | 数据文件夹路径，例如 `'data'` |
| `transform` | 每次取图片时执行的图像预处理操作 |
| `is_train` | 是否读取训练集，`True` 读训练集，`False` 读测试集 |
| `self.datadir` | 保存数据文件夹路径 |
| `self.img` | 保存所有图片数据 |
| `self.label` | 保存所有标签数据 |
| `self.len_data` | 数据集样本数量 |
| `self.transform` | 保存图像预处理流程 |

创建对象时，例如：

```python
train_dataset = FashionDataset('data', transform=...)
```

会自动调用 `__init__()`，并在其中调用 `load_data()` 把数据读入内存。

### `__getitem__(self, index)`

```python
def __getitem__(self, index):
    return self.transform(self.img[index]), self.label[index]
```

这个函数规定“如何取出第 `index` 条数据”。

返回内容是：

```text
一张经过 transform 处理后的图片，对应标签
```

例如：

```python
img, label = test_dataset.__getitem__(20)
```

就是取测试集中的第 20 张图片和它的真实标签。

`DataLoader` 在工作时会不断调用这个函数。

### `__len__(self)`

```python
def __len__(self):
    return self.len_data
```

返回数据集长度。`DataLoader` 需要通过它知道数据集中一共有多少个样本。

### `load_data(self, datadir, is_train)`

```python
def load_data(self, datadir, is_train):
```

这个函数负责真正读取 `.gz` 数据文件。

#### 文件列表

```python
files = [
    'train-labels-idx1-ubyte.gz',
    'train-images-idx3-ubyte.gz',
    't10k-labels-idx1-ubyte.gz',
    't10k-images-idx3-ubyte.gz'
]
```

| 文件名 | 作用 |
|---|---|
| `train-labels-idx1-ubyte.gz` | 训练集标签 |
| `train-images-idx3-ubyte.gz` | 训练集图片 |
| `t10k-labels-idx1-ubyte.gz` | 测试集标签 |
| `t10k-images-idx3-ubyte.gz` | 测试集图片 |

#### 读取标签

```python
label = np.frombuffer(lbpath.read(), np.uint8, offset=8)
```

| 部分 | 作用 |
|---|---|
| `lbpath.read()` | 读取整个标签文件的二进制内容 |
| `np.frombuffer(...)` | 把二进制内容解释成 numpy 数组 |
| `np.uint8` | 每个标签用 0-255 范围内的整数存储 |
| `offset=8` | 跳过标签文件前 8 个字节的文件头 |

标签取值为 `0-9`，分别代表 10 个服饰类别。

#### 读取图片

```python
img = np.frombuffer(imgpath.read(), np.uint8, offset=16).reshape(len(label), 28, 28)
```

| 部分 | 作用 |
|---|---|
| `offset=16` | 跳过图片文件前 16 个字节的文件头 |
| `reshape(len(label), 28, 28)` | 把一长串像素重塑成 `[图片数量, 28, 28]` |

因此 FashionMNIST 的原始单张图片大小是：

```text
28 x 28
```

因为它是灰度图，所以经过 `ToTensor()` 后会变成：

```text
1 x 28 x 28
```
# 3. `FashionMnistModel` 类

```python
class FashionMnistModel(nn.Module):
```

这是卷积神经网络模型类，用于把输入图片分类到 10 个 FashionMNIST 类别中。


### 卷积层

```python
self.conv1 = nn.Conv2d(in_channels=1, out_channels=20, kernel_size=3, stride=1, padding=0)
```

| 参数 | 作用 |
|---|---|
| `in_channels=1` | 输入通道数。FashionMNIST 是灰度图，所以是 1 |
| `out_channels=20` | 输出通道数，也可以理解为输出 20 张特征图 |
| `kernel_size=3` | 卷积核大小为 `3x3` |
| `stride=1` | 卷积核每次移动 1 格 |
| `padding=0` | 不在图片边缘补 0 |

输入 `[batch, 1, 28, 28]` 经过该层后变成：

```text
[batch, 20, 26, 26]
```

```python
self.conv2 = nn.Conv2d(in_channels=20, out_channels=8, kernel_size=3, stride=1)
```

第二个卷积层，输入 20 个通道，输出 8 个通道。

```python
self.conv3 = nn.Conv2d(in_channels=8, out_channels=8, kernel_size=2, stride=1, padding=1)
```

第三个卷积层，输入 8 个通道，输出 8 个通道。

注意：如果代码中写成 `nn.Conv3d`，那是不适合这里的。FashionMNIST 是二维图片，应该使用 `nn.Conv2d`。

### 池化层

```python
self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
```

最大池化层，通常让图片高宽减半。它不会改变通道数。

注意：如果代码中写成 `nn.MaxUnpool2d`，那不是普通池化，而是反池化，一般不能直接这样接在卷积层后面用于分类任务。

```python
self.pool2 = nn.AvgPool2d(kernel_size=3, stride=3)
```

平均池化层，用每个区域的平均值代表该区域。

### 全连接层

```python
self.fc1 = nn.Linear(128, 10)
```

| 参数 | 作用 |
|---|---|
| `128` | 输入特征数，即卷积层输出展平后的长度 |
| `10` | 输出类别数，FashionMNIST 一共有 10 类 |

尺寸变化如下：

```text
输入图片: [batch, 1, 28, 28]
conv1 后: [batch, 20, 26, 26]
pool1 后: [batch, 20, 13, 13]
conv2 后: [batch, 8, 11, 11]
pool2 后: [batch, 8, 3, 3]
conv3 后: [batch, 8, 4, 4]
展平后: [batch, 128]
fc1 后: [batch, 10]
```

其中：

```text
128 = 8 * 4 * 4
```
### `forward(self, x)`

```python
def forward(self, x):
    x = F.relu(self.conv1(x))
    x = self.pool1(x)
    x = F.relu(self.conv2(x))
    x = self.pool2(x)
    x = F.relu(self.conv3(x))
    x = x.view(x.shape[0], -1)
    x = self.fc1(x)
    return x
```

这是前向传播函数，规定输入图片如何一步步通过模型。

| 代码 | 作用 |
|---|---|
| `F.relu(...)` | 激活函数，引入非线性能力 |
| `self.conv1(x)` | 第一次卷积提取低级图像特征 |
| `self.pool1(x)` | 降低特征图尺寸 |
| `self.conv2(x)` | 继续提取更复杂特征 |
| `self.pool2(x)` | 进一步降低尺寸 |
| `self.conv3(x)` | 再次卷积提取特征 |
| `x.view(x.shape[0], -1)` | 保留 batch 维度，把每张图的特征展平成一维向量 |
| `self.fc1(x)` | 输出 10 个类别分数 |

注意：`x.view(...)` 必须赋值给 `x`，否则不会改变后续传入全连接层的张量。

```python
x = x.view(x.shape[0], -1)
```

## 4. `Model` 类

```python
class Model():
```

这是训练与测试封装类，不是真正的神经网络模型。真正的模型是 `FashionMnistModel`。

### `__init__(self)`

```python
self.lr = 0.01
self.epoches = 20
self.model_save_path = './model'
self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
self.model = FashionMnistModel().to(self.device)
self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
self.loss_function = nn.CrossEntropyLoss()
```

| 名称 | 作用 |
|---|---|
| `self.lr` | 学习率，控制参数每次更新的步长 |
| `self.epoches` | 训练轮数，这里是 20 轮 |
| `self.model_save_path` | 模型参数保存目录 |
| `self.device` | 训练设备，优先使用 GPU，否则使用 CPU |
| `self.model` | 创建 CNN 模型，并放到指定设备上 |
| `self.optimizer` | Adam 优化器，用于更新模型参数 |
| `self.loss_function` | 交叉熵损失函数，用于多分类任务 |

`CrossEntropyLoss` 要求：

```text
output: [batch_size, 10]
target: [batch_size]
```

其中 `target` 是类别编号，不需要 one-hot 编码。

### `_save_model(self, epoch)`

```python
torch.save(self.model.state_dict(), '%s/%s.pth' % (self.model_save_path, epoch))
```

保存模型参数到 `./model/epoch.pth`。

`state_dict()` 中保存的是模型的权重和偏置，不保存完整训练过程。

### `_load_model(self, epoch)`

```python
self.model.load_state_dict(torch.load('%s/%s.pth' % (self.model_save_path, epoch), map_location=self.device))
```

从指定 `.pth` 文件中加载模型参数。


### `train(self, train_loader, test_loader)`

```python
def train(self, train_loader, test_loader):
```

训练模型。

核心流程：

```python
for epoch in range(self.epoches):
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(self.device), target.long().to(self.device)
        self.optimizer.zero_grad()
        output = self.model(data)
        loss = self.loss_function(output, target)
        loss.backward()
        self.optimizer.step()
```

| 代码 | 作用 |
|---|---|
| `for epoch in range(...)` | 按轮数训练 |
| `for batch_idx, (data, target) in enumerate(train_loader)` | 每次从 DataLoader 取一个 batch |
| `data.to(self.device)` | 把图片送到 CPU 或 GPU |
| `target.long()` | 把标签转成整数类别类型，适配 `CrossEntropyLoss` |
| `optimizer.zero_grad()` | 清空上一轮梯度 |
| `output = self.model(data)` | 前向传播，得到类别分数 |
| `loss = ...` | 计算预测和真实标签之间的损失 |
| `loss.backward()` | 反向传播，计算梯度 |
| `optimizer.step()` | 根据梯度更新参数 |
| `loss.item()` | 取出普通数值形式的 loss，方便记录或打印 |

每训练完一轮，会调用：

```python
self.test(test_loader)
```

用于查看测试集效果。

每 5 轮保存一次模型：

```python
if (epoch + 1) % 5 == 0:
    self._save_model(epoch + 1)
```

### `test(self, test_loader)`

```python
def test(self, test_loader):
```

测试模型在测试集上的准确率。

核心代码：

```python
with torch.no_grad():
    for data, target in test_loader:
        output = self.model(data)
        pred = output.argmax(dim=1, keepdim=True)
        correct += pred.eq(target.view_as(pred)).sum().item()
```

| 代码 | 作用 |
|---|---|
| `torch.no_grad()` | 测试时不计算梯度，节省内存和计算量 |
| `output.argmax(dim=1)` | 从 10 个类别分数中取最大值对应的类别编号 |
| `target.view_as(pred)` | 把真实标签形状调整得和预测结果一致 |
| `pred.eq(...)` | 判断预测是否正确 |
| `.sum().item()` | 统计正确数量并转成普通 Python 数值 |

## 5. 定义 DataLoader 的 cell

```python
train_dataset = FashionDataset(
    'data',
    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
)
```

这段代码创建训练集。

| 名称 | 作用 |
|---|---|
| `'data'` | 数据文件夹路径，相当于很多教程中的 `root='./data'` |
| `transforms.Compose(...)` | 把多个图像预处理操作组合起来 |
| `transforms.ToTensor()` | 把 `[28, 28]` 的 numpy 图片转成 `[1, 28, 28]` 的 Tensor，并把像素缩放到 `0-1` |
| `transforms.Normalize((0.1307,), (0.3081,))` | 对灰度图做标准化处理 |

标准化公式大致是：

```text
新值 = (原值 - 0.1307) / 0.3081
```

```python
train_loader = DataLoader(train_dataset, batch_size=320, shuffle=True, num_workers=0)
```

| 参数 | 作用 |
|---|---|
| `train_dataset` | 数据来源 |
| `batch_size=320` | 每次取 320 张图片进行训练 |
| `shuffle=True` | 每轮训练前打乱数据顺序 |
| `num_workers=0` | 不额外开子进程读取数据，Windows + Jupyter 中更稳定 |

每次从 `train_loader` 中取出的数据形状通常是：

```text
data: [320, 1, 28, 28]
target: [320]
```

```python
test_dataset = FashionDataset(..., is_train=False)
```

创建测试集。`is_train=False` 表示读取测试文件：

```text
t10k-labels-idx1-ubyte.gz
t10k-images-idx3-ubyte.gz
```

```python
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=0)
```

测试集一般不需要打乱，所以 `shuffle=False`。


## 6. 训练模型的 cell

```python
model = Model()
model.train(train_loader, test_loader)
```

| 名称 | 作用 |
|---|---|
| `model = Model()` | 创建训练封装对象，内部会创建 CNN、优化器、损失函数 |
| `model.train(...)` | 开始训练，并在每轮后测试模型效果 |

注意：这里的 `model` 是训练封装类 `Model` 的实例，不是直接的 CNN。真正的 CNN 存在：

```python
model.model
```

## 7. 加载模型参数

```python
model2 = FashionMnistModel()
state_dict = torch.load("./model/15.pth")
model2.load_state_dict(state_dict)
```

| 名称 | 作用 |
|---|---|
| `model2` | 新创建的 CNN 模型 |
| `state_dict` | 从文件中读取的模型参数字典 |
| `load_state_dict(...)` | 把保存的参数加载进 `model2` |

注意：加载参数前，`model2` 的网络结构必须和保存参数时完全一致。

## 8. 类别名称

```python
label_classes = [
    'T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
    'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot'
]
```

这是 FashionMNIST 的 10 个类别名称。标签编号 `0-9` 分别对应列表中的 10 个字符串。

## 9. `inference(model, img)` 函数

```python
def inference(model, img):
    model.eval()
    img = img.unsqueeze(dim=0)
    output = model(img)
    pred = output.argmax(dim=1, keepdim=True)
    return pred.squeeze().numpy()
```

这个函数用于单张图片推理。

| 代码 | 作用 |
|---|---|
| `model.eval()` | 切换到评估模式 |
| `img.unsqueeze(dim=0)` | 给单张图片增加 batch 维度 |
| `output = model(img)` | 前向传播，得到 10 个类别分数 |
| `argmax(dim=1)` | 找到分数最高的类别编号 |
| `squeeze()` | 去掉多余维度 |
| `.numpy()` | 转成 numpy 数值 |

单张图片原本形状是：

```text
[1, 28, 28]
```

经过 `unsqueeze(dim=0)` 后变成：

```text
[1, 1, 28, 28]
```

第一个 `1` 是 batch size，第二个 `1` 是灰度通道数。

