python 字符串string开头r，b，u，f含义



```
b'abcd\n' # bytes字节符
r'abcd\n' # 非转义原生字符，经处理‘\n’变成'\\'和'n' 

u'abcd\n' # unicode编码字符，Python3默认unicode

a=2
f'{a}bcd\n' # 以f开头表示在字符串内支持大括号内的python 表达式
# 此时为2bcd\n
```





PUT  和 PATCH

PUT ： 替换一个存在的资源

PATCH：对一个存在的资源进行局部修改

