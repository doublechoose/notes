# chapter 2

1. look at the big picture
2. get the data
3. discover and visualize the data to gain insights
4. prepare the data for machine learning algorithms
5. select a model and train it
6. fine-tune your model
7. present your solution
8. launch, monitor, and maintain your system

## 总览

任务：构建一个房产价格模型，使用加州的普查数据。该数据包括了人口数，中间收入，中间房产价格，对于加州的每块区域，区域是美国普查局使用的地区最小单元（每个区域通常有600到3000的人口数）。简称区。

你的模型应该从数据中学习，并能通过给定其他值来预测每个区的中间房产价格。

## 解决问题

第一个要问你老板的问题是这个项目的目的是什么；构建一个模型可能不是最终目标。公司期望如何使用这个模型和从中获益？这很重要，因为它将决定你如何解决问题，选择哪种算法，用什么性能指标来评估你的模型以及要花多少努力来调整它。

你的老板说你的模型的输出（预测一个区的中间房价）将会和其他许多信号一起被喂给另一个机器学习系统。这个下游的系统会决定一个给定区域是否值得投资。做到这点十分重要，因为它直接的影响收入。

下一个问题是当前的解决方案是怎么样的（如果有的话）？它通常会给你一个参考指标，以及了解是如何解决问题的。你的老板说地区房价通常由专家人工估计：一个团队根据一个地区的最新信息（除了中间房价），并且使用复杂的规则来得出估计。这个很费钱并且时间开销大，并且他们的估计并不完美；通常错误率为15%。

好的，现在所有的信息，你都有了，开始设计你的系统吧。首先你需要解决问题：它是监督的、无监督的、或者强化学习？它是一个分类任务，一个回归任务，或者其他类型的？应该使用批量学习或者在线学习技术？在你读下去之前，暂停下，试着自己回答这些问题先。

找到答案了吗？ 我们一起来看看：它肯定是一个典型的监督学习任务，因为你有了一个带标签的训练例子（每个实例有一个期望的输出,比如区域的中间房价）。而且它也是一个典型的回归任务，因为要预测一个值。更确切的说，这是一个多变量回归问题，因为系统将会使用多个特征来做预测（它将会使用区域的人口数，中间收入等）。在第一章，你预测生活满意度只基于一个特征，人均GDP，所以它是一个单变量回归问题。最后，没有接连的数据流进入该系统，没必要快速调整数据，并且数据小到在内存中放的下，所以简单的批量学习就够了。

## 选择一个性能指标

下一步是选择一个性能指标。对于回归问题，一个典型的性能指标是根均方差（RMSE）。 它测量系统在其预测中所犯错误的标准偏差。例如，等于50,000的RMSE意味着系统预测的约68％落在实际值的50,000美元之内，并且约95％的预测落在实际值的100,000美元之内。



## 创建测试集

创建一个测试集理论上十分简单：只要随机的选一些实例，通常是数据集的20%，然后将他们放在一边：

```
import numpy as np
def split_train_test(data, test_ratio):
	shuffled_indices = np.random.permutation(len(data))
	test_set_size = int(len(data) * test_ratio)
	test_indices = shuffled_indices[:test_set_size]
	train_indices = shuffled_indices[test_set_size:]
	return data.iloc[train_indices], data.iloc[test_indices]
```

可以这样使用方法：

```
>>> train_set, test_set = split_train_test(housing, 0.2)
>>> print(len(train_set), "train +", len(test_set), "test")
16512 train + 4128 test
```

可以工作！但不完美，如果你再次运行程序，会生成一个不同的测试集！随着时间的推移，你的算法就会看到整个数据集，这是你要避免的（都看到了还怎么当测试集，这是作弊）。

一个解决方案是在第一次运行时保存测试集，然后在第二次运行时载入。另一个是设置随机数字生成器的种子（如np.random.seed(43))在调用np.random.permutation()前，这样它就会一直生成同样的片段。

但这些方案，在你拿到一个更新的数据集的时候，都会无效。一个常用方案是使用每个实例的识别符来决定要还是不要放进测试集（假设实例有一个唯一且不变的识别符）。比如你可以计算每个实例的识别符的hash，只保存hash最后的byte位，然后放测试集，如果这个值小于等于51（约256的20%）。这保证了测试集会保持一致，在多次的运行后。即使你更新了数据集。新的测试集将会保留新的实例的20%。但不会留有任何属于之前是训练集的实例。以下是实现：

```
import hashlib
def test_set_check(identifier, test_ratio, hash):
	return hash(np.int64(identifier)).digest()[-1] < 256 * test_ratio
def split_train_test_by_id(data, test_ratio, id_column, 	hash=hashlib.md5):
	ids = data[id_column]
	in_test_set = ids.apply(lambda id_: test_set_check(id_, 	test_ratio, hash))
	return data.loc[~in_test_set], data.loc[in_test_set]
```

但是，房价数据集没有一个id列，最简单的方式是使用行数作为id。

```
housing_with_id = housing.reset_index() # adds an `index` column
train_set, test_set = split_train_test_by_id(housing_with_id, 0.2, "index")
```

如果你使用行数作为一个唯一的id，必须保证新的数据被添加到数据集的尾部，并且没有行数被删除，否则可以用最稳定的特征来构建一个唯一的id。比如一个地区的经纬度在几百万年内是维持不变的，所以你可以结合他们到一个ID中如：

```
housing_with_id["id"] = housing["longitude"] * 1000 + housing["latitude"]
train_set, test_set = split_train_test_by_id(housing_with_id, 0.2, "id")
```





