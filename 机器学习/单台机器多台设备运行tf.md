
在一个单CPU的机器上训练一个大型神经网络可以花费数天，甚至数月。

这里，我们将看看tf是如何多设备（CPUs和GPUs)分布计算和并行的。。 首先，我们将在一台机器上分配跨多个设备的计算，然后开始多台机器上的多台设备。

与其他神经网络框架相比，TensorFlow对分布式计算的支持是其主要亮点之一。它使你可以完全控制如何在设备和服务器之间分割（或复制）你的计算图，并且可以让你用灵活的方式并行化和同步操作，以便你可以在各种并行化方法之间进行选择。

我们将看看一些最流行的方法来并行执行和训练一个神网。不是等数周，而是几个小时内就能训练好一个算法。这不仅省了许多时间，这也意味着你可以轻松的尝试许多模型，并且可以用新数据重新训练你的模型。

并行的另一个好处是包括微调你的模型时探索更大的超参数空间，并有效地运行大量的神网。

但我们必须在跑之前先学会走。我们从有多个GPU的一台机器里并行执行一个简单图开始。

## 单台机器多台设备

你可以通过将GPU卡添加到单个机器上，就能获得很大的性能提升。事实上，在许多情况下，这足够了。你根本不需要使用多台机器。例如在单台机器上使用八个GPU，而不是在多台机器上使用16个GPU（由于多机器设置中网络通信带来的额外延时），可以同样快的训练神网。

这里我们将介绍如何设置你的环境，这样tf就能在一台机器上使用多个GPU卡。然后介绍怎么并行的对设备做分布操作和并行执行他们。

### 安装

为了在多个GPU卡上运行tf，首先要确认你的GPU卡是否具有NVIDIA Compute Capability（大于或等于3.0），这包括NVIDIA 的Titan，Titan X，K20,和K40卡（如果你有其他显卡，你可以在这里检查它https://developer.nvidia.com/cuda-gpus ）。

然后你必须下载和安装适当的CUDA版本和cuDNN库（CUDA8.0和cuDNN 5.1 如果是安装的tf版本是1.0.0）并设置一些环境变量这样tf知道去哪找CUDA和cuDNN。安装详情请看tf的官网。

NVIDIA的Compute Unifed Device Architecture 库（CUDA）运行开发者使用能用CUDA的GPU进行关于图形加速的所有类型的计算。NVIDIA的CUDA 深神网（cuDNN）是针对DNN的GPU加速基础库。它提供了常用DNN计算的优化实现，例如激活层，归一化，前向和反向卷积以及池化）。它是NVIDIA Deep Learning SDK 的一部分。tf使用CUDA和cuDNN来控制GPU卡并加速计算。
![1530512056.png](https://upload-images.jianshu.io/upload_images/3509189-aafd734d9b9d8b57.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


你可以用**nvidia-smi**命令检查CUDA是不是安装好了。它会列出可用的GPU卡。

最后你必须安装支持GPU的tf。

```shell
pip3 install --upgrade tensorflow-gpu
```

现在你可以打开python shell，通过import tf和创建一个session来检查是否使用CUDA和cuDNN。



## 管理GPU RAM

默认的，第一次运行一个图，tf自动占用所有可用GPU的所有RAM，这样你就不能在第一个在运行的时候，开始第二个tf程序。如果你这样做了，你会得到一个错误：

![1530512622.png](https://upload-images.jianshu.io/upload_images/3509189-f6ec9af492dbfde6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



一个办法是在另一个的GPU运行另一个程序。最简单的方法是设置CUDA_VISIBLE_DEVICES 环境变量，这样每个程序只看到对应的GPU卡。

```
$ CUDA_VISIBLE_DEVICES=0,1 python3 program_1.py
# and in another terminal:
$ CUDA_VISIBLE_DEVICES=3,2 python3 program_2.py
```

程序1只看到GPU 0 和 1，程序2只看到GPU 2 和 3，一切都会正常工作。

![1530513411.png](https://upload-images.jianshu.io/upload_images/3509189-0b39f85861b3448c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



另一个选择是告诉tf只用内存的一部分。比如让tf只用每个GPU40%的内存，你必须要创建一个ConfigProto 对象，设置它的**gpu_options.per_process_gpu_memory_fraction **为0.4，然后使用这个配置创建session：

```python
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.4
session = tf.Session(config = config)
```

现在两个程序可以在同一个GPU卡中并行执行（但不能允许3个，因为3x04.>1)
![1530513364.png](https://upload-images.jianshu.io/upload_images/3509189-b7bd3279cec00028.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


如果你允许**nvidia-smi**，你会看到2个程序都占用了接近40%的RAM。
![1530513544.png](https://upload-images.jianshu.io/upload_images/3509189-eb0da27a82c46b5e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



另一个选择是告诉tf需要多少才占用多少。为了这么做，你必须要设置**config.gpu_options.allow_growth  **为True。然而tf只要占用了就不会释放内存（为了避免内存碎片），所以过一段时间，你仍会耗尽内存。使用这选项可能难以确保确定性行为，因此你可能最好使用前几个选项。

## 在设备中放置操作

tf依赖于**simple placer**,它非常基础。

### 简单布置

不管什么时候运行一个图，如果tf需要评估一个还没放在设备上的节点，它使用简单的放置器将其放置在未放置的所有其他节点上。简单的放置器遵循以下规则：

- 如果某个节点已经放置在图的上一次运行中的某个设备上，则该节点保留在该设备上。
- 否则，如果用户将节点固定到设备（下面描述），则放置器将其放置在该设备上。
- 否则，它默认GPU #0，或者如果没有GPU，则CPU

正如你所看到的，放置在合适的设备的操作取决于你。如果你什么都不做，那么所有的节点都在默认的设备上。为了将节点固定到设备上，你必须使用**device()**方法创建一个设备块。比如，下面代码固定变量a和常量b到CPU，但多节点c没有固定到任何设备，所以它将会被放置到默认的设备上

```python
with tf.device("/cpu:0"):
    a = tf.Variable(3.0)
    b = tf.constant(4.0)
c = a * b
```

"/cpu:0" 聚集多CPU系统上的所有CPU。目前无法在特定CPU上固定节点或仅仅使用所有CPU的子集。

记录放置位置

我们检查下刚刚放置的限制。你可以设置log_device_placement 为True，这告诉placer当放置一个节点的时候打印log

```shell
>>> config = tf.ConfigProto()
>>> config.log_device_placement = True
>>> sess = tf.Session(config=config)
I [...] Creating TensorFlow device (/gpu:0) -> (device: 0, name: GRID K520,
pci bus id: 0000:00:03.0)
[...]
>>> x.initializer.run(session=sess)
I [...] a: /job:localhost/replica:0/task:0/cpu:0
I [...] a/read: /job:localhost/replica:0/task:0/cpu:0
I [...] mul: /job:localhost/replica:0/task:0/gpu:0
I [...] a/Assign: /job:localhost/replica:0/task:0/cpu:0
I [...] b: /job:localhost/replica:0/task:0/cpu:0
I [...] a/initial_value: /job:localhost/replica:0/task:0/cpu:0
>>> sess.run(c)
12
```

以I开头的表示Info。当我们创建一个session，tf打印log，告诉我们它发现一个GPU。然后第一次我们运行图（这里初始化变量a),简单放置器运行并放置每个节点到指定的设备上，上面可以看到a和b被放在了cpu，c被放在默认的gpu上。

### 动态放置方法

当你创建一个设备块，你可以指定一个方法而不是一个设备名。TensorFlow会调用这个函数来进行每个需要放置在设备模块中的操作，并且该函数必须返回设备的名称来固定操作。 例如，以下代码将所有变量节点固定为“/ cpu：0”（在本例中仅为变量a），将所有其他节点固定为“/ gpu：0”：

```python
def variables_on_cpu(op):
	if op.type == "Variable":
		return "/cpu:0"
	else:
		return "/gpu:0"
    
with tf.device(variables_on_cpu):
	a = tf.Variable(3.0)
    b = tf.constant(4.0)
	c = a * b
```

你可以简单的实现更复杂的算法，例如以循环方式在GPU之间固定变量。

### 操作和内核

对于在设备上运行的TensorFlow操作，它需要具有该设备的实现; 这被称为内核。 许多操作对于CPU和GPU都有内核，但并非全部都是。 例如，TensorFlow没有用于整数变量的GPU内核，因此当TensorFlow尝试将变量i放置到GPU＃0时，以下代码将失败：

```python
>>> with tf.device("/gpu:0"):
... i = tf.Variable(3)
[...]
>>> sess.run(i.initializer)
Traceback (most recent call last):
[...]
tensorflow.python.framework.errors.InvalidArgumentError: Cannot assign a device
to node 'Variable': Could not satisfy explicit device specification
```

 请注意，TensorFlow推断变量必须是int32类型，因为初始化值是一个整数。 如果将初始化值更改为3.0而不是3，或者如果在创建变量时显式设置dtype = tf.float32，则一切正常。

### 软放置

默认情况下，如果您尝试在操作没有内核的设备上固定操作，则当TensorFlow尝试将操作放置在设备上时，您会看到前面显示的异常。 如果您更喜欢TensorFlow回退到CPU，则可以将allow_soft_placement配置选项设置为True：

```python
with tf.device("/gpu:0"):
	i = tf.Variable(3)
    
config = tf.ConfigProto()
config.allow_soft_placement = True
sess = tf.Session(config=config)
sess.run(i.initializer) # the placer runs and falls back to /cpu:0
```

讲了那么多如何放置节点到不同的设备，现在讲tf如何并行运行这些节点。

## 并行执行

当tf运行一个图，它开始找需要被评估的节点列表，然后它计算他们的每个有多少依赖。tf然后开始计算0依赖的及诶单（source 节点）。如果这些节点被放置在不同的设备上，显然他们可以并行计算。如果他们在相同设备上，他们在不同的线程中计算，这样他们也在并行（在不同的GPU线程或者CPU核心）

tf对每个设备管理一个线程池来并行操作，这些叫**inter-op thread pools **，一些操作有多线程核：他们可以使用他们的线程池（每个设备一个）叫**intra-op  thread pools **。
![1530516431(1).png](https://upload-images.jianshu.io/upload_images/3509189-40013ea323cf8201.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


比如在上图，操作A,B和C是source ops所以他们能被马上计算。操作A和B放在GPU#0,所以他们被送到这个设备的inter-op thread pool，然后立即并行计算。操作A有一个多线程核，它的计算被划分成3部分，通过intra-op thread pool进行并行执行。操作C到GPU#1 的inter-op thread pool.

当操作C结束，操作D和E的依赖计数器递减，2个都达到0，所以这两个操作会被送到inter-op thread pool被执行。

可以控制每inter-op pool的数量，通过设置inter_op_parallelism_threads 。 请注意，开始的第一个session将创建内部线程池。 除非将use_per_session_threads选项设置为True，否则所有其他session都将重用它们。 可以通过设置intra_op_parallelism_threads选项来控制每个intra-op池的线程数。

## 控制依赖

有些情况下，即使所有依赖的操作都已执行，推迟操作评估也许是明智之举。 例如，如果它使用大量内存，但在图中只需要更多内存，则最好在最后一刻对其进行评估，以避免不必要地占用其他操作可能需要的RAM。 另一个例子是依赖位于设备外部的数据的一组操作。 如果它们全部同时运行，它们可能会使设备的通信带宽达到饱和，并最终导致所有等待I / O。 其他需要传递数据的操作也将被阻止。 顺序执行这些通信繁重的操作将是优选的，允许设备并行执行其他操作。

为了推迟一些节点的评估，一个简单的方法是添加**control dependencies**。比如下面代码告诉tf评估x和y在a和b被计算之后：

```python
a = tf.constant(1.0)
b = a + 2.0
with tf.control_dependencies([a, b]):
	x = tf.constant(3.0)
	y = tf.constant(4.0)
z = x + y
```

显然z依赖于x和y，计算z要等a和b被计算后，即使它没有明确地在control_dependencies（）块中。同样，由于b依赖于a，我们可以通过在[b]而不是[a，b]上创建控制依赖关系来简化前面的代码，但在某些情况下“ 显式比隐式更好。

碉堡了，现在你知道了：

- 如何在多个设备中放置操作
- 这些操作如何并发执行
- 如何创建控制依赖优化并行执行。
