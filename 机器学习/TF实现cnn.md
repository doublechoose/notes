在tf，每个输入图片通常表示为一个3d shape的tensor[height,width,channels].一个小撮表示为一个4d shape 的tensor[mini-batch size,height,width,channels].卷积层的权重表示为一个4d shape 的tensor [fh,fw,fn,fn']。卷积层的偏差项简单的表示为1D shape 的 tensor[fn]。

我们来看个简单例子。下面代码载入2个样本图片，使用Scikit-Learn的**load_sample_images()**(载入2张彩色照片，一个是寺庙，一个是花)。然后它创建2个7x7的滤波器（一个中间带有垂直白线，另一个带有水平白线），将他们应用到tf的**conv2d()**构建的卷积层。最后画出结果的特征映射（同图13-5的右上角相似）。

```python
import numpy as np
from sklearn.datasets import load_sample_images
import tensorflow as tf
import matplotlib.pyplot as plt

# load sample images
dataset = np.array(load_sample_images().images,dtype=np.float32)
batch_size,height,width,channels = dataset.shape

# create 2 filters
filters_test = np.zeros(shape=(7,7,channels,2),dtype=np.float32)
filters_test[:,3,:,0] = 1 # vertical line
filters_test[3,:,:,1] = 1 # horizontal line

# create a graph with input X plus a convolutional layer applying the 2 filters
X = tf.placeholder(tf.float32,shape=(None,height,width,channels))
convolution = tf.nn.conv2d(X,filters_test,strides=[1,2,2,1],padding="SAME")
with tf.Session() as sess:
    output = sess.run(convolution,feed_dict={X:dataset})

plt.imshow(output[0,:,:,1])
plt.show()
```

讲下**conv2d()**:

- X是小撮的输入（一个4D tensor）

- filters 是要应用的滤波器集合

- strides是一个四元素1D数组，其中两个中心元素是垂直和水平步幅（sh和sw）。 第一个和最后一个元素当前必须等于1。它们可能有一天用于指定批量步幅（跳过某些实例）和通道步幅（跳过前一层的某些特征映射或通道）。

- padding 必须是 "VALID" 或者 "SAME":    

  ----如果设置为“VALID",卷积层不使用零填充，并且可以忽略输入图像底部和右侧的某些行和列，具体取决于步幅，如图13-7所示（为简单起见，此处仅显示水平尺寸， 但当然相同的逻辑适用于垂直维度）。

  ----如果设置为“SAME”，如果有需要，卷积层使用零填充。 在这种情况下，输出神经元的数量等于输入神经元的数量除以步幅，向上舍入（在该示例中，ceil（13/5）= 3）。 然后在输入周围尽可能均匀地添加零。

![1530585630006.png](https://upload-images.jianshu.io/upload_images/3509189-cbd6f58926ccd5b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


不幸的是，卷积有许多超参数：你必须选择滤波器的数量，他们的高度和宽度，步幅，还有padding类型。一如既往的，你可以使用cross-validation来找到正确的超参数值，但是十分耗时。我们稍后将讨论常见的CNN架构，以便了解哪些超参数值在实战中最有效。

## 内存要求

CNN的另一个问题是卷积层需要大量的RAM，特别是在训练的时候，因为反向传播的反向传递需要在前向传递期间计算的所有中间值。

比如，有一个卷积层带有一个5x5的滤波器，输出200个大小为150x100的特征映射，使用1步幅和padding为SAME类型。如果输入是一个150x100RGB的图片（3通道），那么参数数量为（5x5x3+1）x 200 = 15200（+1 对应于偏差项），与完全连接层相比，它相当小。然而在200个特征映射的每个包含150x100的神经元，并且这些神经元，每个神经元需要计算它的权重总和5x5x3 = 75的输入：总共有22500 0000个浮点型计算。不比一个全连接神经元来的少，但计算相当密集。此外，如果特征映射表示为使用32-bit floats，那么卷积层的输出会占用200x150x100x32=9600 0000位（大约11.4MB）的RAM。而这只是一个实例！如果训练包含100的batch，那么这卷积层会占用1GB的RAM！

在推理期间（即，在对新实例进行预测时），一旦计算出下一层，就可以释放一层占用的RAM，因此您只需要两个连续层所需的RAM。 但是在训练期间，在正向传递期间计算的所有内容都需要保留用于反向传递，因此所需的RAM量（至少）是所有层所需的RAM总量。

如果训练因为内存溢出报错，可以试着减少mini-batch的大小。或者，可以尝试使用步幅减少维度，或删除几个层。或者你可以使用16位的浮点型替代32位的。或者通过多设备分布计算。

## 池化层

一旦你理解了卷积层如何工作的，那么池化层很容易掌握。他们的目标是对输入图像进行二次采样（即缩小），以便减少计算负荷，存储器使用和参数的数量（从而限制过度拟合的风险）。减小输入图像尺寸也使神经网络容忍一点点图像偏移（位置不变性）。

正如卷积层，池化层中的每个神经元连接到前一层中有限数量的神经元的输出，位于小的矩形感受域内。你必须定义它的大小，步幅和padding 类型，如前所述。然而一个池化神经元没有权重；它所做的就是使用聚合函数（如max或mean）聚合输入。图13-8显示一个**max pooling layer**，这是池化层最常用类型。在这例子，我们使用一个2x2**池化核**，步幅为2，没有padding。注意，请注意，只有每个核中的最大输入值才能进入下一层。其他输入被丢弃。

![1530587838732.png](https://upload-images.jianshu.io/upload_images/3509189-db88297b49fadc84.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这显然是一种非常具有破坏性的层：即使是2×2的微小内核和2的步幅，两个方向的输出也会小两倍（因此它的面积将减小四倍），简单粗暴的丢弃75％的 输入值。

池化层通常独立地在每个输入通道上工作，因此输出深度与输入深度相同。 你也可以在深度维度上进行汇总，如下所示，在这种情况下，图像的空间维度（高度和宽度）保持不变，但通道数量会减少。

在tf实现一个最大池化层相当简单。下面代码创建了一个使用一个2x2核，步幅为2，没有padding的最大池化层，然后应用它到数据集中的所有图片。

```python
[...] # load the image dataset, just like above

# Create a graph with input X plus a max pooling layer
X = tf.placeholder(tf.float32, shape=(None, height, width, channels))
max_pool = tf.nn.max_pool(X, ksize=[1,2,2,1], strides=[1,2,2,1],padding="VALID")
with tf.Session() as sess:
	output = sess.run(max_pool, feed_dict={X: dataset})
    
# plot the output for the 1st image    
plt.imshow(output[0].astype(np.uint8)) 
plt.show()
```

*ksize*参数包含输入tensor的所有四个维度的核形状：[batch size, height, width, channels]。TensorFlow目前不支持对多个实例进行池化，因此ksize的第一个元素必须为1。此外，它不支持在空间维度（高度和宽度）和深度维度上汇集，因此ksize [1]和ksize [2]必须都等于1，或者ksize [3]必须等于1。

为了创建一个**average pooling layer**,只要使用**avg_pool()**方法取代max_pool()。

现在你知道了关于创建卷积神网的构建模块，下一篇来看如何装配他们。

[下一页](https://www.jianshu.com/p/0c9f7731a8c3)
