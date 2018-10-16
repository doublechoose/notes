# 设置scrapyd为系统后台服务及系统启动项

whereis scrapyd

## 一、设置为系统后台服务

### 1、新建文件/etc/init.d/scrapyd

修改使用权限为可读可执行
```
vi /etc/init.d/scrapyd
sudo chmod 755 /etc/init.d/scrapyd
```

bash

```
#!/bin/bash

PORT=6800
HOME="/var/scrapyd"
BIN="/usr/bin/scrapyd"
 
pid=`netstat -lnopt | grep :$PORT | awk '/python/{gsub(/\/python/,"",$7);print $7;}'`
start() {
   if [ -n "$pid" ]; then
      echo "server already start,pid:$pid"
      return 0
   fi
 
   cd $HOME
   nohup $BIN >> $HOME/scrapyd.log 2>&1 &
   echo "start at port:$PORT"
}
 
stop() {
   if [ -z "$pid" ]; then
      echo "not find program on port:$PORT"
      return 0
   fi
 
   #结束程序，使用讯号2，如果不行可以尝试讯号9强制结束
   kill -9 $pid
   echo "kill program use signal 9,pid:$pid"
}
 
status() {
   if [ -z "$pid" ]; then
      echo "not find program on port:$PORT"
   else
      echo "program is running,pid:$pid"
   fi
}
 
case $1 in
   start)
      start
   ;;
   stop)
      stop
   ;;
   status)
      status
   ;;
   *)
      echo "Usage: {start|stop|status}"
   ;;
esac
 
exit 0

```

### 2、新建目录/var/scrapyd

mkdir /var/scrapyd

### 3、命令操作（启动停止状态）
service scrapyd {start|stop|status}

## 二、设置为系统启动项

启用禁用命令：sysv-rc-conf scrapyd on/off
sysv-rc-conf scrapyd on
或者chkconfig --add/del scrapyd
chkconfig --add scrapyd
chkconfig --del scrapyd
chkconfig --list

## 三、远程访问

默认scrapyd启动bind绑定的ip地址是127.0.0.1端口是：6800，这里为了其他主机可以访问，需将ip地址设置为0.0.0.0

vi /usr/lib/python2.7/site-packages/scrapyd/default_scrapyd.conf

bind_address = 0.0.0.0


知识点：
在linux输入 `ll`,可以看到
`-rwx-r--r--(一共10个参数)表示文件所属组合用户的对应权限
第一个参数表示文件或文件夹
d 表示文件夹
\- 表示文件

2-4参数属于user
5-7参数属于group
8-10属于other

r ==> 可读
w ==> 可写
x ==> 可执行

r = 4
w = 2
x = 1

7 = 4+2+1
5 = 4+1
755表示rwxr-xr-x

777表示rwxrwxrwx 所有用户可读可写可执行

netstat -lnopt | grep :$PORT
netstat 是一个监听TCP/IP网络的非常有用的工具，可以显示路由表，实际的网络连接
以及每个网络接口设备的状态信息。


netstat -lnopt

```
-l 只显示监听端口
-n don't resolve names 不分析名？
-o 显示计时器
-p 显示正在使用Socket的程序识别码和程序名称
-t 显示TCP传输协议的连线状况；
```

grep 文本搜索工具，能用正则表达式搜索文本，并把匹配的行打印出来。
全称global regular expression print

awk 行处理器，通常用来格式化文本信息，依次对每一行进行处理，然后输出

awk '/python/{gsub(/\/python/,"",$7);print $7;}' 
对netstat 得到的行进行处理

```shell
echo "tcp        0      0 172.16.89.145:6800      0.0.0.0:*               LISTEN      3833/python3.6       off (0.00/0/0)" | awk '/python3.6/{gsub(/\/python3.6/,"",$7);print $7;}'

```
返回3833


if  [ -n $string  ]             如果string 非空(非0），返回0(true)  
if  [ -z $string  ]             如果string 为空

nohup 不挂断的运行命令

nohup $BIN >> $HOME/scrapyd.log 2>&1 &

& 在后台运行

2>&1

对于& 1 更准确的说应该是文件描述符 1,而1标识标准输出，stdout。
对于2 ，表示标准错误，stderr。
2>&1 的意思就是将标准错误重定向到标准输出。这里标准输出已经重定向到了 /dev/null。那么标准错误也会输出到/dev/null

可以把/dev/null 可以看作"黑洞". 它等价于一个只写文件. 所有写入它的内容都会永远丢失. 而尝试从它那儿读取内容则什么也读不到.

偶尔也可以把 & 在命令的最后加上，表示让程序后台执行。

为何2>&1要写在后面？

index.php task testOne >/dev/null 2>&1
我们可以理解为，左边是标准输出，好，现在标准输出直接输入到 /dev/null 中，而2>&1是将标准错误重定向到标准输出，所以当程序产生错误的时候，相当于错误流向左边，而左边依旧是输入到/dev/null中。

可以理解为，如果写在中间，那会把隔断标准输出指定输出的文件

你可以用

ls 2>1测试一下，不会报没有2文件的错误，但会输出一个空的文件1；
ls xxx 2>1测试，没有xxx这个文件的错误输出到了1中；
ls xxx 2>&1测试，不会生成1这个文件了，不过错误跑到标准输出了；
ls xxx >out.txt 2>&1, 实际上可换成 ls xxx 1>out.txt 2>&1；重定向符号>默认是1,错误和输出都传到out.txt了。

kill -9 $pid
发送SIGKILL信号给进程，告诉进程，你被终结了，请立刻退出。
9 表示这个信号不能被捕获或忽略(强制终止)

case $1 in



sudo service scrapyd {start|stop|status}

$1 = start|stop|status

case ... esac 与其他语言中的 switch ... case 语句类似，是一种多分枝选择结构。