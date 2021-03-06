典型的CNN架构堆叠一些卷积层（每个卷层通常后跟一个ReLU层），然后是池化层，然后是另外几个卷积层（+ ReLU），然后是另一个池化层，依此类推。随着图像在网络中的进展，图像越来越小，但由于卷积层，它通常也会越来越深（即有更多的特征图）（见图13-9）。

常见的错误是使用太大的卷积内核。 通过将两个3×3内核堆叠在一起，您通常可以获得与9×9内核相同的效果，从而减少计算量。

![1530589040544.png](https://upload-images.jianshu.io/upload_images/3509189-44cb8b172c8905bb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


多年来，已经开发出这种基本架构的许多变体，从而在该领域取得了惊人的进步。 衡量这一进展的一个很好的方法是竞赛中比较错误率，例如ILSVRC [ImageNet挑战](http://image-net.org/)。

我们将首先看看经典的LeNet-5架构（1998），然后是ILSVRC挑战的三个获胜者：AlexNet（2012），GoogLeNet（2014）和ResNet（2015年）。

## LeNet-5

LeNet-5架构可能是最广为人知的CNN架构了。如前所述，它由Yann LeCun在1998所创，并广泛用于手写数字识别（MNIST）。它这样组合神经层

| Layer | Type            |Map| Size | Kernel size | Activation | Stride |
| ----- | --------------- | ---- | ----------- | ------ | ---------- | ---------- |
| Out   | Fully Connected | -    | 10          | -      | RBF        |-|
| F6    | Fully Connected | -    | 84          | -      | tanh       |-|
| C5    | Convolution     | 120  | 1 x 1       | 5 x 5  | tanh       |1|
| S4    | Avg Pooling     | 16   | 5 x 5       | 2 x 2 | tanh       |2|
| C3 | Convolution | 16 | 10 x 10 | 5 x 5 | tanh       |1|
| S2 | Avg Pooling | 6 | 14 x 14 | 2 x 2 | tanh       |2|
| C1 | Convolution | 6 | 28 x 28 | 5 x 5 | tanh       |1|
| In | Input | 1 | 32 x 32 | - | -       |-|

有些额外的细节值得注意：

- MNIST 图片是28 x 28的，但是它们被零填充到32×32像素并在送到网络之前被标准化。网络的其余部分不使用任何填充，这就是随着图像通过网络进展而尺寸不断缩小的原因。
- 平均池化层比平常稍微复杂一些：每个神经元计算其输入的平均值，然后将结果乘以可学习的系数（每个映射一个）并添加可学习的偏差项（再次，每个映射一个），然后最终应用 激活函数。
- C3图中的大多数神经元仅与三个或四个S2图（而不是所有六个S2图）中的神经元相连。 有关详细信息，请参阅原始文件。
- 输出层有点特殊：不是计算输入和加权矢量的点积，而是每个神经元输出其输入矢量与其权重矢量之间的欧几里德距离的平方。 每个输出测量图像属于特定数字类的程度。 交叉熵成本函数现在是首选，因为它可以更好地处理不良预测，产生更大的梯度，从而更快地收敛。

Yann LeCun的[网站](http://yann.lecun.com/)（“LENET”部分）展示了LeNet-5分类数字的精彩演示。

## AlexNet

[AlexNet CNN 架构](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf)赢得了2012年ImageNet ILSVRC 挑战赛：Top-5错误率达到了17％，而第二名最好的只达到了26％！ 它由Alex Krizhevsky（因此得名），Ilya Sutskever和Geoffrey Hinton开发。 它与LeNet-5非常相似，只是更大更深，它是第一个将卷积层直接堆叠在彼此之上，而不是在每个卷积层顶部堆叠汇集层。 表13-2显示了此体系结构。

| Layer | Type            | Maps   | Size      | Kernel size | Stride | Padding | Activation |
| ----- | --------------- | ------ | --------- | ----------- | ------ | ------- | ---------- |
| Out   | Fully Connected | -      | 1000      | -           | -      | -       | Softmax    |
| F9    | Fully Connected | -      | 4096      | -           | -      | -       | ReLU       |
| F8    | Fully Connected | -      | 4096      | -           | -      | -       | ReLU       |
| C7    | Convolution     | 256    | 13 x 13   | 3 x 3       | 1      | SAME    | ReLU       |
| C6    | Convolution     | 384    | 13 x 13   | 3 x 3       | 1      | SAME    | ReLU       |
| C5    | Convolution     | 384    | 13 x 13   | 3 x 3       | 1      | SAME    | ReLU       |
| S4    | Max Pooling     | 256    | 13 x 13   | 3 x 3       | 2      | VALID   | -          |
| C3    | Convolution     | 256    | 27 x 27   | 5 x 5       | 1      | SAME    | ReLU       |
| S2    | Max Pooling     | 96     | 27 x 27   | 3 x 3       | 2      | VALID   | -          |
| C1    | Convolution     | 96     | 55 x 55   | 11 x 11     | 4      | SAME    | ReLU       |
| In    | Input           | 3(RGB) | 224 x 224 | -           | -      | -       | -          |

为了减少过拟合，作者使用2个规则化技术：第一，他们在训练时层F8和F9的输出层应用了丢弃（50% 的丢弃率），第二，他们通过许多偏移随机水平移动训练集图片，并且改变光线条件。

AlexNet还在层C1和C3的ReLU步骤之后立即使用竞争标准化步骤，叫**local response normalization**，这种标准化形式使得最强烈激活的神经元在相同位置但在相邻特征图中抑制神经元（在生物神经元中已经观察到这种竞争激活）。 这鼓励不同的特征图专门化，将它们分开并迫使它们探索更广泛的特征，最终改进泛化。 公式13-2显示了如何应用LRN。

![1530597830916.png](https://upload-images.jianshu.io/upload_images/3509189-ed596e8fe8373a11.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- bi是位于特征映射i中的神经元的归一化输出，位于某行u和v列（请注意，在此等式中我们只考虑位于此行和列的神经元，因此u和v未显示）
- ai是在ReLU步骤之后但在归一化之前激活该神经元
- k，α，β和r是超参数。 k称为偏差，r称为深度半径。
- fn是特征映射的数量。

比如，如果r = 2，并且一个神经元有一个强激活，它会抑制位于其自身上下的特征图中的神经元的激活。

在AlexNet中，超参数设置如下：r = 2，α= 0.00002，β= 0.75，并且k = 1.可以使用TensorFlow的local_response_normalization（）操作来实现该步骤。

## GoogLeNet    

[GoogLeNet架构](http://www.cs.unc.edu/~wliu/papers/GoogLeNet.pdf)由Christian Szegedy等人开发。 来自Google Research，它通过将前5个错误率降至7％以下而赢得了ILSVRC 2014的挑战。 这种出色的表现在很大程度上源于网络比以前的CNN更深的事实（见图13-11）。 这是通过称为初始模块的子网络实现的，11允许GoogLeNet比以前的架构更有效地使用参数：GoogLeNet实际上的参数比AlexNet少10倍（大约600万而不是6000万）。

图13-10显示了初始模块的体系结构。 符号“3×3 + 2（S）”表示该层使用3×3内核，步幅2和SAME padding。 首先复制输入信号并将其馈送到四个不同的层。 所有卷积层都使用ReLU激活功能。 请注意，第二组卷积层使用不同的内核大小（1×1,3×3和5×5），允许它们捕获不同比例的模式。 另请注意，每个单独一层使用1和SAME填充的步幅（即使是最大池化层），因此它们的输出都具有与其输入相同的高度和宽度。 这使得可以在最终深度连续层中连接沿深度维度的所有输出（即，堆叠来自所有四个顶部卷积层的特征映射）。 可以使用**concat()**操作在TensorFlow中实现此连接层，其中axis = 3（轴3是深度）。

![1530598455663.png](https://upload-images.jianshu.io/upload_images/3509189-bfca89a5caeacf4f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


您可能想知道为什么初始模块具有1×1内核的卷积层。 当然这些层无法捕获任何特征，因为它们一次只能看到一个像素？ 实际上，这些层有两个目的：

- 首先，它们被配置为输出比输入更少的特征映射，因此它们充当瓶颈层，这意味着它们降低了维度。这在3×3和5×5卷绕之前特别有用，因为这些是计算上非常昂贵的层。
- 其次，每对卷积层（[1×1,3×3]和[1×1,5×5]）就像一个强大的卷积层，能够捕获更复杂的模式。 实际上，不是在图像上扫描简单的线性分类器（如单个卷积层那样），这对卷积层扫描图像上的两层神经网络。

简而言之，您可以将整个初始模块视为类固醇上的卷积层，能够输出捕获各种尺度复杂模式的特征图。

每个卷积层的卷积核的数量是超参数。 不幸的是，这意味着你需要为你添加的每个初始层调整六个超参数。

现在让我们来看看GoogLeNet CNN的架构（参见图13-11）。 它非常深，以至于我们必须在三列中表示它，但GoogLeNet实际上是一个高堆栈，包括九个初始模块（带有旋转顶部的盒子），每个模块实际上包含三个层。 每个卷积层和每个池化层输出的特征映射的数量显示在内核大小之前。 初始模块中的六个数字表示模块中每个卷积层输出的特征映射的数量（与图13-10中的顺序相同）。 请注意，所有卷积层都使用ReLU激活功能。

![1530598845323.png](https://upload-images.jianshu.io/upload_images/3509189-49e3f84b59bee76b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


我们来看下这个网络：

- 前两层将图像的高度和宽度除以4（因此其面积除以16），以减少计算负荷。
- 然后，本地响应规范化层确保先前的层学习各种各样的功能（如前所述）
- 接下来是两个卷积层，其中第一个层就像一个瓶颈层。 如前所述，您可以将此对视为一个更智能的卷积层
- 同样，本地响应规范化层确保先前的层捕获各种各样的模式。
- 接下来，最大池化层将图像高度和宽度减小2，再次加快计算速度
- 然后是九个初始模块的高堆栈，与几个最大池交错，以减少维数并加速网络。
- 接下来，平均池层使用具有VALID padding的特征映射大小的内核，输出1×1特征映射：这种令人惊讶的策略称为全局平均池。 它有效地强制前面的层生成特征映射，这些特征映射实际上是每个目标类的置信映射（因为其他类型的特征将被平均步骤破坏）。 这使得不必在CNN顶部有几个完全连接的层（如AlexNet），大大减少了网络中的参数数量并限制了过度拟合的风险。
- 最后一层是不言自明的：用于正则化的丢失，然后是具有softmax激活函数的完全连接的层，以输出估计的类概率。

该图略有简化：原始的GoogLeNet架构还包括两个辅助分类器，它们插在第三和第六个初始模块之上。 它们都由一个平均池化层，一个卷积层，两个完全连接的层和一个softmax激活层组成。 在训练期间，他们的损失（按比例缩小70％）增加了整体损失。 目标是消除消失的渐变问题并使网络正规化。 但是，它表明它们的影响相对较小。

## ResNet    

最后还有一个很重要的，2015年ILSVRC挑战赛的获胜者是[残余网络](https://arxiv.org/pdf/1512.03385v1.pdf)（或ResNet），由Kaiming He等人开发，使用由152层组成的极深CNN，使得前5个错误率低于3.6％。 能够训练这种深度网络的关键是使用**skip connections(跳过连接）**（也称为快捷连接）：喂给神经层的信号也被添加到位于堆栈上方一点的层的输出。 让我们看看为什么这很有用。

在训练神经网络时，目标是使其模拟目标函数h（x）。 如果将输入x添加到网络的输出（即，添加跳过连接），则网络将被强制建模f（x）= h（x） - x而不是h（x）。 这称为残差学习（见图13-12）。

![1530599922137.png](https://upload-images.jianshu.io/upload_images/3509189-40acb9046ddd12e9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

初始化一个常规神经网络时，其权重接近于零，因此网络只输出接近零的值。 如果添加跳过连接，则生成的网络只输出其输入的副本; 换句话说，它最开始只模拟身份函数。 如果目标函数非常接近身份函数（通常是这种情况），这将大大加快训练速度。

此外，如果添加许多跳过连接，即使多个层尚未开始学习，网络也可以开始进行（参见图13-13）。 由于跳过连接，信号可以轻松地穿过整个网络。 深度剩余网络可被视为一堆剩余单元，其中每个剩余单元是具有跳过连接的小型神经网络。

![1530600139292.png](https://upload-images.jianshu.io/upload_images/3509189-f688257205cac799.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


现在让我们看看ResNet的架构（参见图13-14）。 它实际上非常简单。 它的开始和结束与GoogLeNet完全相同（除了没有丢失层），其间只是一个非常深的简单剩余单元堆栈。 每个残差单元由两个卷积层组成，具有批量归一化（BN）和ReLU激活，使用3×3内核并保留空间维度（步幅1，SAME填充）。

![1530600215433.png](https://upload-images.jianshu.io/upload_images/3509189-0d4fce836594e8aa.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


请注意，每几个残差单位的特征映射数量加倍，同时它们的高度和宽度减半（使用带有步幅2的卷积层）。 发生这种情况时，输入不能直接添加到剩余单元的输出中，因为它们的形状不同（例如，此问题会影响图13-14中虚线箭头所示的跳过连接）。 为了解决这个问题，输入通过带有步幅2的1×1卷积层和正确数量的输出特征映射（见图13-15）

![1530600306476.png](https://upload-images.jianshu.io/upload_images/3509189-6353e3f2d019ad45.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


ResNet-34是具有34层（仅计算卷积层和完全连接层）的ResNet，包含三个输出64个特征图的残余单元，4个具有128个映射的RU，6个具有256个映射的RU，以及3个具有512个映射的RU.

更深层次的ResNets，例如ResNet-152，使用稍微不同的剩余单位。 它们使用三个卷积层而不是两个3×3卷积层（例如）256个特征图，第一个是1×1卷积层，只有64个特征映射（少4倍），它们起着瓶颈层的作用（如前所述） 然后是具有64个特征图的3×3层，最后是具有256个特征图（4倍64）的另一个1×1卷积层，其恢复原始深度。 ResNet-152包含三个这样的RU，它们输出256个映射，然后是8个具有512个映射的RU，一个高达36个RU和1,024个映射，最后是3个具有2,048个映射的RU。

正如你所看到的，该领域正在迅速发展，每年都会出现各种各样的架构。 一个明显的趋势是CNN越来越深入。 它们也越来越轻，需要的参数越来越少。 目前，ResNet架构既是最强大的，也可能是最简单的架构，所以它实际上是你现在应该使用的架构，但每年都要关注ILSVRC的挑战。 2016年的获奖者是来自中国的Trimps-Soushen团队，错误率高达2.99％。 为了实现这一目标，他们训练了之前模型的组合并将它们组合成一个整体。 根据任务的不同，降低的错误率可能会或可能不值得额外的复杂性。

您可能还需要了解一些其他架构，特别是VGGNet13（ILSVRC 2014挑战赛的亚军）和Inception-v414（它融合了GoogLeNet和ResNet的想法，实现了接近3％的前5个错误 ImageNet分类率）。

实现我们刚刚讨论的各种CNN架构并没有什么特别之处。 我们之前看到了如何构建所有单独的构建块，因此现在你只需要组装它们以创建所需的体系结构。 我们将在即将到来的练习中构建ResNet-34，您将在Jupyter notebook中找到完整的代码。

### tf卷积操作

TensorFlow还提供了一些其他类型的卷积层：

- conv1d（）为1D输入创建卷积层。 例如，这在自然语言处理中是有用的，其中句子可以表示为单词的一维数组，并且接收字段覆盖几个相邻的单词。
- conv3d（）为3D输入创建卷积层，例如3D PET扫描
- atrous_conv2d（）创建了一个令人生畏的卷积层（“àtrous”是法语“with holes”）。 这相当于使用规则的卷积层，其中滤波器通过插入行和列（即，孔）而扩展。 例如，等于[[1,2,3]]的1×3滤波器可以以4的膨胀率扩张，导致扩张的滤波[[1,0,0,0,2,0,0]， 0,3]]。 这允许卷积层在没有计算价格的情况下具有更大的感受野并且不使用额外的参数。
- conv2d_transpose（）创建一个转置卷积层，有时称为解卷积层，15对图像进行上采样。 它通过在输入之间插入零来实现，因此您可以将其视为使用分数步幅的常规卷积层。 上采样很有用，例如，在图像分割中：在典型的CNN中，当您在网络中前进时，要素图会变得越来越小，因此如果要输出与输入大小相同的图像，则需要上采样图层
- depthwise_conv2d（）创建深度卷积层，将每个滤波器独立应用于每个输入通道。 因此，如果有fn滤波器和fn'输入通道，那么这将输出fn×fn'特征映射。
- separable_conv2d（）创建一个可分离的卷积层，它首先像深度卷积层一样，然后将1×1卷积层应用于生成的特征映射。 这使得可以将滤波器应用于任意输入通道组。
