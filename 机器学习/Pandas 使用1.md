# Pandas 使用1

## 安装

```
# conda
conda install pandas
# pip
python3 -m pip install --upgrade pandas
```



## pandas 解决了什么问题？

Python长期以来一直非常适合数据整理和准备，但对于数据分析和建模则不那么重要。pandas填补了这一空白，使您能够在Python中执行整个数据分析工作流程，而无需切换到更像域特定的语言，如R.结合优秀的IPython工具包和其他库，在Python中进行数据分析的环境在性能，生产力和协作能力方面表现出色。

[十分钟pandas](https://pandas.pydata.org/pandas-docs/stable/10min.html)

读取txt文件

```python
import pandas as pd
data = pd.read_csv('a.us.txt',sep=",")
```

查看数据

```
# 前五个数据
df.head()
# 最后三个数据
df.tail(3)

# 展示该数据的统计摘要
df.describe()
# 转置
df.T
# 排序
df.sort_index(axis=1,ascending=False)
# 列名
df.sort_values(by='B')

```

```
import subprocess
out_bytes = subprocess.check_output(['netstat','-a'])
```

这段代码执行一个指定的命令并将执行结果以一个字节字符串的形式返回。 如果你需要文本形式返回，加一个解码步骤即可。例如：

```
out_text = out_bytes.decode('utf-8')
```

只要其中某几列：

```
df = data.loc[:,['Open','High','Low','Close','Volume']]
```

pandas中主要数据结构被实现为以下2类：

- DataFrame， 可以想象为一个关系型数据表格，其中包含多个行和已命名的列
- Series，  它是单一列，DataFrame 包含一个或多个Series，每个Series均有一个名称

创建Series的一种方法是构建Series对象，例如：

```python
pd.Series(['San Francisco','San Jose','Sacramento'])
```

您可以将映射 `string` 列名称的 `dict` 传递到它们各自的 `Series`，从而创建`DataFrame`对象。如果 `Series` 在长度上不一致，系统会用特殊的 [NA/NaN](http://pandas.pydata.org/pandas-docs/stable/missing_data.html) 值填充缺失的值。例如：

```
city_names = pd.Series(['San Francisco', 'San Jose', 'Sacramento'])
population = pd.Series([852469, 1015785, 485199])

pd.DataFrame({ 'City name': city_names, 'Population': population })
```

### np.random.permutation(len(data))

随机的排列一个序列，或者返回一个已排好的排列

```
>>> np.random.permutation(10)
array([1, 7, 4, 3, 0, 9, 2, 5, 8, 6])

>>> np.random.permutation([1, 4, 9, 12, 15])
array([15,  1,  9,  4, 12])
```

reset_index()

```
添加一个index列
housing_with_id = housing.reset_index() # adds an `index` column
```

Scikit-Learn   提供了一些将数据集变为多个子数据集的方法，最简单的方法是`train_test_split`

### object creation

通过传入一个list值，创建一个Series

```
s = pd.Series([1,3,5,np.nan,6,8])

```

通过传入一个NumPy数组和datetime index和标签列，创建一个DataFrame

```
dates = pd.date_range('20130101',periods=6)
dates
```

