击球手击球。你马上开始跑，预测球的轨迹，你追踪它并调整你的移动，最后抓住它（掌声雷动）。其实你一直在预测未来，不管是接住朋友说话的下一句，还是在早餐的时候预测肉包的味道。这一节，我们将讨论**recurrent neural network（递归神经网络）** ，一类可以预测未来的网络（当然只是一定程度上）。他们可以分析时间序列数据如股票价格，并告诉你什么时候买或者卖。在无人驾驶系统中，他们可以预测车子轨迹并帮助避免意外发生。更常见的，它们可以处理任意长度的序列，而不是像我们迄今为止讨论过的所有网络那样固定大小的输入。比如，他们可以将句子，文档或者声音样本作为输入，让他们成为了自然语言处理如自动翻译，语音转文本或者情感分析（如读取影评并提取观众的感受）的实用工具。

此外，RNN能预测的能力也让他们有令人意外的创造力。你可以让他们预测旋律中最有可能的下一个音符，然后随机的选择其中的音符并播放。然后向网络询问下一个最可能的音符，播放它，并一次又一次地重复该过程。在你知道之前，您的网络将构成一个旋律，例如由Google的[Magenta](https://magenta.tensorflow.org/)项目制作的[旋律](https://cdn2.vox-cdn.com/uploads/chorus_asset/file/6577761/Google_-_Magenta_music_sample.0.mp3)。 同样，RNN可以[生成句子](https://karpathy.github.io/2015/05/21/rnn-effectiveness/)，[图像标题](https://arxiv.org/pdf/1411.4555v2.pdf)等等。 结果并不完全是莎士比亚或莫扎特，但谁知道他们将在几年后产生什么呢？

这节我们将研究下RNN背后的基本概念，他们面临的主要问题（也就是，梯度消失\爆炸），和解决它的常用方案：LSTM和GRU单元。一路上，我们将一如既往地展示如何使用TensorFlow实现RNN。 最后，我们将看一下机器翻译系统的架构。

## 递归神经元 

到目前为止，我们主要研究了前馈神经网络，其中激活只在一个方向上流动，从输入层到输出层。一个递归的神网看起来非常像一个前馈神经网络，除了他还有向后指向的连接。我们来看下最简单的RNN，它由一个接收输入的神经元组成，产生一个输出发送回自身，如图14-1（左）所示。在每个时间阶段（也叫帧），这个*递归神经元*接收输入**x(t)**,以及来自前一时间段它自己的输出，**y(t-1)**。我们可以在时间轴上表示这个小网络，如图14-1（右）所示。这称为**通过时间展开网络（unrolling the network through time ）**。

![1530668734(1).png](https://upload-images.jianshu.io/upload_images/3509189-95e069682b1a7778.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


你可以很容易的创建一个递归神经元。每个时间段 t，每个神经元接收输入向量**x(t)** 和前一个时间段的输出向量**y(t-1)**,如图14-2。注意现在输入和输出都是向量（当只有一个神经元，输出是一个标量）。

![1530668960(1).png](https://upload-images.jianshu.io/upload_images/3509189-085db30f41d750b8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


每个递归神经元有2个权重集：一个给输入**x(t)**,另一个是给前一个时间段的输出**y(t-1)**。称这些权重向量为**wx** ，和**wy**吧。一个单递归神经元的输出可以按照你的预期进行计算，如公式14-1所示（b是偏置项，φ（·）是激活函数，例如ReLU）

![1530669828(1).png](https://upload-images.jianshu.io/upload_images/3509189-38233c2a28220aa7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


就像前馈神经网络一样，我们可以使用前一个等式的矢量化形式一次性计算整个小批量整个层的输出（见公式14-2）

![1530669926(1).png](https://upload-images.jianshu.io/upload_images/3509189-88f57534ef44223b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- Y（t）是m×n neurons矩阵，其包含小批量中每个实例的时间步长t的层输出（m是小批量中的实例数，n个神经元是神经元的数量）。
- X（t）是m×n inputs矩阵，包含所有实例的输入（ninputs是输入要素的数量）。
- Wx是ninputs×n neurons矩阵，包含当前时间步长输入的连接权重
- Wy是n neurons×n neurons矩阵，包含前一时间步的输出的连接权重
- 权重矩阵Wx和Wy通常连接成单个权重矩阵W的形状（ninputs + nneurons）×nneurons（参见公式14-2的第二行）。
- b 是nneurons 大小的向量，包含每个神经元的偏差项

注意Y（t）是X（t）和Y（t-1）的函数，它是X（t-1）和Y（t-2）的函数，它是X的函数（t- 2）和Y（t-3），依此类推。 这使得Y（t）是从时间t = 0开始的所有输入的函数（即，X（0），X（1），...，X（t））。 在第一个时间步，t = 0，没有先前的输出，因此通常假定它们全为零。

## 记忆细胞

由于在时间步t的反复神经元的输出是来自先前时间步的所有输入的函数，你可以认为它具有一种形式的**记忆** 。 跨时间步长保留某些状态的神经网络的一部分称为记忆细胞（或简称为细胞）。单个递归神经元或一层递归神经元是一个非常基本的细胞，但在本章后面我们将讨论一些更复杂和更强大的细胞类型。

通常，在时间步t的单元状态，表示为h（t）（“h”代表“隐藏”），是该时间步的一些输入和前一时间步的状态的函数：h（t） = f（h（t-1），x（t））。 其在时间步长t的输出，表示为y（t），也是先前状态和当前输入的函数。 在我们到目前为止讨论的基本单元的情况下，输出简单地等于状态，但在更复杂的单元中，情况并非总是如此，如图14-3所示。

![1530670730(1).png](https://upload-images.jianshu.io/upload_images/3509189-c88bf64e02d43b15.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 输入和输出序列

一个RNN可以同时地获取一个输入序列并产出一个输出序列（如图14-4 左上角）。比如，这种类型对于预测时间序列如股票价格有效：你喂它在过去N天的价格，它必须转为输出未来一天的价格（即从N - 1天前到明天）。

或者，你可以喂给网络一系列输入，然后忽略所有的输出，除了最后一个（看右上角网络）。换句话说，这是个**序列到向量** 网络。比如你可以喂给网络一个影评对应的一系列的单词，然后网络会输出一个情感分数（如从 -1【讨厌】到 +1【喜欢】）。

相对的，你可以在第一次时间步喂给网络一个单一输入（对其他时间步输入0），让他输出一个序列（看左下角网络）。这是一个**向量到序列**网络。比如，输入可以是个图片，然后输出是图片的标题。

最后，你也可以有一个**序列到向量**网络，叫**encoder** ，然后是**向量到序列**网络，叫**decoder**（如右下角）。例如，你可以用这个网络来翻译一个句子从一个语言到另一个语言。这个两步骤的模型，叫Encoder-Decoder。比使用序列到序列的RNN动态翻译要好得多（如左上角），因为句子的最后一个单词可以影响翻译的第一个单词，所以你需要得到整个句子后才能翻译。

![1530672174(1).png](https://upload-images.jianshu.io/upload_images/3509189-ab57d552033148fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


听起来挺美好，那开始码代码吧！

## TF里的基本RNN

首先我们来实现一个非常简单的RNN模型，不使用任何TF的RNN操作，来更好的理解在背后究竟发生了什么。我们会创建一个RNN，包含一个五个递归神经元的神经层（如图14-2），使用tanh激活函数。我们假设RNN只执行2个时间步，在每个时间步输入大小为3的向量。下面代码构建了这个RNN，两个时间步展开：

```python
n_inputs = 3
n_neurons = 5

X0 = tf.placeholder(tf.float32,[None,n_inputs])
X1 = tf.placeholder(tf.float32,[None,n_inputs])

Wx = tf.Variable(tf.random_normal(shape=[n_inputs,n_neurons],dtype=tf.float32))
Wy = tf.Variable(tf.random_normal(shape=[n_neurons,n_neurons],dtype=tf.float32))
b = tf.Variable(tf.zeros([1,n_neurons],dtype=tf.float32))

Y0 = tf.tanh(tf.matmul(X0,Wx)+b)
Y1 = tf.tanh(tf.matmul(Y0,Wy)+tf.matmul(X1,Wx)+b)

init = tf.global_variables_initializer()
```

这个网络就像一个2层的前馈神网，只改了点地方：首先 层之间的权重和偏差项被两个层共享，其次，我们给每个层喂入输入，然后获得每个层的输出。为了运行这个模型，我们需要在每个时间步中喂给它输入，如：

```python
import numpy as np
# Mini-batch: instance 0, instance1,instance3 ,instance4
X0_batch = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 0, 1]]) # t = 0
X1_batch = np.array([[9, 8, 7], [0, 0, 0], [6, 5, 4], [3, 2, 1]]) # t = 1

with tf.Session() as sess:
    init.run()
    Y0_val,Y1_val  = sess.run([Y0,Y1],feed_dict={X0: X0_batch,X1:X1_batch})
```

这个mini-batch包含4个实例，每个有一个输入序列，由2个输入组成。最后Y0_val和Y1_val包含所有神经元和小批量中所有实例的两个时间步长的网络输出：

```shell
>>> print(Y0_val) # output at t = 0
[[-0.2964572 0.82874775 -0.34216955 -0.75720584 0.19011548] # instance 0
[-0.12842922 0.99981797 0.84704727 -0.99570125 0.38665548] # instance 1
[ 0.04731077 0.99999976 0.99330056 -0.999933 0.55339795] # instance 2
[ 0.70323634 0.99309105 0.99909431 -0.85363263 0.7472108 ]] # instance 3
>>> print(Y1_val) # output at t = 1
[[ 0.51955646 1. 0.99999022 -0.99984968 -0.24616946] # instance 0
[-0.70553327 -0.11918639 0.48885304 0.08917919 -0.26579669] # instance 1
[-0.32477224 0.99996376 0.99933046 -0.99711186 0.10981458] # instance 2
[-0.43738723 0.91517633 0.97817528 -0.91763324 0.11047263]] # instance 3
```

这不难，但如果你要运行一个超过100步的RNN，这个图必须会变得相当大。现在我们来看如何用tf的RNN操作。

## 静态时间展开

**static_rnn()**函数通过链接单元格来创建展开的RNN网络。 以下代码创建与前一个完全相同的模型:

```python
X0 = tf.placeholder(tf.float32,[None,n_inputs])
X1 = tf.placeholder(tf.float32,[None,n_inputs])

basic_cell = tf.contrib.rnn.BasicRNNCell(num_units=n_neurons)
output_seqs, states = tf.contrib.rnn.static_rnn(
basic_cell, [X0,X1],dtype=tf.float32)
Y0,Y1 = output_seqs
```

首先，我们和之前一样创建输入的placeholders，然后我们创建一个BasicRNNCell,你可以认为是个工厂，它创建单元的副本来构建展开的RNN（每个时间步一个）。然后我们调用**static_rnn()**,给他一个单元工厂和输入tensor，然后告诉它输入的数据类型（这用于创建初始状态矩阵，默认情况下为零）。每次输入的时候，**static_rnn()**方法调用工厂的 **_\_call\_\_()**方法，创建2个单元的副本（每个包含一个有五个递归神经元的神经层），使用共享权重和偏差项，并将它们链接起来，就像我们之前做的那样。**static_rnn()**方法返回2个对象。第一个是一个Python list包含每个时间步的输出tensor。第二个是一个包含网络的最后状态的tensor。当你使用基本单元，最后的状态简单的等于最后的输出。

如果有50个时间步，必须定义50个输入placeholder和50个输出tensor是很不方便的。此外，在执行期你必须要分别喂给50个placeholder和操作50个输出。让我们简化一下。下面代码又一次构建同样的RNN，但这次只需要一个形状为[None，n_steps，n_inputs]的单个输入placeholder，其中第一个维度是小批量大小。然后它在每个时间步提取输入序列的列表。X_seqs是形状为[None，n_inputs]的n_steps张量的Python列表，其中第一个维度是小批量大小。我们首先使用**transpose()**方法交换2个维度（perm为交换规则：[1,0,2]，0位置和1位置的交换），现在时间步在第一维度。然后我们提取一个Python tensor列表（一个时间步一个tensor)使用**unstack()**方法。下2行和之前一样。最后我们使用**stack()**方法合并所有输出张量到一个tensor，然后我们交换前两个维度以获得最终输出张量的形状[None，n_steps，n_neurons]（现在第一个维度是小批量大小）。

```python
X = tf.placeholder(tf.float32,[None, n_steps,n_inputs])
X_seqs = tf.unstack(tf.transpose(X,perm=[1,0,2]))
basic_cell = tf.contrib.rnn.BasicRNNCell(num_units=n_neurons)
output_seqs, states = tf.contrib.rnn.static_rnn(basic_cell,X_seqs,dtype=tf.float32)
outputs = tf.transpose(tf.stack(output_seqs),perm=[1,0,2])
```
- tf.unstack（）则是一个矩阵分解的函数，交换1和0，按照n_steps分解
- tf.stack（）这是一个矩阵拼接的函数

现在我们可以通过喂给它一个张量包含所有的小批量序列就能运行网络了：

```python
X_batch = np.array([
    #t = 0      t= 1
    [[0, 1, 2], [9, 8, 7]], # instance 0
	[[3, 4, 5], [0, 0, 0]], # instance 1
	[[6, 7, 8], [6, 5, 4]], # instance 2
	[[9, 0, 1], [3, 2, 1]], # instance 3
])

with tf.Session() as sess:
    init.run()
    outputs_val = outputs.eval(feed_dict={X: X_batch})
```

我们为所有实例，所有时间步和所有神经元获得单个outputs_val张量：

```python
>>> print(outputs_val)
[[[-0.2964572 0.82874775 -0.34216955 -0.75720584 0.19011548]
  [ 0.51955646 1. 0.99999022 -0.99984968 -0.24616946]]
 
[[-0.12842922 0.99981797 0.84704727 -0.99570125 0.38665548]
 [-0.70553327 -0.11918639 0.48885304 0.08917919 -0.26579669]]
 
[[ 0.04731077 0.99999976 0.99330056 -0.999933 0.55339795]
 [-0.32477224 0.99996376 0.99933046 -0.99711186 0.10981458]]
 
[[ 0.70323634 0.99309105 0.99909431 -0.85363263 0.7472108 ]
 [-0.43738723 0.91517633 0.97817528 -0.91763324 0.11047263]]]
```

但是，这种方法仍构建了一个每个时间步长包含一个单元的图。如果有50个时间步，这个图会变得相当的丑。这有点像编写程序没有使用循环（例如，Y0 = f（0，X0）; Y1 = f（Y0，X1）; Y2 = f（Y1，X2）; ......; Y50 = f（Y49，X50））。有了这样大的图，你甚至可能在反向传播期间（尤其是GPU卡的内存有限）会出现内存溢出（OOM）错误，因为它必须在正向传递期间存储所有张量值，以便它可以使用它们来计算 反向传播期间的梯度。

幸运的是，有个更好的方案：**dynamic_rnn()**方法。

## 动态时间展开

**dynamic_rnn()**方法使用了一个**while_loop()**操作来在单元上运行适当的次数，并且你可以设置swap_memory=True，如果你想在反向传播的时候让它交换GPU的内存给CPU的内存，以避免OOM错误。方便的，它还在每个时间步接受带有所有输入的单个张量（形状[None，n_steps，n_inputs]），并且在每个时间步输出所有输出的单个张量（形状[None，n_steps，n_neurons]）; 无需堆叠，取消堆叠或转置。 以下代码使用dynamic_rnn（）函数创建与之前相同的RNN。 它好多了！

```python
X = tf.placeholder(tf.float32,[None,n_steps,n_inputs])

basic_cell = tf.contrib.rnn.BasicRNNCell(num_units=n_neurons)
outputs,states = tf.nn.dynamic_rnn(basic_cell,X,dtype=tf.float32)

```

在反向传播期间，while_loop（）操作执行适当的魔术：它在正向传递期间存储每次迭代的张量值，因此它可以使用它们来计算反向传递期间的渐变。

## 处理可变长度输入序列

到目前为止，我们只使用固定大小的输入序列（所有输入序列都恰好两步）。 如果输入序列具有可变长度（例如，像句子一样）会怎么样？ 在这种情况下，您应该在调用dynamic_rnn（）（或static_rnn（））函数时设置sequence_length参数; 它必须是1D张量，表示每个实例的输入序列的长度。 例如：

```python
seq_length = tf.placeholder(tf.int32, [None])
[...]
outputs, states = tf.nn.dynamic_rnn(basic_cell, X, dtype=tf.float32,
sequence_length=seq_length)
```

例如，假设第二个输入序列只包含一个输入而不是两个输入。 它必须用零向量填充，以便适合输入张量X（因为输入张量的第二个维度是最长序列的大小，即2）。

```python
X_batch = np.array([
	# step 0 step 1
	[[0, 1, 2], [9, 8, 7]], # instance 0
	[[3, 4, 5], [0, 0, 0]], # instance 1 (padded with a zero vector)
	[[6, 7, 8], [6, 5, 4]], # instance 2
	[[9, 0, 1], [3, 2, 1]], # instance 3
])
seq_length_batch = np.array([2, 1, 2, 2])
```

当然，你现在需要喂给placeholder X 和seq_length值：

```python
with tf.Session() as sess:
    init.run()
    outputs_val,states_val =
    sess.run([outputs, states], feed_dict={X: X_batch, seq_length: seq_length_batch})
```

现在，RNN为输入序列长度的每个时间步输出零向量（查看第二个时间步的第二个实例的输出）：

```python
>>> print(outputs_val)
[[[-0.2964572 0.82874775 -0.34216955 -0.75720584 0.19011548]
  [ 0.51955646 1. 0.99999022 -0.99984968 -0.24616946]] # final state
 
[[-0.12842922 0.99981797 0.84704727 -0.99570125 0.38665548] # final state
 [ 0.         0.         0.          0.         0.       ]] # zero vector
 
[[ 0.04731077 0.99999976 0.99330056 -0.999933 0.55339795]
 [-0.32477224 0.99996376 0.99933046 -0.99711186 0.10981458]] # final state
 
[[ 0.70323634 0.99309105 0.99909431 -0.85363263 0.7472108 ]
 [-0.43738723 0.91517633 0.97817528 -0.91763324 0.11047263]]] # final state
```

此外，状态张量包含每个单元的最后状态（除了0向量）：

```python
>>> print(states_val)
[[ 0.51955646 1. 0.99999022 -0.99984968 -0.24616946] # t = 1
[-0.12842922 0.99981797 0.84704727 -0.99570125 0.38665548] # t = 0 !!!
[-0.32477224 0.99996376 0.99933046 -0.99711186 0.10981458] # t = 1
[-0.43738723 0.91517633 0.97817528 -0.91763324 0.11047263]] # t = 1
```

## 处理可变长度的输出

如果输出序列长度可变怎么处理呢？如果事先知道每个序列的长度（例如，如果知道它与输入序列的长度相同），则可以如上所述设置sequence_length参数。 遗憾的是，通常这是不可能的：例如，翻译句子的长度通常不同于输入句子的长度。 在这种情况下，最常见的解决方案是定义一个称为序列结束标记（EOS标记）的特殊输出。 任何超过EOS的输出都应该被忽略（我们将在本章后面讨论）。

很好，现在你知道如何构建一个RNN网络（或者更准确地说是随时间展开的RNN网络），那么怎么训练他们呢？

