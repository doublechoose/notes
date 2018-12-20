# Python 源码剖析 python对象

## 对象机制的基石 ---- PyObject

在python中，所有的东西都是对象，而所有的对象都拥有一些相同的内容，这些内容在PyObject中定义，PyObject是整个Python对象机制的核心。

`object.h`

