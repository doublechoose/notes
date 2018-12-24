# zipline 架构分析

```
from __future__ import print_function
```

该句是python2的概念，在python2的环境下使用python3的print函数

zipline命令行

首先从`setup.py`中可以看到代码的entry_point

```python
entry_points={
    'console_scripts': [
        'zipline = zipline.__main__:main',
    ],
    ....
}
```

```python
if bundle.startswith('.'):
    continue
```

# 装饰器

本质上是一个Python函数或类

可以让其他函数或类在不做任何代码修改的前提下增加额外功能。

