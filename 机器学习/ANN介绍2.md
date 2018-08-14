## 使用TF的高级API训练MLP

用tf训练一个MLP模型最简单方式是使用高级API TF.Learn。DNNClassifier 类让训练具有任意数量隐藏层和一个softmax输出层输出类别概率的深度神经网络变得微不足道。比如下面代码训练一个分类用的DNN，带有2个隐藏层（300个神经元，另一个100个神经元）和一个带有10个神经元的softmax输出层：

```python
import tensorflow as tf

feature_columns = tf.contrib.learn.infer_real_valued_columns_from_input(X_train)
dnn_clf = tf.contrib.learn.DNNClassifier(hidden_units=[300,100],n_classes=10,feature_columns=feature_columns)

dnn_clf.fit(x=X_train,y=y_train,batch_size=50,steps=40000)
```

如果你在MNIST数据集上运行这段代码（调整大小后，使用Scikit-learn的StandarScalar），就能在测试集上得到一个达到98.1%的准确率。

```python
from sklearn.metrics import accuracy_score
y_pred = list(dnn_clf.predict(X_test))
accuracy_score(y_test,y_pred)

```

tf.learn 库也提供了一些评估模型的方便方法：

```
dnn_clf.evaluate(X_test,y_test)
```

DNNClassifier类创建了所有的神经元层，基于ReLU阶跃函数（可以通过设置activation_fn 超参数调整）。输出层使用softmax函数，损失函数是cross entropy（交叉熵）。

## 使用简单的TF训练一个DNN

如果想控制整个网络架构，最好使用tf的低级python API。在这边，我们将使用此api构建和之前相同的模型，并且将实现小撮梯度下降，在MNIST数据集上进行训练。第一步是构建期，构建一个tf图。第二步是执行期，运行图来训练模型。

### 构建期

首先导入tf库，指定输入输出数量，设置隐含层的神经元数量。

```python
import tensorflow as tf

n_inputs = 28*28 # MNIST
n_hidden1 = 300
n_hidden2 = 100
n_outputs = 10
```

接下来用placeholder表示训练数据和指标，就是X和y。X的shape为部分定义。我们知道X会是一个2D的张量（矩阵），第一维度表示实例数量，第二维度表示特征数。特征是28x28（每个像素一个特征）。但不知道每撮多少个训练实例。同样的，y是一个1维的张量，每个实例一个值，但也不知道训练撮的大小，所以shape为（None):

```python
X = tf.placeholder(tf.float32,shape=(None,n_inputs),name="X")
y = tf.placeholder(tf.float32,shape=(None),name="y")
```

现在创建神经网络。X在输入层，在构建期，它会被一个训练撮替换。现在创建2个隐藏层和一个输出层。两个隐藏层几乎相同：不同只有输入和包含的神经元数量。输出层也很类似，但是使用一个softmax激活函数替代ReLU激活函数。于是我们创建一个neuron_layer()函数用来创建一个层。

```python
def neuon_layer(X, n_neurons, name, activation=None):
    with tf.name_scope(name):
        n_inputs = int(X.get_shape()[1])
        stddev = 2 / np.sqrt(n_inputs)
        init = tf.truncated_normal((n_inputs,n_neurons),stddev=stddev)
        W = tf.Variable(init,name="weights")
        b = tf.Variable(tf.zeros([n_neurons]),name="biases")
        z = tf.matmul(X,W) + b
        if activation=="relu":
            return tf.nn.relu(z)
        else:
            return z
```

1. 首先创建一个name scope，这会保含这层中所有计算节点。这会在TensorBoard看起来舒服些。
2. 接着，获得输入矩阵的shape并获取第二维的值（第一维度是实例数）。
3. 下三行创建一个W变量保存权重矩阵，它将包含输入和其他神经元的所有连接权重，shape为（n_inputs,n_neurons)。它会被初始化会随机值。使用这个特定标准背离帮助算法收敛更快。这是能提高效率的一个小微调。随机初始化所有隐藏的连接权重很重要，这会避免梯度下降算法碰到对称而无法突破。
4. 创建一个b变量用于bias，初始化为0,每个神经元一个bias参数。
5. 创建子图计算 z = X · W + b,这种矢量化的实现将对层中、撮中所有的实例进行有效的计算输入的加权和bias项。
6. 最后，如果activation 参数设为“relu”，代码返回relu(z)，否则返回z

现在开始搭建神经网络吧。第一层隐藏层用X作为输入。第二层用第一层的输出作为输入。最后输出层用第二层隐藏层的输出作为输入。

```python
with tf.name_scope("dnn"):
  hidden1 = neuron_layer(X,n_hidden1,"hidden1",activation="relu")
  hidden2 = neuron_layer(hidden1,n_hidden2,"hidden1",activation="relu") 
    logits = neuron_layer(hidden2,n_outputs,"hidden1",activation="outputs")
```

logits是进入softmax激活函数之前的值,为了结果最优化，后面再处理softmax计算。

tf给了许多便利的方法来创建标准神经网络层，所以通常没有必要定义你自己的neuon_layer()函数。比如，tf的**fully_connected()**方法创建一个完全连接层，所有的输入会连上所有的神经元。它会处理好weights和biases变量，使用适当的初始化策略，并且默认使用ReLU函数（可以通过使用activation_fn参数修改）。将我们前面的代码修改使用fully_connected()：

```python
from tensorflow.contrib.layers import fully_connected

with tf.name_scope("dnn"):
    hidden1 = fully_connected(X,n_hidden1,scope="hidden1")
    hidden2 = fully_connected(hidden1,n_hidden2,scope="hidden2")    
    logits = fully_connected(hidden2,n_outputs,scope="n_outputs",activation_fn=None)
    
```

现在有了神经网络模型，我们需要定义损失函数来训练它，我们使用cross entropy。cross entropy在判断出不准的时候会惩罚模型。tf提供几个函数来计算cross entropy。我们用spare_soft_max_corss_entropy_with_logits():它基于logtis计算cross entropy。这将得到一个1维的张量，包含每个实例的cross entropy。然后我们可以用tf的reduce_mean()方法对所有的实例计算平均值。

```python
with tf.name_scope("loss"):
    xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
    label=y,logits=logtis)
    loss = tf.reduce_mean(xentropy,name="loss")
```

sparse_softmax_cross_entropy_with_logits等价于计算softmax 后计算cross entropy，但是更加高效，并且能处理好当logits恰好等于0的情况。

现在定义GradientDescentOptimizer，让损失函数最小化。

```python
learning_rate = 0.01

with tf.name_scope("train"):
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    training_op = optimizer.minimize(loss)
```

在构建期最后重要的一步是指定怎样评估模型。我们将简单的用精确度还衡量。

首先，对每个实例，判断是否正确或者不是最高的logit对应于目标类别。你可以使用in_top_k()方法。这会返回一个1维张量，里面都是boolean值，然后我们需要将这些boolean值转为float然后计算平均数，这会得到网络的整体的精确度。

```python
with tf.name_scope("eval"):
    correct = tf.nn.in_top_k(logits,y,1)
    accuracy = tf.reduce_mean(tf.cast(correct,tf.float32))
```

创建一个节点初始化所有的变量。然后创建一个Saver保存训练模型参数到磁盘上。

```python
init = tf.global_variables_initializer()
saver = tf.train.Saver()
```

不到40行，但是相当紧凑：我们为输入和目标创建placeholders，创造一个函数构建一个神经层，使用这个函数构建一个DNN，定义损失函数，创造一个优化器，最后定义性能评估。现在到执行期。

### 执行期

首先载入MNIST。

```python
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/")
```

现在定义想要迭代的次数，还有小撮的数量：

```python
e_epochs = 400
batch_size = 50
```

训练模型：

```python
with tf.Session() as sess:
    init.run()
    for epoch in range(n_epochs):
        for iteration in range(mnist.train.num_examples // batch_size)
			X_batch,y_batch = mnist.train.next_batch(batch_size)
            sess.run(training_op,feed_dict={X:X_batch,y:y_batch})
		acc_train = accuracy.eval(feed_dict={X:X_batch,y:y_batch})
		acc_test = accuracy.eval(feed_dict=		{X:mnist.test.images,y:mnist.test.labels})
		print(epoch,"Train accuracy: ",acc_train,"Test accuracy: ",acc_test)
	
	save_path = saver.save(sess,"./my_model_final.ckpt")

```

这段代码打开tf的session，运行init 节点初始化所有的变量。然后进入主循环：每个时期，通过对应于训练集大小的许多小撮进行迭代。每次通过next_batch()获得小撮，然后训练，在每期结束时，评估最后小撮和整个训练集，打印结果，最后保存模型参数到磁盘。

### 使用神经网络

当神经网络训练好了，你就可以拿它进行预测。可以复用构建期，但修改执行期的代码：

```python
with tf.Session as sess:
    saver.restore(sess,"./my_model_final.ckpt")
    x_new_scaled=[...] # some new images(scaled from 0 to 1)
    Z = logits.eval(feed_dict={X:x_new_scaled})
    y_pred = np.argmax(Z,axis=1)
```

第一行载入模型。然后输入想分类的图片。记得进行scale。

评估logits节点。如果想知道所有的判断类概率，你需要应用softmax()函数到logits。但如果只是要预测一个类，只要挑概率最高的值（使用argmax())

### 微调神经网络超参数

神经网络的灵活性也是他们的一个主要的缺点：有许多超参数要调整。
