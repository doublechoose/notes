打开jupyter

```
jupyter notebook
```

Scikit-Learn 设计原则

- 一致性 所有对象共享一个一致且简答的接口：
  - Estimators 。任何对象可以基于一个数据集评估一些参数的叫estimator（如一个imputer就是一个estimator）。评估本身是通过fit()方法执行，并且它只用一个数据集作为一个参数（或者对于监督式学习是2个参数，第二个参数包含标签）。任何其他参数需要指导估计执行过程的被叫做一个超参数（如imputer的策略），并且它必须设置作为一个实例变量（通常经由一个构造参数）
  - Transformers。一些estimator（如imputer）也能转换数据集；这些叫transformers.再一次，API相当简单：转换通过方法transform()执行和带入要进行转换的数据集作为参数。这个转换通常依赖学习参数。所有transformer都有一个简便方法叫fit_transform().等价于先调用fit()方法，然后再调用transform()（但有时候fit_transform()是优化过的运行更快）。
  - Predictors. 最后，一些estimators能对给定数据集进行预测。他们被称为predictor。比如，上一章LinearRegression模型是一个predictor：它预测生活满意度，对于给定的人均GDP。一个predictor有个predict()方法，带入一个数据集的新实例，并返回一个数据集对应的预测，它也有一个score()方法，用于在测试集中进行测量预测质量（以及在监督学习算法的情况下的相应标签）。
- Inspection （检查）.所有的estimator的超参数可以通过公共实例变量直接访问（如 imputer.strategy),并且所有的estimator的学习参数也能由公共变量使用带下横线进行访问（如imput.statistics_).
- Nonproliferation of class（防止类的扩散）。数据集用NumPy数组或者SciPy稀疏矩阵表示，而不是自定义的类。超参数只是普通的Python strings 或者 数字。
- Composition。存在构建块会尽可能的复用。比如，正如我们将要看到的，很容易从任意变换器序列创建一个Pipeline估算器，然后是最终估算器。
- Sensible defaults.Scikit-learn 为大多数参数提供合理的默认值，更容易快速创建一个基本能工作的系统。

## 处理文本和类别属性

之前我们遗漏了分类属性ocean_proximity，因为它是一个文本属性，所以我们无法计算它的中位数。大多数机器学习算法偏爱和数字打交道，让我们将这些文本标签转为数字吧。

Scikit-Learn为这个任务提供了一个转换器，叫LabelEncoder：

```python
>>> from sklearn.preprocessing import LabelEncoder
>>> encoder = LabelEncoder()
>>> housing_cat = housing["ocean_proximity"]
>>> housing_cat_encoded = encoder.fit_transform(housing_cat)
>>> housing_cat_encoded
array([1,4,...,1,0,3])
```

现在好多了：我们可以在任何ML算法中使用数字型数据。你可以看下这个编码器使用classes_ 属性的映射（“<1H OCEAN"映射为0，”INLAND“映射为1 等）：

```python
>>>print(encoder.classes_)
['<1H OCEAN' 'INLAND' 'ISLAND' 'NEAR BAY' 'NEAR OCEAN']
```

这里有个问题，ML会假设两个相邻值比远离值来的相似。显然这不是那种情况（比如类别0和4比0和1更相近）。为了解决这个问题，一个常用方法是为每个类别创建一个二元属性：当类别是“<1H OCEAN"，设置属性等于1（和0），当类别为”INLAND“设置属性为1.以此类推。这个叫one-hot 编码。因为只有一个属性会等于1.其他的都为0.

