# 解决python3 UnicodeEncodeError: 'gbk' codec can't encode character '\xXX' in position XX

原因：print()函数自身有限制，不能完全打印所有的unicode字符。

```
import io
import sys
import urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
```



