# ubuntu下python2.7 编译





## 下载python2.7 源码

https://www.python.org/downloads/release/python-2715/



## 安装

```
./configure --prefix=/path/to/your/wish --enable-optimization

make

make install
```



加上软链

```
ln -s /path/to/your/wish/bin/python2.7 /usr/bin/python
```



done



##### 1.首先要安装一些必要的库

centos6.6的docker容器中是没有gcc库的，首先安装gcc库

```
yum install gcc
```

安装其他必要库,这些库要在编译python源码前安装，在后续安装pip的过程中因为缺失这些导致重新编python译源码n次，着实烦恼啊。

```
yum install zlib
yum install zlib-devel
yum install openssl
yum install openssl-devel
```

##### 2.下载python源码包及其他必要工具包

首先下载python源码包,官网下载地址 <https://www.python.org/downloads>

```
wget https://www.python.org/ftp/python/2.7.14/Python-2.7.14.tgz
```

解压到指定目录

```
tar -xzf Python-2.7.14.tgz
```

下载setuptool和pip（用来管理python依赖包）

```
 wget https://pypi.python.org/packages/41/5f/6da80400340fd48ba4ae1c673be4dc3821ac06cd9821ea60f9c7d32a009f/setuptools-38.4.0.zip#md5=3426bbf31662b4067dc79edc0fa21a2e
 
wget https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz#md5=35f01da33009719497f01a4ba69d63c9
```

##### 3.编译python源码

首先生成python安装路径,我这里将安装路径放在/usr/local下面

```
mkdir /usr/local/python2.7
```

进入解压的源码路径，运行下面命令生成Makefile

```
./configure --enable-optimizations --prefix=/usr/local/python2.7/
```

**--enable-optimizations** 为最优安装，建议使用这个参数。**--prefix** 声明安装路径

修改 Modules/Setup 文件,修改内容如下

```
     # Socket module helper for SSL support; you must comment out the other
    # socket line above, and possibly edit the SSL variable:
    #SSL=/usr/local/ssl
    _ssl _ssl.c \
            -DUSE_SSL -I$(SSL)/include -I$(SSL)/include/openssl \
            -L$(SSL)/lib -lssl -lcrypto
            
```

默认这块是注释的，放开注释即开。这块功能是开启SSL模块，不然会出现安装完毕后，提示找不到ssl模块的错误。

Makefile生后依次在当前路径执行编译和安装命令

```
make & make install
```

以上命令执行完毕，且无报错的情况下,我们将默认python换将切换至2.7，保险起见现将软链备份。

```
cd /usr/bin

mv python python.bak
```

建立新的软链

```
ln -s /usr/local/python2.7/bin/python2.7 /usr/bin/python
```

运行命令python -V,查看是否出现2.7的版本，出现即为安装成功。

##### 4.安装pip工具

首先进入setuptools的解目录，执行命令

```
python setup.py install
```

命令执行成功后，在进入pip-9.0.1的解压目录,执行命令

```
python setup.py install
```