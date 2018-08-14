## 管理图

创建的任何节点都会自动添加到默认的图中：

```python
>>> x1 = tf.Variable(1)
>>> x1.graph is tf.get_default_graph()
>>> True
```

当你要管理多个独立的图时，可以创建一个新图，并在block中暂时作为默认图，如下所示：

```python
graph = tf.Graph()
with graph.as_default():
    x2 = tf.Variable(2)
x2.graph is graph
>>> True
x.2.graph is tf.get_default_graph()
>>> False
```

在Jupyter或者python shell中，可能经常运行同样的命令多次，于是最后你的默认图中会包含多个重复节点。怎么办呢，一个是重启Jupyter，一个是使用重置默认图：```tf.reset_default_graph()```

## 节点值的生命周期

评估一个节点时，TF自动的决定所要依赖的节点集并首先赋值这些节点。

```python
w = tf.constant(3)
x = w + 2
y = x + 5
z = x * 3

with tf.Session() as sess:
    print(y.eval()) # 10
    print(z.eval()) # 15
```

这是个简单图。然后它开启一个session计算y：TF自动的检测到y依赖w，w依赖x，于是它先算w，然后x，然后y，并返回y的值。接下来计算z，同样的，tf必须先算w和x。注意，这里tf不会复用之前计算的w和x值。也就是x和w被算了2次。

所有的节点值除了变量值在图之间的运行，都会被丢弃。变量值会由session维护（queues和reader也维护一些）。变量从它的初始化执行开始它的生命周期，session close时结束生命。

如果不想重复计算w和x，就必须在一个图中同时计算y和z，如下：

```python
with tf.Session() as sess:
  y_val,z_val = sess.run([y,z])
  print(y_val) # 10
  print(z_val) # 15
```

在单进程tf中，多个session不共享任何状态，即使他们复用同一个图（每个session都有自己图的每个变量的副本）。在分布式tf中，变量存储在服务器上而不是在session中，所以多个session可以共享相同的变量。



