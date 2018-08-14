

自动编码器，能够学习输入数据的有效表示，称为编码，无需任何监督（即，训练集未标记）。这些编码比输入数据维度更低，这让它能够降低维度，更重要的是它有强大的特征检测器，并且可以用来做深神网无监督预训练，最后他们还能生成和训练数据非常相似的新数据。这个叫**会生的模型**。比如你可以训练一个自动编码器在人脸图片上，它就能生成一个新的面孔。神奇的是，自动编码器的工作原理是通过简单的拷贝他们的输入到输出。这听起来像很普通的任务，但我们会看到用许多方法约束网络，会让他相当困难。比如，你可以限制内在表示的大小，或者你可以给输入添加噪声并训练网络来恢复到原始输入。这些约束避免自动编码器从简单的拷贝输入到输出，这会强迫他学习表示数据的高效方式。简单的说，编码是自动编码器尝试在一些约束下学习身份函数的副产物。我们将学习自动编码器是如何工作的，哪些约束可以加进去，如何用tf实现维度降低，特征提取，无监督预训练，或者生殖模型。

## 高效数据表示

下面那个序列哪个你最容易记住呢？

- 40, 27, 25, 36, 81, 57, 10, 73, 19, 68
-  50, 25, 76, 38, 19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20 

乍看之下，第一个比较短，容易记住。但是如果仔细研究下序列2 ，会发现2个规律：偶数的下一项是它自己的一半，奇数加前一项的值再加1等于下一项（例如：50,25，（50+25+1））。那这时候第二个序列就很好记了，只需要记住首个数字50，以及序列的总个数。如果能记住每个长序列，那么也就不必去找第二个序列的规律了。正因为记不住长序列，所以就会另辟蹊径去寻找规律。这就表明了为什么要在训练的时候约束自动编码器来推动它发现和探索数据的规律。

专业国际象棋手能够5秒记住象棋上所有棋子的位置，而大多数人做不到。但这个只限于对的位置，而不是随机摆放棋子位置。象棋达人的记忆没有比你我好多少，他们只是因为有象棋经验而更容易看到象棋的规律。正如象棋手，自动编码器将输入转为一种高效的内在表示，然后吐出一些看起来和输入十分类似的东西。自动编码器由2部分组成：一个**编码器**（识别网络），负责将输入转为内在表示，接着是**解码器**（生成网络），将内在表示转为输出。如图15-1

一个自动编码器通常和多层感知机（MLP）一样的架构，除了输出神经元的数量必须等于输入神经元。这个例子中，只有一个有2个神经元的隐藏层（编码器），和一个三个神经元的输出层（解码器）。输出通常被叫做**重建**，因为自动编码器试着重建输入，损失函数包含一个重建损失，当重建与输入不同时，该重建损失会对模型进行惩罚。

![1530758082(1).png](https://upload-images.jianshu.io/upload_images/3509189-cb0aab378e6308c4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


因为内在表示比输入数据维度来的低（2D而不是3D)，自动编码器被认为是**不完全**的。一个不完整的自动编码器不能普通的拷贝它的输入到编码中，但它必须找到输出其输入副本的方法。它被迫学习输入数据中最重要的特征（并删除不重要的特征）。

让我们看看如何实现一个非常简单的不完全自动编码器来降低维数。

## 使用不完全线性执行PCA自动编码器

如果自动编码器只使用线性激活函数和损失函数为均方差（MSE）。然后可以证明它最终会执行主成分分析（PCA）。

以下代码构建了一个简单的线性自动编码器，用于在3D数据集上执行PCA，将其投影到2D：

```python
import tensorflow as tf
from tensorflow.contrib.layers import fully_connected

n_inputs = 3 # 3D inputs
n_hidden = 2 # 2D codings

n_outputs = n_inputs
learning_rate = 0.01

X = tf.placeholder(tf.float32, shape=[None, n_inputs])
hidden = fully_connected(X, n_hidden, activation_fn=None)
outputs = fully_connected(hidden, n_outputs, activation_fn=None)

reconstruction_loss = tf.reduce_mean(tf.square(outputs - X)) # MSE

optimizer = tf.train.AdamOptimizer(learning_rate)
training_op = optimizer.minimize(reconstruction_loss)

init = tf.global_variables_initializer()
```

- 输入数量等于输出数量
- 为了执行简单的PCA，我们设置activation_fn=None(所有的神经元都是线性的)，损失函数为MSE。

现在载入数据集，在训练集上训练模型，然后用于编码测试集：

```
X_train, X_test = [...] # load the dataset

n_iterations = 1000
codings = hidden # the output of the hidden layer provides the codings

with tf.Session() as sess:
	init.run()
	for iteration in range(n_iterations):
		training_op.run(feed_dict={X: X_train}) # no labels (unsupervised)
	codings_val = codings.eval(feed_dict={X: X_test})

```

图15-2显示了原始3D数据集（左侧）和自动编码器隐藏层（即右侧编码层）的输出。 正如您所看到的，自动编码器找到了最佳的2D平面来投影数据，尽可能多地保留数据的变化（就像PCA一样）。

![1530759000(1).png](https://upload-images.jianshu.io/upload_images/3509189-0f4d97630b19ea55.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 堆叠式自动编码器

就像我们讨论的其他神经网络一样，自动编码器可以有多个隐藏层。 在这种情况下，它们被称为**堆叠自动编码器（或深度自动编码器）**。 添加更多层有助于自动编码器学习更复杂的编码。 但是，必须注意不要使自动编码器太强大。 想象一个编码器如此强大，它只是学会将每个输入映射到一个任意数字（并且解码器学习反向映射）。 显然，这样的自动编码器将完美地重建训练数据，但是它不会在过程中学习任何有用的数据表示（并且它不可能很好地概括为新实例）。

堆叠自动编码器的架构通常关于中央隐藏层（编码层）是对称的。 简单来说，它看起来像一个三明治。 例如，MNIST的自动编码器 可能有784个输入，其次是隐藏层有300个神经元，然后是150个神经元的中央隐藏层，然后是另一个隐藏层有300个神经元，输出层有784个神经元。 该堆叠自动编码器如图15-3所示

![1530759516(1).png](https://upload-images.jianshu.io/upload_images/3509189-e79a089a302799db.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## tf 实现

您可以实现堆叠自动编码器，就像常规深度MLP一样。 特别是，我们可以应用第11章中用于训练深网的相同技术。 例如，以下代码使用He初始化，ELU激活函数和ℓ2正则化为MNIST构建堆叠自动编码器。 代码应该看起来非常熟悉，除了没有标签（没有y）：

```python
n_inputs = 28 * 28 # for MNIST
n_hidden1 = 300
n_hidden2 = 150 # codings
n_hidden3 = n_hidden1
n_outputs = n_inputs

learning_rate = 0.01
l2_reg = 0.001

X = tf.placeholder(tf.float32, shape=[None, n_inputs])
with tf.contrib.framework.arg_scope(
		[fully_connected],
		activation_fn=tf.nn.elu,
		weights_initializer=tf.contrib.layers.variance_scaling_initializer(),
		weights_regularizer=tf.contrib.layers.l2_regularizer(l2_reg)):
	hidden1 = fully_connected(X, n_hidden1)
	hidden2 = fully_connected(hidden1, n_hidden2) # codings
	hidden3 = fully_connected(hidden2, n_hidden3)
	outputs = fully_connected(hidden3, n_outputs, activation_fn=None)

reconstruction_loss = tf.reduce_mean(tf.square(outputs - X)) # MSE

reg_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
loss = tf.add_n([reconstruction_loss] + reg_losses)

optimizer = tf.train.AdamOptimizer(learning_rate)
training_op = optimizer.minimize(loss)

init = tf.global_variables_initializer()
```

然后，您可以正常训练模型。 请注意，数字标签（y_batch）未使用：

```
n_epochs = 5
batch_size = 150

with tf.Session() as sess:
	init.run()
	for epoch in range(n_epochs):
		n_batches = mnist.train.num_examples // batch_size
		for iteration in range(n_batches):
			X_batch, y_batch = mnist.train.next_batch(batch_size)
			sess.run(training_op, feed_dict={X: X_batch})
```

## 联系权重

当自动编码器整齐对称时，就像我们刚刚构建的那样，一种常见的技术是将解码器层的权重与编码器层的权重联系起来。 这样可以减少模型中的权重数量，加快训练速度并限制过度拟合的风险。 具体地，如果自动编码器具有总共N层（不计入输入层），并且WL表示第L层的连接权重（例如，层1是第一隐藏层，则层N/2是编码层，并且层N是 输出层），然后解码器层权重可以简单地定义为：

W（N-L+1） = WTL（L = 1,2，...，N/2）

不幸的是，使用fully_connected（）函数在TensorFlow中实现绑定权重有点麻烦; 实际上，手动定义层实际上更容易。 代码结果明显更加冗长：

```
activation = tf.nn.elu
regularizer = tf.contrib.layers.l2_regularizer(l2_reg)
initializer = tf.contrib.layers.variance_scaling_initializer()

X = tf.placeholder(tf.float32, shape=[None, n_inputs])

weights1_init = initializer([n_inputs, n_hidden1])
weights2_init = initializer([n_hidden1, n_hidden2])

weights1 = tf.Variable(weights1_init, dtype=tf.float32, name="weights1")
weights2 = tf.Variable(weights2_init, dtype=tf.float32, name="weights2")
weights3 = tf.transpose(weights2, name="weights3") # tied weights
weights4 = tf.transpose(weights1, name="weights4") # tied weights

biases1 = tf.Variable(tf.zeros(n_hidden1), name="biases1")
biases2 = tf.Variable(tf.zeros(n_hidden2), name="biases2")
biases3 = tf.Variable(tf.zeros(n_hidden3), name="biases3")
biases4 = tf.Variable(tf.zeros(n_outputs), name="biases4")

hidden1 = activation(tf.matmul(X, weights1) + biases1)
hidden2 = activation(tf.matmul(hidden1, weights2) + biases2)
hidden3 = activation(tf.matmul(hidden2, weights3) + biases3)
outputs = tf.matmul(hidden3, weights4) + biases4

reconstruction_loss = tf.reduce_mean(tf.square(outputs - X))
reg_loss = regularizer(weights1) + regularizer(weights2)
loss = reconstruction_loss + reg_loss

optimizer = tf.train.AdamOptimizer(learning_rate)
training_op = optimizer.minimize(loss)

init = tf.global_variables_initializer()
```

这段代码非常简单，但有几点需要注意：

- 首先，weight3和weight4不是变量，它们分别是权重2和权重1的转置（它们与它们“联系”）。
- 其次，因为它们不是变量，所以将它们正规化是没有用的：我们只调整权重1和权重2。
- 第三，偏见永远不会被束缚，也永远不会正规化

## 一次训练一个自动编码器

不像我们刚才那样一次性训练整个堆叠自动编码器，一次训练一个浅自动编码器通常要快得多，然后将它们全部堆叠成单个堆叠自动编码器（因此得名），如图15-4所示。 这对于非常深的自动编码器尤其有用。

![1530760069(1).png](https://upload-images.jianshu.io/upload_images/3509189-fa0208f6251332b0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


在训练的第一阶段期间，第一自动编码器学习重建输入。 在第二阶段期间，第二自动编码器学习重建第一自动编码器的隐藏层的输出。 最后，您只需使用所有这些自动编码器构建一个大三明治，如图15-4所示（即，您首先堆叠每个自动编码器的隐藏层，然后以相反的顺序堆叠输出层）。 这为您提供了最终的堆叠自动编码器。 您可以通过这种方式轻松训练更多自动编码器，构建一个非常深的堆叠自动编码器。

要实现这种多相训练算法，最简单的方法是为每个阶段使用不同的TensorFlow图。 训练自动编码器后，您只需通过它运行训练集并捕获隐藏层的输出。 然后，该输出用作下一个自动编码器的训练集。 一旦所有自动编码器都经过这种方式的训练，您只需复制每个自动编码器的权重和偏差，并使用它们构建堆叠自动编码器。

实现这种方法非常简单，所以我们不会在这里详细说明，但请查看Jupyter notebook中的代码。

另一种方法是使用包含整个堆叠自动编码器的单个图形，以及执行每个训练阶段的一些额外操作，如图15-5所示。

![1530760600(1).png](https://upload-images.jianshu.io/upload_images/3509189-6bbc77037ef7d979.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


这值得解释一下：

- 图中的中心列是全堆叠自动编码器。 这部分可以在训练后使用。
- 左列是运行第一阶段培训所需的一组操作。 它创建一个绕过隐藏层2和3的输出层。此输出层与堆叠自动编码器的输出层共享相同的权重和偏差。 最重要的是培训操作，旨在使输出尽可能接近输入。 因此，该阶段将训练隐藏层1和输出层（即第一自动编码器）的权重和偏差。
- 图中的右列是运行第二阶段培训所需的一组操作。 它增加了训练操作，旨在使隐藏层3的输出尽可能接近隐藏层1的输出。注意，我们必须在运行阶段2时冻结隐藏层1.此阶段将训练权重和偏差 隐藏层2和3（即第二自动编码器）。

tf代码：

```
[...] # Build the whole stacked autoencoder normally.
# In this example, the weights are not tied.

optimizer = tf.train.AdamOptimizer(learning_rate)

with tf.name_scope("phase1"):
	phase1_outputs = tf.matmul(hidden1, weights4) + biases4
	phase1_reconstruction_loss = tf.reduce_mean(tf.square(phase1_outputs - X))
	phase1_reg_loss = regularizer(weights1) + regularizer(weights4)
	phase1_loss = phase1_reconstruction_loss + phase1_reg_loss
	phase1_training_op = optimizer.minimize(phase1_loss)

with tf.name_scope("phase2"):
	phase2_reconstruction_loss = tf.reduce_mean(tf.square(hidden3 - hidden1))
	phase2_reg_loss = regularizer(weights2) + regularizer(weights3)
	phase2_loss = phase2_reconstruction_loss + phase2_reg_loss
	train_vars = [weights2, biases2, weights3, biases3]
	phase2_training_op = optimizer.minimize(phase2_loss, var_list=train_vars)
```

第一阶段非常简单：我们只创建一个跳过隐藏层2和3的输出层，然后构建训练操作以最小化输出和输入之间的距离（加上一些正则化）。

第二阶段仅添加了使隐藏层3的输出与隐藏层1之间的距离最小化所需的操作（也具有一些正则化）。 最重要的是，我们向minimize（）方法提供可训练变量列表，确保省去weights1和biases1; 这有效地在阶段2期间冻结隐藏的第1层。

在执行阶段，您需要做的就是运行阶段1训练操作多个时期，然后阶段2训练操作一些更多时期。

由于隐藏层1在阶段2期间被冻结，因此对于任何给定的训练实例，其输出将始终相同。 为了避免在每个时期重新计算隐藏层1的输出，您可以在阶段1结束时为整个训练集计算它，然后在阶段2期间直接提供隐藏层1的缓存输出。这可以为您提供 一个不错的性能提升。

## 可视化重建

确保自动编码器经过适当训练的一种方法是比较输入和输出。 它们必须非常相似，差异应该是不重要的细节。 让我们绘制两个随机数字及其重建：

```
n_test_digits = 2
X_test = mnist.test.images[:n_test_digits]

with tf.Session() as sess:
	[...] # Train the Autoencoder
	outputs_val = outputs.eval(feed_dict={X: X_test})

def plot_image(image, shape=[28, 28]):
	plt.imshow(image.reshape(shape), cmap="Greys", interpolation="nearest")
	plt.axis("off")

for digit_index in range(n_test_digits):
	plt.subplot(n_test_digits, 2, digit_index * 2 + 1)
	plot_image(X_test[digit_index])
	plt.subplot(n_test_digits, 2, digit_index * 2 + 2)
	plot_image(outputs_val[digit_index])

```

![1530760978(1).png](https://upload-images.jianshu.io/upload_images/3509189-497e049309175f6f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


看起来足够接近。 所以自动编码器已经正确地学会了重现它的输入，但是它学到了有用的功能吗？ 让我们来看看

## 可视化功能

一旦您的自动编码器学习了一些功能，您可能需要查看它们。 有各种各样的技术。 可以说最简单的技术是考虑每个隐藏层中的每个神经元，并找到最能激活它的训练实例。 这对于顶层隐藏层特别有用，因为它们通常捕获相对较大的功能，您可以轻松地在包含它们的一组训练实例中发现这些功能。 例如，如果神经元在看到图片中的猫时强烈激活，那么激活它的图片最明显都包含猫。 然而，对于较低层，这种技术不能很好地工作，因为这些特征更小，更抽象，因此通常很难准确理解神经元对所有兴奋的东西。

让我们看看另一种技术。 对于第一个隐藏层中的每个神经元，您可以创建一个图像，其中像素的强度对应于与给定神经元的连接的权重。 例如，以下代码绘制了第一个隐藏层中五个神经元所学习的特征：

```
with tf.Session() as sess:
	[...] # train autoencoder
	weights1_val = weights1.eval()
for i in range(5):
	plt.subplot(1, 5, i + 1)
	plot_image(weights1_val.T[i])
```

![1530761151(1).png](https://upload-images.jianshu.io/upload_images/3509189-c550af51dcf3e8ed.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


前四个特征似乎对应于小补丁，而第五个特征似乎寻找垂直笔划（请注意，这些特征来自堆叠去噪自动编码器，我们将在后面讨论）。

另一种技术是为自动编码器提供随机输入图像，测量您感兴趣的神经元的激活，然后执行反向传播以调整图像，使神经元更加激活。 如果你多次迭代（执行渐变上升），图像将逐渐变成最令人兴奋的图像（对于神经元）。 这是一种有用的技术，可视化神经元正在寻找的输入类型。

最后，如果您使用自动编码器执行无监督预训练 - 例如，对于分类任务 - 验证自动编码器学习的特征是否有用的简单方法是测量分类器的性能

## 使用堆叠自动编码器进行无监督预训练

如果您正在处理复杂的监督任务，但是您没有大量标记的训练数据，那么一种解决方案是找到执行类似任务的神经网络，然后重用其较低层。 这使得仅使用很少的训练数据训练高性能模型成为可能，因为您的神经网络不必学习所有低级功能; 它只会重用现有网络学到的特征探测器。

同样，如果您有一个大型数据集，但大部分都是未标记的，您可以首先使用所有数据训练堆叠自动编码器，然后重复使用较低层为您的实际任务创建神经网络，并使用标记数据对其进行训练。 例如，图15-8显示了如何使用堆叠自动编码器为分类神经网络执行无监督预训练。 如前所述，堆叠自动编码器本身通常一次训练一个自动编码器。在训练分类器时，如果你真的没有太多标记的训练数据，你可能想要冻结预训练的层（至少是较低的层）

![1530761353(1).png](https://upload-images.jianshu.io/upload_images/3509189-09ba70d1596845cd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


这种情况实际上很常见，因为构建一个大的未标记数据集通常很便宜（例如，一个简单的脚本可以从互联网上下载数百万个图像），但标记它们只能由人类可靠地完成（例如，将图像分类为可爱或 不）。 标记实例是耗时且昂贵的，因此仅具有几千个标记实例是很常见的。

正如我们前面所讨论的，当前深度学习海啸的一个触发因素是Geoffrey Hinton等人在2006年发现的。 深度神经网络可以无人监督的方式预先训练。 他们使用受限制的Boltzmann机器（见附录E），但在2007年Yoshua Bengio等人。 显示自动编码器也能正常工作。

TensorFlow实现没有什么特别之处：只需使用所有训练数据训练自动编码器，然后重复使用其编码器层来创建新的神经网络（有关如何重用预训练层的更多详细信息，请参阅第11章，或查看代码示例 在Jupyter中）。

到目前为止，为了强制自动编码器学习有趣的特征，我们限制了编码层的大小，使其不完整。 实际上可以使用许多其他类型的约束，包括允许编码层与输入一样大，或者甚至更大的约束，从而导致过度完整的自动编码器。 我们现在来看看其中的一些方法

## 去噪自动编码器

强制自动编码器学习有用功能的另一种方法是向其输入添加噪声，训练它以恢复原始的无噪声输入。 这可以防止自动编码器将其输入简单地复制到其输出，因此最终必须在数据中找到模式。

自20世纪80年代以来，使用自动编码器去除噪声的想法一直存在（例如，在Yann LeCun的1987年硕士论文中提到过）。 在2008年的一篇论文中，3 Pascal Vincent等人。 表明自动编码器也可用于特征提取。 在2010年的一篇论文中，4 Vincent等人。 介绍了堆叠去噪自动编码器。

噪声可以是添加到输入的纯高斯噪声，也可以随机关闭输入，就像丢失一样（在第11章中介绍）。 图15-9显示了这两个选项。

![1530761596(1).png](https://upload-images.jianshu.io/upload_images/3509189-4fac7ea41f01c5c7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### TensorFlow Implementation 

在TensorFlow中实现去噪自动编码器并不太难。 让我们从高斯噪声开始。 它实际上就像训练常规自动编码器一样，除了你为输入添加噪声，并且重建损失是根据原始输入计算的：

```python
X = tf.placeholder(tf.float32, shape=[None, n_inputs])
X_noisy = X + tf.random_normal(tf.shape(X))
[...]
hidden1 = activation(tf.matmul(X_noisy, weights1) + biases1)
[...]
reconstruction_loss = tf.reduce_mean(tf.square(outputs - X)) # MSE
[...]
```

由于X的形状仅在构造阶段被部分定义，我们无法预先知道必须添加到X的噪声的形状。我们不能调用X.get_shape（）因为这将只返回部分定义的X形状 （[None，n_inputs]）和random_normal（）需要一个完全定义的形状，因此它会引发异常。 相反，我们调用tf.shape（X），它创建一个在运行时将返回X形状的操作，该操作将在该点完全定义。

实现更常见的dropout版本并不困难：

```
from tensorflow.contrib.layers import dropout
keep_prob = 0.7
is_training = tf.placeholder_with_default(False, shape=(), name='is_training')
X = tf.placeholder(tf.float32, shape=[None, n_inputs])
X_drop = dropout(X, keep_prob, is_training=is_training)
[...]
hidden1 = activation(tf.matmul(X_drop, weights1) + biases1)
[...]
reconstruction_loss = tf.reduce_mean(tf.square(outputs - X)) # MSE
[...]
```

在训练期间，我们必须使用feed_dict将is_training设置为True：

```
sess.run(training_op, feed_dict={X: X_batch, is_training: True})
```

但是，在测试期间，没有必要将is_training设置为False，因为我们在调用placeholder_with_default（）函数时将其设置为默认值。

## 稀疏自动编码器

通常导致良好特征提取的另一种约束是稀疏性：通过向成本函数添加适当的术语，推动自动编码器以减少编码层中的活动神经元的数量。 例如，可以推动它在编码层中平均仅具有5％的显着活跃的神经元。 这迫使自动编码器将每个输入表示为少量激活的组合。 因此，编码层中的每个神经元通常最终代表一个有用的特征（如果你每个月只说几个字，你可能会试着让它们值得一听）。

为了支持稀疏模型，我们必须首先在每次训练迭代时测量编码层的实际稀疏度。 我们通过计算整个训练批次中编码层中每个神经元的平均激活来实现。 批量大小不能太小，否则平均值不准确

一旦我们对每个神经元进行平均激活，我们希望通过在成本函数中添加稀疏性损失来惩罚过于活跃的神经元。 例如，如果我们测量神经元的平均激活为0.3，但目标稀疏度为0.1，则必须惩罚它以激活更少。 一种方法可以简单地将平方误差（0.3-0.1）^2加到成本函数中，但实际上更好的方法是使用Kullback-Leibler散度（在第4章中简要讨论），其具有比均值更强的梯度。 平方误差，如图15-10所示

![1530761898(1).png](https://upload-images.jianshu.io/upload_images/3509189-19e51a2392b8729f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![1530761953(1).png](https://upload-images.jianshu.io/upload_images/3509189-f0939e9592c93ca5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


在我们的情况下，我们想要测量编码层中的神经元将激活的目标概率p与实际概率q（即，训练批次上的平均激活）之间的偏差。 因此，KL分歧简化为公式15-2。

![1530761978(1).png](https://upload-images.jianshu.io/upload_images/3509189-6ef6bba0670c4a1e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


一旦我们计算了编码层中每个神经元的稀疏度损失，我们只需总结这些损失，并将结果添加到成本函数中。 为了控制稀疏性损失和重建损失的相对重要性，我们可以将稀疏性损失乘以稀疏度权重超参数。 如果此重量太高，模型将紧贴目标稀疏度，但它可能无法正确重建输入，使模型无用。 相反，如果它太低，模型将主要忽略稀疏性目标，它不会学习任何有趣的功能。

### TensorFlow Implementation 

```
def kl_divergence(p, q):
	return p * tf.log(p / q) + (1 - p) * tf.log((1 - p) / (1 - q))

learning_rate = 0.01
sparsity_target = 0.1
sparsity_weight = 0.2

[...] # Build a normal autoencoder (in this example the coding layer is hidden1)

optimizer = tf.train.AdamOptimizer(learning_rate)

hidden1_mean = tf.reduce_mean(hidden1, axis=0) # batch mean
sparsity_loss = tf.reduce_sum(kl_divergence(sparsity_target, hidden1_mean))
reconstruction_loss = tf.reduce_mean(tf.square(outputs - X)) # MSE
loss = reconstruction_loss + sparsity_weight * sparsity_loss
training_op = optimizer.minimize(loss)
```

一个重要的细节是编码层的激活必须在0和1之间（但不等于0或1），否则KL分歧将返回NaN（非数字）。 一个简单的解决方案是对编码层使用逻辑激活函数

```
hidden1 = tf.nn.sigmoid(tf.matmul(X, weights1) + biases1)
```

一个简单的技巧可以加速收敛：我们可以选择具有更大梯度的重建损失，而不是使用MSE。 交叉熵通常是一个不错的选择。 要使用它，我们必须规范化输入，使它们从0到1取值，并在输出层使用逻辑激活函数，这样输出也会取0到1之间的值.TensorFlow的sigmoid_cross_entropy_with_logits（）函数负责 有效地将逻辑（sigmoid）激活函数应用于输出并计算交叉熵：

```
[...]
logits = tf.matmul(hidden1, weights2) + biases2)
outputs = tf.nn.sigmoid(logits)

reconstruction_loss = tf.reduce_sum(
tf.nn.sigmoid_cross_entropy_with_logits(labels=X, logits=logits))
```

请注意，训练期间不需要输出操作（我们仅在我们想要查看重建时才使用它）。

## 变分自动编码器

另一个重要的自动编码器类别是由Diederik Kingma和Max Welling在2014年推出的，并且很快成为最受欢迎的自动编码器类型之一：变分自动编码器。

它们与我们到目前为止讨论的所有自动编码器完全不同，特别是：

- 它们是概率自动编码器，意味着即使在训练之后，它们的输出也部分地由机会确定（与仅在训练期间使用随机性的自动编码器去噪相反）。
- 最重要的是，它们是生成自动编码器，这意味着它们可以生成看起来像是从训练集中采样的新实例。

这两个属性使它们与RBM非常相似（参见附录E），但它们更容易训练，采样过程更快（使用RBM，您需要等待网络稳定到“热平衡”，然后才能进行采样 一个新的实例）。

我们来看看它们是如何工作的。 图15-11（左）显示了一个变分自动编码器。 当然，您可以识别所有自动编码器的基本结构，编码器后跟解码器（在本例中，它们都有两个隐藏层），但有一个转折：而不是直接为给定输入生成编码 ，编码器产生平均编码μ和标准偏差σ。 然后从具有平均μ和标准偏差σ的高斯分布中随机地采样实际编码。 之后，解码器正常解码采样编码。 该图的右侧部分显示了通过此自动编码器的训练实例。 首先，编码器产生μ和σ，然后编码被随机采样（注意它不是精确地位于μ），最后这个编码被解码，最终输出类似于训练实例

![1530762325(1).png](https://upload-images.jianshu.io/upload_images/3509189-92761db3c80b8a06.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


正如您在图表中看到的那样，尽管输入可能具有非常复杂的分布，但是变分自动编码器倾向于产生看起来好像是从简单的高斯分布中采样的编码：在训练期间，成本函数（下面讨论）推动 在编码空间（也称为潜在空间）内逐渐迁移的编码占据大致（超）球形区域，看起来像高斯点云. 一个重要的结果是，在训练变分自动编码器之后，您可以非常轻松地生成一个新实例：只需从高斯分布中对随机编码进行采样，对其进行解码，然后再进行操作！

那么让我们来看看成本函数。 它由两部分组成。 第一种是通常的重建损失，它推动自动编码器重现其输入（我们可以使用交叉熵，如前所述）。 第二个是潜在的损失，它推动自动编码器具有看起来好像是从简单的高斯分布中采样的编码，为此我们使用目标分布（高斯分布）和编码的实际分布之间的KL偏差。 数学比以前复杂得多，特别是因为高斯噪声限制了可以传输到编码层的信息量（从而推动自动编码器学习有用的功能）。 幸运的是，方程简化了下面的潜在损失代码：

```
eps = 1e-10 # smoothing term to avoid computing log(0) which is NaN
latent_loss = 0.5 * tf.reduce_sum(
tf.square(hidden3_sigma) + tf.square(hidden3_mean)
- 1 - tf.log(eps + tf.square(hidden3_sigma)))
```

一种常见的变体是训练编码器输出γ= log（σ2）而不是σ。 只要我们需要σ，我们就可以计算σ=exp2γ。 这使得编码器更容易捕获不同尺度的sigma，因此它有助于加速收敛。 潜在的损失最终变得更简单了：

```python
latent_loss = 0.5 * tf.reduce_sum(
tf.exp(hidden3_gamma) + tf.square(hidden3_mean) - 1 - hidden3_gamma)
```

以下代码使用log（σ^ 2）变量构建图15-11（左）所示的变分自动编码器：

```
n_inputs = 28 * 28 # for MNIST
n_hidden1 = 500
n_hidden2 = 500
n_hidden3 = 20 # codings
n_hidden4 = n_hidden2
n_hidden5 = n_hidden1
n_outputs = n_inputs
learning_rate = 0.001
with tf.contrib.framework.arg_scope(
		[fully_connected],
		activation_fn=tf.nn.elu,
		weights_initializer=tf.contrib.layers.variance_scaling_initializer()):
	X = tf.placeholder(tf.float32, [None, n_inputs])
	hidden1 = fully_connected(X, n_hidden1)
	hidden2 = fully_connected(hidden1, n_hidden2)
	hidden3_mean = fully_connected(hidden2, n_hidden3, activation_fn=None)
	hidden3_gamma = fully_connected(hidden2, n_hidden3, activation_fn=None)
	hidden3_sigma = tf.exp(0.5 * hidden3_gamma)
	noise = tf.random_normal(tf.shape(hidden3_sigma), dtype=tf.float32)
	hidden3 = hidden3_mean + hidden3_sigma * noise
	hidden4 = fully_connected(hidden3, n_hidden4)
	hidden5 = fully_connected(hidden4, n_hidden5)
	logits = fully_connected(hidden5, n_outputs, activation_fn=None)
	outputs = tf.sigmoid(logits)	

reconstruction_loss = tf.reduce_sum(
tf.nn.sigmoid_cross_entropy_with_logits(labels=X, logits=logits))
latent_loss = 0.5 * tf.reduce_sum(
tf.exp(hidden3_gamma) + tf.square(hidden3_mean) - 1 - hidden3_gamma)
cost = reconstruction_loss + latent_loss

optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
training_op = optimizer.minimize(cost)

init = tf.global_variables_initializer()
```

###  生成数字

现在让我们使用这个变分自动编码器来生成看起来像手写数字的图像。 我们需要做的就是训练模型，然后从高斯分布中抽样随机编码并对其进行解码。

```
import numpy as np

n_digits = 60
n_epochs = 50
batch_size = 150

with tf.Session() as sess:
	init.run()
	for epoch in range(n_epochs):
		n_batches = mnist.train.num_examples // batch_size
		for iteration in range(n_batches):
			X_batch, y_batch = mnist.train.next_batch(batch_size)
			sess.run(training_op, feed_dict={X: X_batch})
	codings_rnd = np.random.normal(size=[n_digits, n_hidden3])
	outputs_val = outputs.eval(feed_dict={hidden3: codings_rnd})
```

而已。 现在我们可以看到自动编码器产生的“手写”数字是什么样的（见图15-12）：

```
for iteration in range(n_digits):
	plt.subplot(n_digits, 10, iteration + 1)
	plot_image(outputs_val[iteration])
```

![1530762735(1).png](https://upload-images.jianshu.io/upload_images/3509189-b26725958e08011b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


大多数这些数字看起来非常有说服力，而有些数字相当“有创意”。但不要对自动编码器过于苛刻 - 它只在不到一个小时前开始学习。 给它一点训练时间，这些数字看起来会越来越好。
