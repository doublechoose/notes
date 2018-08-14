tf的基本原则很简单：首先用python定义一个计算图来执行，然后tf拿走这个图，使用优化的C++代码高效执行。

创建第一个图，并在Session中运行。

```python
import tensorflow as tf

x = tf.Variable(3,name="x")
y = tf.Variable(3,name="y")
f = x*x*y + y + 2
```

这段代码实际上没有做任何计算操作，只是创建了一个图。实际上，连变量都没有初始化。为了计算这个图，你需要打开TensorFlow的Session，然后用它去初始化变量并评估**f** . session负责将*操作* 放入如CPU和GPU这样的设备中，然后运行他们。并且它保管所有的变量值。

下面这段代码创建了一个session，初始化变量，并且赋值，然后运行**f**,然后关闭session（释放资源）。

```python
sess = tf.Session()
sess.run(x.initializer)
sess.run(y.initializer)
result = sess.run(f)
result
sess.close()
#厌倦了重复写sess？可以这样写
with tf.Session as sess:
    x.initializer.run()
    y.initializer.run()
    result = f.eval()
```

调用x.initializer.run()等同于tf.get_default_session().run(x.initializer)

调用f.eval() 等同于tf.get_default_session().run(f)

该session会在block的最后自动close。

除了手工为每个变量初始化，还可以使用方法global_variables_initializer(),它没有马上执行初始化，而是在图中创建一个note节点，当运行的时候才对所有变量进行初始化：

```python
init = tf.global_variables_initializer() #prepare an init node

with tf.Session as sess:
    init.run() # actually initialize all the variables
    result = f.eval()
```

在Jupyter或者python shell中可以使用InteractiveSession。和普通的Session的唯一区别是当InteractiveSession 第一次被创建后它自动的设置自己为默认的session，从而不用写在block中，但最后还是要手动的close。

```
>>> sess = tf.InteractiveSession()
>>> init.run()
>>> result = f.eval()
>>> print(result)
>>> 42
>>> sess.close()
```

tf编程分为两部分:第一部分构建一个计算图（构建期），第二部分运行它（执行期）。构建期通常构建一个计算图描述ML模型和训练它所需要的计算。执行期运行一个循环重复评估训练步骤（如，每次一小撮数据）。最终改良模型参数。

