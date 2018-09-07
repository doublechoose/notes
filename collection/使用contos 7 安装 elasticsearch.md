使用contos 7 安装 elasticsearch

下载elasticsearch rpm（*RPM是*Red-Hat Package Manager）

```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.4.0.rpm
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.4.0.rpm.sha512
# 校验安装包的sha
shasum -a 512 -c elasticsearch-6.4.0.rpm.sha512 
sudo rpm --install elasticsearch-6.4.0.rpm
```

shasum 是在perl-Digest-SHA中，安装shasum命令：

```
yum install -y perl-Digest-SHA
```

elasticsearch 启动和停止

```
sudo systemctl start elasticsearch.service
sudo systemctl stop elasticsearch.service
```

elasticsearch 配置外网访问

```
cd /etc/elasticsearch
修改elasticsearch.yml 里
network.host: 0.0.0.0
端口号： 9200
```



vi 使用

| 快捷键     | 作用    |
| ------- | ----- |
| ：wq     | 保存并退出 |
| i       | 插入编辑  |
| esc     | 退出编辑  |
| ：q（！可选） | 不保存退出 |

kibana 使用service 启动
```
sudo -i service kibana start
sudo -i service kibana stop
```
kibana 使用systemd启动

```
sudo systemctl start kibana.service
sudo systemctl stop kibana.service
```

kibana 配置外网可见

```
cd /etc/kibana
修改 kibana.yml的
server.host: 0.0.0.0
```

Centos7 普通用户加入sudo组

1. 首先切换到root

2. visudo

   这个和vi的用法一样，移动光标，到最后一行，按a，进入append模式，输入以下这行内容(同理，cd到/etc/sudoers目录下,由于sudoers文件为只读权限，所以需要添加写入权限，chmod u+w sudoers 。vim sudoers )
   找到root ALL = (ALL) ALL这一行，在下一行加入username ALL = (ALL) ALL。username指代你想加入sudo组的用户名。 
   把sudoers文件的权限修改回来。chmod u-w sudoers 
   这样普通用户可以执行sudo命令了。
   ps:这里说下你可以sudoers添加下面四行中任意一条 
   youuser ALL=(ALL) ALL 
   %youuser ALL=(ALL) ALL 
   youuser ALL=(ALL) NOPASSWD: ALL 
   %youuser ALL=(ALL) NOPASSWD: ALL

   第一行:允许用户youuser执行sudo命令(需要输入密码). 
   第二行:允许用户组youuser里面的用户执行sudo命令(需要输入密码). 
   第三行:允许用户youuser执行sudo命令,并且在执行的时候不输入密码. 
   第四行:允许用户组youuser里面的用户执行sudo命令,并且在执行的时候不输入密码.
   3、测试 sudo
   测试以上是否正确配置了 sudo ,只需要在普通用户权限下输入
   $ sudo whoami
   如果配置正确,则命令会返回“root”字样。

安装ik中文分词插件

下载ik中文分词：

https://github.com/medcl/elasticsearch-analysis-ik/releases

```
wget zip
```

放到/usr/share/elasticsearch/plugins/ik

ik为自己创建的文件夹中

解压 unzip



