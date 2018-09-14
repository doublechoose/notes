### @property

装饰器可以给函数动态加上功能，内置的@property负责将一个方法变成属性调用：

```
class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
```

把一个getter变成属性，只需要加上@property就可以了。

### \_\_init\_\_.py 作用

将文件夹变为一个python模块，每个模块的包中都有一个\_\_init\_\.py文件。通常为空，但可以增加其他功能。在导入一个包时，实际上是导入它的init.py 文件。

**kwargs 类型为字典

`kwargs.pop('cls', self.__class__)`

表示如果没有key为cls的，则返回当前的类。

### getattr() 函数

用于返回一个对象属性值

### @classmethod

使用该方法修饰的方法是类专属的，并且可以通过类名进行调用。

###  BytesIO StringIO

数据读写不一定是文件，也可以在内存中读写。

StringIO操作的只能是str，如果要操作二进制数据，就需要用BytesIO。

'P','RGBA','RGB'这是PIL Image读图可能出现的3种mode，每种mode的图片数据都有不同的组织形式，当训练、测试数据都是一堆图片的时，就要留神了。

要转为同一种模式。

