## 给训练算法喂数据

我们对之前的代码修改成小撮梯度下降。为此，我们需要一个方法来将X和y替代为每次迭代用的下一个小撮数据。最简单的方法是使用placeholder节点。这些节点不做任何计算。他们只输出你要他们在运行时输出的数据。他们通常用于传递训练数据到tf。如果你在运行时不为placeholder指定一个值，会报错。

创建一个placeholder：

```python
A = tf.placeholder(tf.float32,shape(None,3))
B = A + 5
with tf.Session() as sess:
  B_val_1 = B.eval(feed_dict={A:[[1,2,3]]})
  B_val_2 = B.eval(feed_dict={A:[[4,5,6],[7,8,9]]})
 
print(B_val_1)
[[6. 7. 8.]]
print(B_val_2)
[[ 9. 10. 11.]
 [12. 13. 14.]]
```

指定None，表示any size。

为了实现小撮梯度下降，只要修改下已有代码。首先是在构建期修改X和y的定义：

```
X = tf.placeholder(tf.float32,shape(None,n+1),name="X")
y = tf.placeholder(tf.float32,shape(None,1),name="y")
```

然后定义batch大小和计算总的batch

```
batch_size = 100 # 一撮多少个数据
n_batches = int(np.ceil(m/batch_size)) # 多少撮
```

最后，在执行期，一个一个的喂，然后提供评估依赖的节点时，通过feed_dict 参数计算：

```python
def fetch_batch(epoch, batch_index,batch_size):
  [...] # load the data from disk
  return X_batch,y_batch

with tf.Session() as sess:
  sess.run(init)
  
  for epoch in range(n_epochs):
    for batch_index in range(n_batches):
      X_batch,y_batch = fetch_batch(epoch,batch_index,batch_size)
      sess.run(training_op,feed_dict={X:X_batch,y:y_batch})
  
  best_theta = theta.eval()
```

## 保存和恢复模型

当你训练好你模型，你应该保存到磁盘，这样就能在另一个程序中使用、和其他模型进行比较等等。而且，你可能想在训练中保存checkpoint，这样你的电脑在训练时崩溃，你可以从上一个checkpoint继续，而不是从头开始。

tf让保存和恢复模型变得简单。只要在构建期的最后创建一个Saver节点。然后在执行期，调用它的save()方法。

```python
[...]
theta = tf.Variable(tf.random_uniform([n+1,1],-1.0,1.0),name="theta")
[...]
init = tf.global_variables_initializer()
saver = tf.train.Saver()

with tf.Session() as sess:
  sess.run(init)
  
  for epoch in range(n_epochs):
    if epoch % 100 == 0: # checkpoint every 100 epochs
      save_path = saver.save(sess, '/tmp/my_model.ckpt')
    
    sess.run(training_op)
  save_path = saver.save(sess,'/tmp/my_model_final.ckpt')
  
```

恢复模型也很简单：在构建期最后创建一个Saver，然后在执行期开始前，调用restore()方法：

```python
with tf.Session() as sess:
  saver.restore(sess, '/tmp/my_model_final.ckpt')
  [...]

```

默认的，Saver保存和恢复使用变量自己的名字，也可自己指定哪个变量保存和恢复，使用什么名字。

```python
saver = tf.train.Saver({"weight":theta})
```

### 使用TensorBoard

现在我们有一个计算图，使用小撮梯度下降训练了一个线性回归模型，并且我们在几个间隔间保存了checkpoint，听起来很复杂，是把，然而我们还用print()来视觉化进度。有个更好的方法：TensorBoard。如果喂给它一些训练统计数据，它会在浏览器中显示出很好的交互式可视化效果（如学习曲线）。这很有用，可以查明图中的错误，找到瓶颈等等。

首先是修改下你的程序，写一些图的定义和一些训练统计数据。每次运行的时候都要用不同的log文件夹，否则TensorBoard会从不同的运行中合并统计数据。最简单的方法是使用时间戳：

```python
from datetime import datetime

now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
root_logdir = "tf_logs"
logdir = "{}/run-{}/".format(root_logdir,now)


```



下一步在每个构建期后面添加：

```python
mse_summary = tf.summary.scalar('MSE',mse)
file_writer = tf.summary.FileWriter(logdir,tf.get_default_graph())
```

第一行在图中创建一个节点，用于评估MSE并写到TensorBoard-compatible 二进制log叫 summary。第二行创建一个FileWriter将summaries写入到文件中，第一个参数为log的文件路径。第二参数为你想可视化的图。

下一步，需要在训练时更新执行期评估mse_summary节点值。这会输出一个summary，然后使用file writer写入到事件。

```python
[...]
for batch_index in range(n_batches):
  X_batch,y_batch = fetch_batch(epoch,batch_index,batch_size)
  if batch_index % 10 == 0:
    summary_str = mse+summary.eval(feed_dict={X:X_batch,y:y_batch})
    step = epoch * n_batches + batch_index
    file_writer.add_summary(summary_str,step)
  sess.run(training_op, feed_dict{X:X_batch,y:y_batch})
[...]
```

避免每次训练迭代记录日志，这会让训练变慢。

在程序的最后关闭FileWriter:

```
file_writer.close()
```

运行程序，现在它会创建log文件夹，并写入一个包含图定义和MSE值的文件，打开shell进到你的工作区，输入 **ls -l tf_logs/run\***

打开TensorBoard：

```
tensorboard --logdir tf_logs/
```

### 命名范围

当处理更多复杂模型如神经网络时，图会有成千上万的节点。为了避免这个，可以对相关联的节点进行创建命名范围。

```python
with tf.name_scope("loss") as scope:
    error = y_pred - y
    mse = tf.reduce_mean(tf.square(error),name="mse")
```

现在每个在scope中的op会带有前缀"loss/":

```
print(error.op.name)
loss/sub
print(mse.op.name)
loss/mse
```

