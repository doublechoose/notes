## RMSProp

虽然AdaGrad减慢了一点速度，并且从未收敛到全局最优，但是RMSProp解决这个问题，通过累加最近迭代中的梯度（从训练开始后的所有梯度相对）。它通过在第一步中使用指数衰减来实现的。
![1530257763096.png](https://upload-images.jianshu.io/upload_images/3509189-db44d56c2dd955c4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


衰减率典型设为0.9，是的，又多了一个新的超参数，但这个默认值效果不错，所以你一点也不用调整。tf也实现了**RMSPropOptimizer **

```python
optimizer = tf.train.RMSPropOptimizer(learning_rate=learning_rate,
                                      momentum=0.9, decay=0.9, epsilon=1e-10)
```

除了非常简单的问题，这个优化器几乎完胜AdaGrad。它通常比动量优化和Nesterov加速梯度表现的更好，事实上在Adam优化之前，这是许多研究人员首选的优化算法。

## Adam Optimization    

[Adam](https://arxiv.org/pdf/1412.6980v8.pdf) 代表自适应矩估计，结合动量优化和RMSProp的思想：就像Momentum优化一样，它跟踪过去梯度的指数衰减平均值，就像RMSProp一样，它跟踪过去平方梯度的指数衰减平均值。
![1530258265731.png](https://upload-images.jianshu.io/upload_images/3509189-64789831465892d5.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


如果你只看第1、2和5步，你会发现Adam和动量优化和RMSProp相当类似。不同的区别是1计算一个指数衰减平均而不是指数衰减和，但这实际上是等价的，除了一个常数因子（衰减平均值指数衰减和的1-β1倍），步骤3和4是一个技术细节：**m**和**s**被初始化为0，他们在训练开始时会偏向0，所以这2步有助于在训练开始提升m和s。动量衰减超参数通常初始化为0.9，而缩放衰减超参数β2通常初始化为0.999. 如前所述，平滑项ε通常被初始化为诸如10-8的微小数字。 这些是TensorFlow的AdamOptimizer类的默认值，因此可以简单地使用它们：

```python
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
```

实际上，由于Adam是一种自适应学习速率算法（如AdaGrad和RMSProp），因此它需要的学习速率超参数η的调整较少。 您经常可以使用默认值η= 0.001，使得Adam比梯度下降更易于使用。

迄今为止讨论的所有优化技术仅依赖于一阶偏导数（雅可比矩阵）。 优化论文包含基于二阶偏导数（Hessians）的惊人算法。 不幸的是，这些算法很难应用于深度神经网络，因为每个输出有n^2个Hessians（其中n是参数的数量），而不是每个输出只有n个Jacobian。 由于DNN通常具有数以万计的参数，二阶优化算法通常甚至不适合内存，即使他们这样做时，计算Hessians的速度也太慢。

### 训练稀疏模型

刚刚提出的所有优化算法都会生成密集模型，这就是说大多数参数将不为零。 如果你在运行时需要一个非常快速的模型，或者如果你需要它占用较少的内存，你可能更喜欢以稀疏模式结束代替。

实现这一目标的一个小方法是照常训练模型，然后摆脱微小的权重（将它们设置为0）。

另一种选择是在训练期间应用强 ℓ1正则化，因为它会推动优化器尽可能多地消除权重.

但是，在某些情况下，这些技术可能仍然不足。 最后一个选择是应用双重平均，通常称为Follow Te Regularized Leader（FTRL），一种技术由Yurii Nesterov提出当与l1正则化一起使用时，这种技术往往导致非常稀疏的模型。 TensorFlow实现了一个称为FTRL的变体FTRLOptimizer类中的FTRL-Proximal。

## 学习率时间表

找一个好的学习率可能会很棘手。如果设置得太高，训练很可能偏离。如果设置的很小，训练最终会收敛到最优，但是需要很长的一段时间。如果设置的稍微高一点，一开始会让进度变快，但最后会在最优附近折返跑，沉淀不下来（除非你使用一个自适应学习率优化算法如AdaGrad，RMSProp，或者Adam，但即使是这样也需要时间下沉）。如果你有有限的计算预算，你可以在它适当收敛前中断训练，给出一个子最优的解决方案。
![1530260371798.png](https://upload-images.jianshu.io/upload_images/3509189-a025d8646741083e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



然而你可以做的比一个不变的学习率好：如果你从一个大的学习率开始，然后在它停止大下降的时候减少它，你就可以得到一个比学习率固定来的快的好的解决方案。有许多策略在训练时减少学习率，这些策略叫学习率时间表，最常用的有：

#### Predetermined piecewise constant learning rate

​	比如，一开始设置学习率为η0 = 0.1，然后在50期后设置η1 = 0.001。虽然这个方案能工作，但往往需要摆弄找出正确的学习速度以及何时使用它们。

#### Performance scheduling    

​	每N步测量验证错误（就像提前停止一样）和当错误停止下降时，将学习速率减小λ

####  Exponential scheduling    

​	将学习速率设置为迭代次数t的函数：η（t）=η0^10-t / r。 这个效果很好，但它需要调整η0和r。 学习率将每r步下降10倍

#### Power scheduling    

​	设学习率为η（t）=η0（1 + t / r）^-c。 超参数c通常被设置1。这与指数调度类似，但学习率下降更慢。

比较一些的表现当训练用于语音识别的深度神经网络时，最流行的学习时间表 - 使用Momentum优化进行识别。 Andrew Senior 的结论是，在这种情况下，performance scheduling和exponential scheduling 都表现良好，但他们偏爱Exponential scheduling，因为它实现起来更简单，易于调优，并稍微收敛到最佳解决方案。

用tf实现一个学习率时间表很直接：

```python
initial_learning_rate = 0.1
decay_steps = 10000
decay_rate = 1/10
global_step = tf.Variable(0, trainable=False)
learning_rate = tf.train.exponential_decay(initial_learning_rate, global_step,
                                           decay_steps, decay_rate)
optimizer = tf.train.MomentumOptimizer(learning_rate, momentum=0.9)
training_op = optimizer.minimize(loss, global_step=global_step)
```

设置完超参数的值后，我们创建一个非可训练变量global_step（init to 0），来追踪当前训练迭代次数。然后我们使用tf的exponential_decay() 方法定义一个指数衰减学习率（η0 = 0.1 and r = 10,000 ）。下一步，我们创建一个优化器（这里是MomentumOptimizer）来使用这个衰减学习率。最后我们创建一个训练操作，通过调用优化器的minimize()方法。因为我们传递了global_step变量，它会照顾好它的。以上！

由于AdaGrad，RMSProp和Adam优化会自动减少学习在培训期间的费率，没有必要增加额外的学习时间表。 对于其他优化算法，使用指数衰减或性能调度即可，大大加快了融合。

