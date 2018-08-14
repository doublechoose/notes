### 模块化

ReLU 整流线性单元。ReLU计算一个线性函数的输入，输出结果，如果它是正的，否则为0.假设你要创建一个图2个ReLU相加的输出：

```python
n_features = 3
X = tf.placeholder(tf.float32,shape(None,n_features),name="X")

w1 = tf.Variable(tf.random_normal((n_features,1)),name="weight1")
w2 = tf.Variable(tf.random_normal((n_features,1)),name="weight2")
b1 = tf.Variable(0.0,name="bias1")
b2 = tf.Variable(0.0,name="bias2")

z1 = tf.add(tf.matmul(X,w1),b1,name="z1")
z2 = tf.add(tf.matmul(X,w2),b2,name="z2")


relu1 = tf.maximum(z1,0. name="relu1")
relu2 = tf.maximum(z1,0. name="relu2")

output = tf.add(relu1,relu2,name="output")
```

如上，这样重复的代码维护难且容易出错。tf让你遵守DRY（don't repeat yourself）原则：简单的创建一个方法来构建ReLU。

```python
def relu(X):
  w_shape = (int(X.get_shape()[1]),1)
  w = tf.Variable(tf.random_normal(w_shape),name="weights")
  b = tf.Variable(0.0,name="bias")
  z = tf.add(tf.matmul(X,w),b,name="z")
  return tf.maximum(z,0.,name="relu")

n_features = 3
X = tf.placeholder(tf.float32,shape=(None,n_features),name="X")
relus = [relu(X) for i in range(5)]
output = tf.add_n(relus,name="output") # relus里每个tensor进行相加
```

当创建一个节点，tf会检查这个名字是否存在，如果存在，则在名字后面添加  **_** 和一个index值。

使用name scope会让图更清晰。



### 共享变量

如果想在图的不同组件之间共享一个变量，一个简单的做法是先创建它然后作为参数传入到需要它的方法中。比如，假设想控制ReLU的阈值（当前是硬编码为0）,使用一个共享的阈值变量给所有的ReLU。可以先创建这个变量，然后传递给relu()方法中。

```python
def relu(X, threshold):
    with tf.name_scope("relu"):
        [...]
        return tf.maximum(z,threhold,name="max")

threshold = tf.Variable(0.0,name="threshold")
X = tf.placeholder(tf.float32,shape=(None,n_features),name="X")
relus = [relu(X,threshold) for i in range(5)]
output = tf.add_n(relus,name="output")
```

现在可以使用阈值控制所有ReLU的阈值变量。 然而，如果有许多像这样的共享参数要传，这很操蛋。很多人会使用Python字典包含所有的变量，传给每个函数，另一些人为每个模块创建一个类（如使用类的ReLU类变量来处理共享参数），另一种选择是在第一次调用时，将变量设置relu()方法的属性：

```python
def relu(X):
    with tf.name_scope("relu"):
        if not hasattr(relu,"threshold"):
            relu.threshold = tf.Variable(0.0,name="threshold")
        [...]
        retrurn tf.maximum(z,relu.threshold,name="max")
```

tf提供另外的选择，相比于之前的方案会更加干净和模块化。如果不存在，使用get_variable()方法创建共享变量，存在，则复用它。想要的行为（创建或复用）由当前的Variable_scope()属性决定。

```python
with tf.variable_scope("relu"):
    threshold = tf.get_variable("threshold",shape=(),
    initializer=tf.constant_initializer(0.0))
```

如果变量在之前就已经创建，那么就会抛出异常。此行为避免错误的复用变量。

如果你想复用一个变量，则需要指定，通过设置scope的reuse属性为True：

```python
with tf.variable_scope("relu",reuse = True):
    threshold = tf.get_variable("threshold")
#也可以这样写
with tf.variable_scope("relu") as scope:
    scope.reuse_variables()
    threshold = tf.get_variable("threshold")

```

这段代码会获取已有的“relu/threshold”变量，或者不存在或者没有使用get_variable()方法创建抛出异常。

一旦reuse设置为True，就不能在block中设置False回去。

现在你就可以这样写：

```python
def relu(X):
    with tf.variable_scope("relu",reuse=True):
        threshold = tf.get_variable("threshold") $ reuse existing variable
        [...]
        return tf.maxmum(z,threshold,name = "max")

X = tf.placeholder(tf.float32,shape(None,n_features),name="X")
with tf.variable_scope("relu"): #create the variable
    threshold = tf.get_variable("threshold",shape=(),
    initializer=tf.constant_initializer(0.0))
relus = [relu(X)for relu_index in range(5)]
output = tf.add_n(relus,name="output")
```
