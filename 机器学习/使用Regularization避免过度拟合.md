## 使用Regularization避免过度拟合

深神网通常有成千上万个参数，有时候甚至百万级别的。有这么多参数，网络有着难以置信的自由度并可以适应各种各样的复杂数据集。但这种极大的灵活性也意味着它很容易过度拟合训练集。

有数百万个参数，你可以适配整个动物园。这篇展示一些最流行的神网的正规化技术，还有如何用tf实现：early stopping, ℓ1 and ℓ2 regularization, dropout, max-norm regularization, 和 data augmentation.  

## Early Stopping    

为了避免过度拟合训练集，一个很好的方案是尽早停止：当其在验证集上的表现开始下降时，停止训练。

用TensorFlow实现这一点的一种方式是定期在验证集上评估模型（例如，每隔50个步骤），并且如果它胜过先前的“赢家”快照则保存“胜利者”快照。 计数自上次“赢家”快照保存以来的步数，以及当该数达到某个限制（例如，2,000步）时中断训练。 然后恢复最后的“赢家”快照。

尽管尽早停止在实践中运行良好，但通过将其与其他正则化技术相结合，您通常可以在网络中获得更高的性能。

## ℓ 1 and ℓ2 Regularization    

可以使用ℓ 1 和 ℓ2 Regularization 约束一个神网的连接权重（但通常不处理它的偏差）。

使用tf的一个方法是，简单的将适当的正则化术语添加到损失函数里。 例如，假设您只有一个权重为weight1的隐藏层和一个权重为weight2的输出层，则可以像这样应用l1正则化：

```python
[...] # construct the neural network
base_loss = tf.reduce_mean(xentropy, name="avg_xentropy")
reg_losses = tf.reduce_sum(tf.abs(weights1)) + tf.reduce_sum(tf.abs(weights2))
loss = tf.add(base_loss, scale * reg_losses, name="loss")
```

然而，如果有许多层，这样并不方便。幸运的是，tf提供了一个更好的选择。许多方法创建变量（如get_variable() 或者fully_connected())接收一个*_regularizer 参数给每个创建好的变量（weights_regularizer)。你可以传递任何以权重为参数的函数并返回相应的正则化损失。l1_regularizer(), l2_regularizer(), 和 l1_l2_regularizer()  方法返回这样的方法：

```python
with arg_scope(
[fully_connected],
weights_regularizer=tf.contrib.layers.l1_regularizer(scale=0.01)):
    hidden1 = fully_connected(X, n_hidden1, scope="hidden1")
	hidden2 = fully_connected(hidden1, n_hidden2, scope="hidden2")
	logits = fully_connected(hidden2, n_outputs, activation_fn=None,scope="out")
    
```

这段代码创建了一个带有2个隐藏层和一个输出层的神网，并且它也创造一个节点计算ℓ1 正规化损失到每个图层的权重。tf自动的添加这些节点到一个指定的列表包含所有的损失。你只要添加正规化损失到你的总损失，这样：

```python
reg_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
loss = tf.add_n([base_loss] + reg_losses, name="loss")
```

别忘记添加正规化损失到你的总损失中，不然他们会被忽略。

## Dropout

深神网中最受欢迎的正则化技术是dropout。由G. E. Hinton 在2012年提出，Nitish Srivastava进一步细化。它被证明十分成功：即使是最先进的神网，仅仅通过添加dropout，就可以提高1-2%的准确度。这可能听起来不是很多，但是当一个模型具有95%的准确度时，获得2%的准确度提升意味着将错误率降低近40%（从5%到3%左右）。

它是一个相当简单的算法：在每次训练的每步，每个神经元（包括输入神经元但不包括输出神经元）有一个概率p会暂时的“丢掉”。意味着它将在这次训练阶段被完全忽略，但在下一步可能会被激活。超参数*p*叫**丢弃率**，并且通常被设为50%。训练后，神经元不再被丢弃。以上（除了后面讨论的细节）。

![1530493038.png](https://upload-images.jianshu.io/upload_images/3509189-bfb03cd58f88940c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这种野蛮粗暴的技术竟然能用？相当令人惊讶。就像一家公司运作的更好的办法是让员工通过抛硬币决定去不去上班？但是谁知道呢。说不定可行！公司显然会被迫调整其组织，它不能依赖任何人来给咖啡机放咖啡豆或者执行其他关键任务，因此这些工作必须分散给几个人身上。员工必须学习和其他同事合作，而不是他们中的小部分人合作。公司会变得更加的有弹力，如果一个人辞职，这并没有多大影响。这个idea对公司有没有用不知道，但是对于神网，肯定是有用的。受丢弃训练的神经元不能与其邻近的神经元共同适应;他们必须自己变得有用。他们也不能过分的依赖一些输入神经元；他们必须关注所有的输入神经元。最终他们对输入的微小变化不太敏感。最后得到一个泛化更好的更强大的网络。

另一种理解丢弃的力量是认识到每个训练阶段训练处的神网是独一无二的。由于每个神经元可有可无，因此会有2的n次方个可能的网络（其中n是可丢弃神经元的总数）。这是个巨大的数字，以至于几乎不可能对相同的神网进行两次采样。一旦运行了10000次训练阶段，基本上你训练了10000个不同的神经网络（每次只有一个训练实例）。这些神经网络显然不是独立的，因为他们共享许多权重，但它们都是不同的。由此产生的神网可以看做所有这些小神经网络的平均集合。

有一个小而重要的技术细节。假设p=50，测试期间，神经元将连接到训练期间（平均）2倍的输入神经元。为了补偿这个事实，我们需要在训练后将每个神经元的输入连接权重乘以0.5，如果不这样做，每个神经元的总输入信号大约是网络训练的2倍，并且可能表现不好。换句话说，我们需要在训练后将每个输入连接权重乘以维持概率（1-p)。或者我们可以在训练过程中，将每个神经元的输出除以维持概率（这些方案并不完全等效，但工作的不错）。

为了使用tf实现丢弃，你可以简单的应用**dropout()**方法给输入层和每个隐藏层的输出。在训练时，这个方法随机的丢掉一些项（设置为0）并用保留概率来划分剩余项目。训练后，这个方法什么都不做。

```python
from tensorflow.contrib.layers import dropout

[...]
is_training = tf.placeholder(tf.bool,shape=(),name='is_training')
keep_prob = 0.5
X_drop = dropout(X,keep_prob,is_training=is_training)
hidden1 = fully_connected(X_drop,n_hidden1,scope="hidden1")
hidden1_drop = drop(hidden1,keep_prob,is_training)
hidden2 = fully_connected(hidden1_drop,n_hidden2,scope="hidden2")
hidden2_drop = drop(hidden2,keep_prob,is_training)

logits = fully_connected(hidden2_drop,n_outputs,activation_fn=None,scope="outputs")
```

要用tensorflow.contrib.layers的dropout()而不是tensorflow.nn，第一个在不训练的时候关闭，这是你希望的，第二个则不会。

就像之前的Batch Normalization，你需要设置当训练时，is_training为True，测试时，为False。

如果你看到模型过度拟合，你可以增加丢弃率（减小keep_prob超参数）。相反的，如果模型欠拟合，你应该减小丢弃率（增加keep_prob）。它还可以帮助增加大神经层的丢弃率，并减少小神经层的丢弃率。

丢弃倾向于显著减缓收敛速度，但通常会在调整得当的时候得到更好的模型。所以值得花额外的时间和精力。

Dropconnect是丢弃的变体，其中单个连接随机丢弃而不是整个神经元，一般来说，丢弃表现会更好。

## 最大范数规则化

另一个神网相当流行的规则化技术叫最大范数规则化（**max-norm regularization**):对每个神经元，它约束每个神经元的权重w，使得||w||2 <= r,其中r是最大范数超参数， ||.||2 是ℓ 2范数。

我们通常通过在每次训练阶段结束后计算||W||2并且有必要的时候修剪W （W  <—W r/(||w||2))实现这个约束。

减少r增加了规则化的数量，并且帮助减少过拟合。最大范数规则化（简称最大范规）可以帮助减缓梯度消失/爆炸问题（如果没有使用Batch Normalization）。

tf没有提供一个标准的最大范规器，但它也不难实现。以下代码创建了一个剪辑的节点clip_weights
权重可以沿第二轴变化，以便每个行向量具有最大范数1.0：

```python
threshold = 1.0
clipped_weights = tf.clip_by_norm(weights,clip_norm=threshold,axes=1)
clip_weights = tf.assign(weights,clipped_weights)
```

然后应用这个操作到每个训练阶段：

```python
with tf.Session as sess:
    [...]
    for epoch in range(n_epochs):
        [...]
        for X_batch,y_batch in zip(X_batches,y_batches):
            sess.run(training_op,feed_dict={X:X_train,y:y_batch})
            clip_weights.eval()
```

你可能想知道如何访问每个层的权重变量。 为此，你可以简单地使用这样的变量作用域：

```python
hidden1 = fully_connected(X,n_hidden1,scope="hidden1")

with tf.variable_scope("hidden1",reuse=True):
    weights1 = tf.get_variable("weights")

# 或者
hidden1 = fully_connected(X,n_hidden1,scope="hidden1")
hidden2 = fully_connected(hidden1,n_hidden2,scope="hidden2")
[...]

with tf.variable_scope("",default_name="",reuse=True): #root scope
    weights1 = tf.get_variable("hidden1/weights")
    weights2 = tf.get_variable("hidden2/weights")    
```

如果你不知道变量名是什么的时候，可以使用TensorBoard来找到，或者简单的使用**global_variables()**方法，然后打印所有的变量名：

```python
for variable in tf.global_variables():
    print(variable.name)
```

虽然前面的解决方案能行，但是有点脏乱。一个更干净的方案是创建一个**max_norm_regularizer()**方法，然后使用它：

```python
def max_norm_regularizer(threshold,axes=1,name="max_norm",
                        collection="max_norm"):
    def max_norm(weights):
        clipped = tf.clip_by_norm(weights,clip_norm=threshold,axes=axes)
        clip_weights = tf.assign(weights,clipped,name=name)
        tf.add_to_collection(collection, clip_weights)
        return None # there is no regularization loss term
    return max_norm
```

该函数返回参数化的max_norm（）函数，可以像其他任何调整器一样使用该函数：

```python
max_norm_reg = max_norm_regularizer(threshold=1.0)
hidden1 = fully_connected(X, n_hidden1, scope="hidden1",
                          weights_regularizer=max_norm_reg)
```

请注意，最大范数正则化不需要为整体损失函数添加正则化损失项，所以max_norm（）函数返回None。 但是，你仍然需要在每个训练阶段后都执行clip_weights操作，因此您需要得到它的一个句柄。 这就是max_norm（）函数将clip_weights节点添加到max-norm剪裁操作集合的原因。 您需要获取这些裁剪操作并在每个训练阶段后执行它们：

```python
clip_all_weights = tf.get_collection("max_norm")

with tf.Session() as sess:
    [...]
    for epoch in range(n_epochs):
        [...]
        for X_batch,y_batch in zip(X_batches,y_batches):
            sess.run(training_op,feed_dict={X:X_batches,y:y_batches})
            sess.run(clip_all_weights)
```

是不是更干净了些。

## 数据增强

最后一个规则化技术，数据增强,从已有数据中生成新的训练实例，人造的扩大训练集的大小。这会减少过拟合。诀窍是生成逼真的训练实例;理想情况下，人们分辨不出哪些是生成的哪些不是。而且，简单地添加白噪声也没有帮助，你应用的修改应该是可以学习的（白噪音不能）。

比如，你的模型是为了对蘑菇图片进行分类，你可以通过不同的小移动，旋转和调整训练集中每张照片的大小，并将得到的图片添加到训练集中。这迫使模型更能容忍图片中蘑菇的位置，方向和大小。如果希望对光照条件更加宽容，则可以类似的生成具有各种对比度的许多图像，假设蘑菇是对称的，也可以水平翻转图片，通过结合这些转换，可以大大增加训练集的大小。

通常最好在培训期间生成训练实例，而不是浪费存储空间和网络带宽。 TensorFlow提供了多种图像处理操作，例如移调（移位），旋转，调整大小，翻转和裁剪，以及调整亮度，对比度，饱和度和色调（请参阅API文档以获取更多详细信息）。 这使得为图像数据集实现数据增强变得很容易。

训练非常深的神经网络的另一个强大技术是添加跳过连接（跳过连接是将层的输入添加到较高层的输出时）。

## 实战指导


| 默认DNN配置                |                     |
| ---------------------- | ------------------- |
| Initialization         | He initialization   |
| Activation function    | ELU                 |
| Normalization          | Batch Normalization |
| Regularization         | Dropout             |
| Optimizer              | Adam                |
| Learning rate schedule | None                |

当然，如果你能找到解决类似问题的模型，你应该尝试重新使用它预训练神经网络的一部分。

这个默认配置碰到几种情况，需要修改：

- 如果不能找到一个好的学习率（收敛太慢，所以你提高了训练率，现在收敛很快，但是网络的准确率不理想），那么你可以试着添加一个学习时间表如指数衰减。
- 如果训练集太小，可以实现数据增强
- 如果你需要一个稀疏模型，你可以在混合中添加一些l1正则化（并且可以在训练之后选择性地将微小的权重归零）。 如果你需要一个更稀疏的模型，你可以尝试使用FTRL而不是Adam优化，以及ℓ1正则化
- 如果你需要一个运行时快速的模型，则可能需要丢弃Batch Normalization，然后替换ELU为 会漏的ReLU，也可以用稀疏模型。

有这些指导，你现在可以训练非常深的网络——如果你很有耐心，那以上，就这些。如果你使用一台机器，你可能需要等待许多天或者几个月让训练完成。
