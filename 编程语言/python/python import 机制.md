# python import 机制

- relative import

- absolute import

## relative import 

```
from . import sth0
from .swh1 import sth1
from ..swh2 import sth2
from ...swh3 import sth3
```

相对引用使用一个点号来标识引入库的，一个点表示一个当前目录，多一个则是上一个目录。

## absolute import

```
from swh2.swh1 import sth0
```

绝对引用通过package的绝对路径引入module，且路径要从最上一层的package写起。

注意：

#### 使用relative import的脚本不能直接启动，否则会报错Attempt relative import in non-package。

原因：相对引入使用被引入文件的`__name__`属性来决定该文件在整个包结构的位置，但是当python脚本被直接运行时，这个module的`__name__`就被设置`__main__`, 而不是module原来的name，这样相对路径就无法识别。



#### 即使使用了绝对引用，启动脚本也要放在和top-level package 同层级，如果放在top-level的package下，会报错：No module named xxx

原因：

1. python 通过import的模块搜索路径有：
   1. 程序主目录
   2. pythonpath目录
   3. 标准链接库目录
   4. .pth文件目录（指python运行用户把有效路径添加到模块搜索路径中）
2. 如果启动脚本放在src目录下：
   1. 程序主目录为src/,在这个目录没有src这个module
   2. pythonpath目录页不会有src这个module
   3. 标准链接库也不会搜到src这个module
3. 如果启动脚本放在src同级目录下：
   1. 程序主目录下即可搜索到src这个module，import 就不会报错。

