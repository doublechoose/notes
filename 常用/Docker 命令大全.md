# Docker 命令大全

[TOC]

## 容器生命周期管理

### run

**docker run ：**创建一个新的容器并运行一个命令

```
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

OPTIONS说明：

- **-a stdin:** 指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项；
- **-d:** 后台运行容器，并返回容器ID；
- **-i:** 以交互模式运行容器，通常与 -t 同时使用；
- **-p:** 端口映射，格式为：主机(宿主)端口:容器端口
- **-t:** 为容器重新分配一个伪输入终端，通常与 -i 同时使用；
- **--name="nginx-lb":** 为容器指定一个名称；
- **--dns 8.8.8.8:** 指定容器使用的DNS服务器，默认和宿主一致；
- **--dns-search example.com:** 指定容器DNS搜索域名，默认和宿主一致；
- **-h "mars":** 指定容器的hostname；
- **-e username="ritchie":** 设置环境变量；
- **--env-file=[]:** 从指定文件读入环境变量；
- **--cpuset="0-2" or --cpuset="0,1,2":** 绑定容器到指定CPU运行；
- **-m :**设置容器使用内存最大值；
- **--net="bridge":** 指定容器的网络连接类型，支持 bridge/host/none/container: 四种类型；
- **--link=[]:** 添加链接到另一个容器；
- **--expose=[]:** 开放一个端口或一组端口；

###start/stop/restart

**docker start** :启动一个或多个已经被停止的容器

**docker stop** :停止一个运行中的容器

**docker restart** :重启容器

语法

```
docker start [OPTIONS] CONTAINER [CONTAINER...]
docker stop [OPTIONS] CONTAINER [CONTAINER...]
docker restart [OPTIONS] CONTAINER [CONTAINER...]
```

### kill

**docker kill** :杀掉一个运行中的容器。

语法

```
docker kill [OPTIONS] CONTAINER [CONTAINER...]
```

OPTIONS说明：

- **-s :**向容器发送一个信号

实例

杀掉运行中的容器mynginx

```
$ docker kill -s KILL mynginx
mynginx
```

### rm

**docker rm ：**删除一个或多少容器

语法

```
docker rm [OPTIONS] CONTAINER [CONTAINER...]
```

OPTIONS说明：

- **-f :**通过SIGKILL信号强制删除一个运行中的容器
- **-l :**移除容器间的网络连接，而非容器本身
- **-v :**-v 删除与容器关联的卷

实例

强制删除容器db01、db02

```
docker rm -f db01 db02
```

移除容器nginx01对容器db01的连接，连接名db

```
docker rm -l db 
```

删除容器nginx01,并删除容器挂载的数据卷

```
docker rm -v nginx01
```

### pause/unpause

**docker pause** :暂停容器中所有的进程。

**docker unpause** :恢复容器中所有的进程。

语法

```
docker pause [OPTIONS] CONTAINER [CONTAINER...]
docker unpause [OPTIONS] CONTAINER [CONTAINER...]
```

实例

暂停数据库容器db01提供服务。

```
docker pause db01
```

恢复数据库容器db01提供服务。

```
docker unpause db01
```

### create

**docker create ：**创建一个新的容器但不启动它

语法

```
docker create [OPTIONS] IMAGE [COMMAND] [ARG...]
```

实例

使用docker镜像nginx:latest创建一个容器,并将容器命名为myrunoob

```
runoob@runoob:~$ docker create  --name myrunoob  nginx:latest      
09b93464c2f75b7b69f83d56a9cfc23ceb50a48a9db7652ee4c27e3e2cb1961f
```

### exec

**docker exec ：**在运行的容器中执行命令

语法

```
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

OPTIONS说明：

- **-d :**分离模式: 在后台运行
- **-i :**即使没有附加也保持STDIN 打开
- **-t :**分配一个伪终端

实例

在容器mynginx中以交互模式执行容器内/root/runxxx.sh脚本



```
$ docker exec -it mynginx /bin/sh /root/runxxx.sh
```

在容器mynginx中开启一个交互模式的终端

```
$ docker exec -i -t  mynginx /bin/bash
root@b1a0703e41e7:/#
```

## 容器操作

### ps

**docker ps :** 列出容器

语法

```
docker ps [OPTIONS]
```

OPTIONS说明：

- **-a :**显示所有的容器，包括未运行的。

- **-f :**根据条件过滤显示的内容。

- **--format :**指定返回值的模板文件。

- **-l :**显示最近创建的容器。

- **-n :**列出最近创建的n个容器。

- **--no-trunc :**不截断输出。

- **-q :**静默模式，只显示容器编号。

- **-s :**显示总的文件大小。



### inspect

**docker inspect :** 获取容器/镜像的元数据。

语法

```
docker inspect [OPTIONS] NAME|ID [NAME|ID...]
```

OPTIONS说明：

- **-f :**指定返回值的模板文件。
- **-s :**显示总的文件大小。
- **--type :**为指定类型返回JSON。

实例

获取镜像mysql:5.6的元信息。

```
$ docker inspect mysql:5.6
```

### top

**docker top :**查看容器中运行的进程信息，支持 ps 命令参数。

语法

```
docker top [OPTIONS] CONTAINER [ps OPTIONS]
```

容器运行时不一定有/bin/bash终端来交互执行top命令，而且容器还不一定有top命令，可以使用docker top来实现查看container中正在运行的进程。

实例

查看容器mymysql的进程信息。

```
$ docker top mymysql
```

### attach

**docker attach :**连接到正在运行中的容器。

语法

```
docker attach [OPTIONS] CONTAINER
```

要attach上去的容器必须正在运行，可以同时连接上同一个container来共享屏幕（与screen命令的attach类似）。

官方文档中说attach后可以通过CTRL-C来detach，但实际上经过我的测试，如果container当前在运行bash，CTRL-C自然是当前行的输入，没有退出；如果container当前正在前台运行进程，如输出nginx的access.log日志，CTRL-C不仅会导致退出容器，而且还stop了。这不是我们想要的，detach的意思按理应该是脱离容器终端，但容器依然运行。好在attach是可以带上--sig-proxy=false来确保CTRL-D或CTRL-C不会关闭容器。

实例

容器mynginx将访问日志指到标准输出，连接到容器查看访问信息。

```
$ docker attach --sig-proxy=false mynginx
```

### events

**docker events :** 从服务器获取实时事件

语法

```
docker events [OPTIONS]
```

OPTIONS说明：

- **-f ：**根据条件过滤事件；
- **--since ：**从指定的时间戳后显示所有事件;
- **--until ：**流水时间显示到指定的时间为止；

实例

显示docker 2016年7月1日后的所有事件。

```
runoob@runoob:~/mysql$ docker events  --since="1467302400"
```

### logs

**docker logs :** 获取容器的日志

语法

```
docker logs [OPTIONS] CONTAINER
```

OPTIONS说明：

- **-f :** 跟踪日志输出
- **--since :**显示某个开始时间的所有日志
- **-t :** 显示时间戳
- **--tail :**仅列出最新N条容器日志

实例

跟踪查看容器mynginx的日志输出。

```
runoob@runoob:~$ docker logs -f mynginx
```

### wait

**docker wait :** 阻塞运行直到容器停止，然后打印出它的退出代码。

语法

```
docker wait [OPTIONS] CONTAINER [CONTAINER...]
```

实例

```
docker wait CONTAINER
```

### export

**docker export :**将文件系统作为一个tar归档文件导出到STDOUT。

语法

```
docker export [OPTIONS] CONTAINER
```

OPTIONS说明：

- **-o :**将输入内容写到文件。

实例

将id为a404c6c174a2的容器按日期保存为tar文件。

```
runoob@runoob:~$ docker export -o mysql-`date +%Y%m%d`.tar a404c6c174a2
```

### port

**docker port :**列出指定的容器的端口映射，或者查找将PRIVATE_PORT NAT到面向公众的端口。

```
docker port [OPTIONS] CONTAINER [PRIVATE_PORT[/PROTO]]
```

查看容器mynginx的端口映射情况。

```
$ docker port mymysql
```

待续。。。

### 容器rootfs命令

- [commit](http://www.runoob.com/docker/docker-commit-command.html)
- [cp](http://www.runoob.com/docker/docker-cp-command.html)
- [diff](http://www.runoob.com/docker/docker-diff-command.html)

### 镜像仓库

- [login](http://www.runoob.com/docker/docker-login-command.html)
- [pull](http://www.runoob.com/docker/docker-pull-command.html)
- [push](http://www.runoob.com/docker/docker-push-command.html)
- [search](http://www.runoob.com/docker/docker-search-command.html)

### 本地镜像管理

- [images](http://www.runoob.com/docker/docker-images-command.html)
- [rmi](http://www.runoob.com/docker/docker-rmi-command.html)
- [tag](http://www.runoob.com/docker/docker-tag-command.html)
- [build](http://www.runoob.com/docker/docker-build-command.html)
- [history](http://www.runoob.com/docker/docker-history-command.html)
- [save](http://www.runoob.com/docker/docker-save-command.html)
- [import](http://www.runoob.com/docker/docker-import-command.html)

### info|version

- [info](http://www.runoob.com/docker/docker-info-command.html)
- [version](http://www.runoob.com/docker/docker-version-command.html)

