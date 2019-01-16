# 打包、上传至自己的pypiserver 



## pypiserver安装和使用

https://pypi.org/project/pypiserver/#quickstart-installation-and-usage

```
pip install pypiserver
mkdir ~/packages  
```



### 启动

```
pypi-server -p 8080 packages &  
```



### 打包

tree：

yourlib

​    `setup.py`

​    dirname

​         `__init__.py`    

​         module

```
#setup.py
from setuptools import setup, find_packages

# 注意，这个name需要和top-level的目录名一致，否则代码无法打包
setup(
    name = "wsdk",
    version = "1.0",
    py_modules=[''],
    install_requires=['requests', 'zipline>=1.3.0',
                      'pyyaml', 'pymysql', 'cn-stock-holidays'],
)
```



#### 查看setup.py 的命令

```
python setup.py --help-commands

```

create a "egg" distribution

```
python setup.py bdist_egg

#whl文件 可以放在pypiserver上下载
wheel
python setup.py bdist_wheel
```

上传到pypiserver的为whl包，这样才能用pip下载安装，上传为egg的，会出现

```
could not find a version that satisfies the requirement xxx...
```



### upload 

```
twine upload --repository-url http://172.16.89.145:9010 dist/*
```

### 安装自己打的包

```
pip install  --extra-index-url http://172.16.89.145:9010/simple/ aiutils --trusted-host 172.16.89.145

or

pip install ai-util -i http://172.16.89.145:9010/simple/  --trusted-host 172.16.89.145

# -i 表示base url of python package index（default https://pypi.org/simple

加 --upgrade 可以升级包
```

