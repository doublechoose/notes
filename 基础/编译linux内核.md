# 编译linux内核

ubuntu 虚拟机下编译linux内核



## .config

复制当前系统编译的配置，在/usr/src目录下

```
$ ls /usr/src/
linux-headers-4.15.0-30-generic 等
```

其中，在linux-headers-4.15.0-30-generic目录下存在.config文件，复制到要编译的源码下

```
linux-stable$ cp /usr/src/linux-headers-4.15.0-30-generic/.config .
```



## 编译配置

可能出现的问题

```
*** Unable to find the ncurses libraries or the
 *** required header files.
 *** 'make menuconfig' requires the ncurses libraries.
 *** 
 *** Install ncurses (ncurses-devel) and try again.
 *** 
scripts/kconfig/Makefile:202: recipe for target 'scripts/kconfig/dochecklxdialog' failed
make[1]: *** [scripts/kconfig/dochecklxdialog] Error 1
Makefile:543: recipe for target 'menuconfig' failed
make: *** [menuconfig] Error 2
```

提示缺少ncurse相关的库，安装

```
sudo apt-get install libncurses5-dev
```

安装好之后，重新执行，选择[load]–>[OK]–>[Save]–>[OK]–>[EXIT]–>[EXIT]

## 编译内核

执行 make

```
$ make
```

编译模块

```
make modules -j256
```

## 安装内核

```
//先安装模块
root$ make modules_install

//再安装内核
root$ make install
```

 更改启动grub

grub就是管理Ubuntu系统启动的一个程序，我们编译好的内核要设置为缺省运行项，修改对应的grub，其实也很简单。 
查看当前版本：

```
$ cat /proc/version  
Linux version 4.10.0-35-generic (buildd@lcy01-33) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.4) ) #39~16.04.1-Ubuntu SMP Wed Sep 13 09:02:42 UTC 2017

或者
$ uname -r

```

