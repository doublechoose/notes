## 线性回归

TF operations（简称ops）可以传入任意数量的输入并产生任意数量的输出。如加法和乘法ops，传入2个输入并产生一个输出。变量和常量没有输入（source ops）。输入和输出是多维数组，叫tensor，就像Numpy数组，tensor有一个type和一个shape。

下面例子利用2D数组对California房价数据执行线性回归。它从获取数据集开始，然后为所有训练实例添加一个bias输入特征（x0 = 1).(它使用numpy，所以马上执行)。然后它创建2个tf constant 节点。X和y，保存data和targets。然后使用一些矩阵操作来定义theta。这些矩阵操作- transpose(),matmul(),和matrix_inverse()，不言自明。但他们也不马上做任何计算。而是在图中创造一个节点。

θ的定义：(θ= XT · X)^–1 · XT · y 

最后创建一个session并计算theta。

```python
import numpy as np
from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing()
m, n = housing.data.shape
housing_data_plus_bias = np.c_[np.ones((m, 1)), housing.data]

X = tf.constant(housing_data_plus_bias, dtype=tf.float32, name="X")
y = tf.constant(housing.target.reshape(-1, 1), dtype=tf.float32, name="y")
XT = tf.transpose(X)
theta = tf.matmul(tf.matmul(tf.matrix_inverse(tf.matmul(XT, X)), XT), y)
with tf.Session() as sess:
	theta_value = theta.eval()
```

## 实现梯度下降

首先手动的计算梯度，然后使用tf的autodiff特征让tf自动计算梯度，最后使用tf的开箱即用的优化器。

当使用梯度下降的时候，第一，先正规化输入特征向量，不然训练会很慢。

###手动计算梯度

- random_uniform() 方法在图中创建一个节点，将会生成一个包含随机值的tensor，赋予shape和值域，有点像NumPy的rand()方法。
- assign()方法创建一个节点，可以分配一个新值给一个变量，这里，它实现了θ^(next step) = θ –η∇θMSE(θ). 
- 主循环执行训练步骤一次又一次（n_epochs次），每100次迭代，打印当前Mean Squared Error均方差。

```python
n_epochs = 1000
learning_rate = 0.01

X = tf.constant(scaled_housing_data_plus_bias,dtype=tf.float32,name="X")
y = tf.constant(scaled_housing_data_plus_bias,dtype=tf.float32,name="y")
theta = tf.Variable(tf.target.reshape(-1,1),dtype=tf.float32,name="theta")
y_pred = tf.matmul(X, theta, name="predictions")
error = y_pred - y
mse = tf.reduce_mean(tf.square(error),name="mse")
gradients = 2/m * tf.matmul(tf.transpose(X),error)
training_op = tf.assign(theta,theta-learning_rate*gradients)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    
    for epoch in range(n_epochs):
        if epoch % 100 == 0:
            print("Epoch",epoch,"MSE = ",mse.eval())
        sess.run(training_op)
    best_theta = theta.eval()
```

### 使用autodiff

前面的代码可以工作，但是需要数学推导出损失函数（MSE）的梯度。在做线性回归的时候，很简单。但是如果你要在深度神经网络做这些工作的话，这会很蛋疼。这将会冗长且易错的。你可以用*symbolic differentiation* 来自动找到偏导。但由此产生的代码不一定高效。

为什么呢？看下个这个函数f(x) = exp(exp(exp(x)))。求导f'(x) = exp(x)\*exp(exp(x))\* exp(exp(exp(x)))。如果将f(x)和f'(x) 分开编码，代码就不会那么高效。一个更高效的方法是先计算exp(x)，然后exp(exp(x))，然后exp(exp(exp(x))),然后返回三个。这样如果要导数的话，只需要这三个值乘起来，就得到了。如果用简单的方法，你需要调用exp函数9次，用这个方法只要3次。

tf的autodiff来了：能自动并且高效的计算梯度。只要将gradients = 。。。替换：

```
gradients = tf.gradients(mse, [theta])[0]
```

gradients() 传入一个op（在这里是mse）和一个变量列表（这里是theta），然后它创建一个ops列表来计算op的梯度。

### 使用优化器

tf也提供了许多优化器，包括梯度下降优化器。可以简单的替换gradients = ... 和 training_op = ... 为：

```
optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
training_op = optimizer.minimize(mse)

```

如果要选择其他优化器，只要改变一行，比如你可以使用momentum optimizer（可以比梯度下降更快收敛）：

```
optimizer = tf.train.MomentumOptimizer(learning_rate=learning_rate,
momentum=0.9)
```
