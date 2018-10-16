https://blog.liyuans.com/archives/ngrok.html

# Ngrok: 使用 Ngrok 实现内网穿透

Jan 10,2017 in [教程](https://blog.liyuans.com/category/tutorial.html) read (7499) | 百度已收录 | Author: [Leonn](https://blog.liyuans.com/author/1/)

目录[背景](https://blog.liyuans.com/archives/ngrok.html#_label0)[NAT 穿透原理](https://blog.liyuans.com/archives/ngrok.html#_label1)[一个栗子](https://blog.liyuans.com/archives/ngrok.html#_label1_0)[Ngrok](https://blog.liyuans.com/archives/ngrok.html#_label2)[准备工作](https://blog.liyuans.com/archives/ngrok.html#_label2_0)[编译服务端](https://blog.liyuans.com/archives/ngrok.html#_label3)[服务端](https://blog.liyuans.com/archives/ngrok.html#_label4)[测试连接](https://blog.liyuans.com/archives/ngrok.html#_label4_0)[编译客户端](https://blog.liyuans.com/archives/ngrok.html#_label5)[客户端](https://blog.liyuans.com/archives/ngrok.html#_label6)[未完待续](https://blog.liyuans.com/archives/ngrok.html#_label7)[参考资料](https://blog.liyuans.com/archives/ngrok.html#_label8)



## 背景

- **很多时候，我们都有这样的需求**：需要将本地正在开发的服务暴露在公网上，也就是从外网直接访问我们本机上的服务。
- 正常情况下，这是办不到的，因为我们的本机并没有公网 IP，我们的本机处在内网当中。



## NAT 穿透原理

这里需要顺手提及一个知识：NAT 穿透。



### 一个栗子

我们的机器一般都在路由器的内网当中，IP 地址基本上都是`192.168.x.x`系列，我们并没有公网 IP，那么如何访问外网呢？

- 我们打开浏览器访问 Google，Google 与我们主机之间如何通信？
  假设我们主机 IP 为`192.168.0.100`，路由器 LAN IP 为`192.168.0.1`，WAN IP 为`211.22.145.234`（这是一个公网 IP），Google 服务器 IP 为`74.125.204.101`。
- 详细通信流程如下：
  - 主机构建 HTTP 请求数据包，目标 IP 为`74.125.204.101`，目标端口`80/443`，源 IP 为`192.168.0.100`，源端口随机生成，假定为`5000`。
  - 主机检查目标 IP 地址，发现不在一个网段，数据包丢给默认网关`192.168.0.1`。
  - 路由器 LAN 口收到数据包，构建 NAT 映射，随机生成端口，假定为`5500`，这样映射就是 :`5500 -> 192.168.0.100:5000`。WAN 口收到的数据包，如果目标端口是`5500`，则转发给内网 IP 为`192.168.0.100`的机器的`5000`端口。
  - 路由器修改数据包的源端口为`5500`，源 IP 地址为`211.22.145.234`，使用 WAN 口将数据包发送出去。
  - Google 服务器收到请求，构建响应 HTTP 数据包，目标 IP 地址`211.22.145.234`，目标端口为`5500`。
  - 路由器 WAN 口收到数据包，目标端口为`5500`，查询 NAT 表，发现对应的机器是`192.168.0.100:5000`，所以修改目标 IP 为`192.168.0.100`，目标端口为`5000`。并通过 LAN 口发送给主机。
  - 主机接收到数据包，完成这一次通信。

从上面可以看出，内网机器能够和外网通信，全靠拥有公网 IP 的路由器做交通枢纽。
路由器通过查询 NAT 表，来确定数据包该发送给内网哪台机器。
所以内网多台机器都可以通过这一台路由器和外网进行通信。这极大的节省了宝贵的公网 IP 资源。



## Ngrok

- 而 ngrok 就是利用以上原理实现了内网穿透的工具，只是稍有不同，交换的工具从路由器变成了我们具有固定 IP 的 VPS。
  当然原理没有大变，都是找一个公网服务器做中介。此处成为服务器 A。流程如下。

```
1. 本地内网主机和服务器A构建一条连接
2. 用户访问服务器A
3. 服务器A联系本地内网主机获取内容
4. 服务器A将获取到的内容发送给用户
5. 通过上面的流程，就实现了用户访问到了我们内网的内容。
```

- 那么帮助我们实现这个功能的程序就是 Ngrok 。通过在服务器上安装 Ngrok ，我们就可以和本地主机构建一条隧道。来让外网用户访问本地主机的内容。



### 准备工作

#### 安装依赖

- 注意 golang 需要 1.6 以上，否则不能编译客户端
- 下面是 1.7.3，其他的自己去官网下载，我使用的 Ubuntu 16，自带的即可

```
wget https://storage.googleapis.com/golang/go1.7.3.linux-amd64.tar.gz
tar -zxvf go1.7.3.linux-amd64.tar.gz -C /usr/local
```

#### 获取 ngrok 源码

```
git clone https://github.com/inconshreveable/ngrok.git ngrok
## 建议请使用下面的地址，修复了无法访问的包地址
git clone https://github.com/tutumcloud/ngrok.git ngrok
cd ngrok
```

#### 生成证书

- 生成并替换源码里默认的证书，**注意域名修改为你自己的**。
  （之后编译出来的服务端客户端会基于这个证书来加密通讯，保证了安全性）

```
NGROK_DOMAIN="liyuans.com"

openssl genrsa -out base.key 2048
openssl req -new -x509 -nodes -key base.key -days 10000 -subj "/CN=$NGROK_DOMAIN" -out base.pem
openssl genrsa -out server.key 2048
openssl req -new -key server.key -subj "/CN=$NGROK_DOMAIN" -out server.csr
openssl x509 -req -in server.csr -CA base.pem -CAkey base.key -CAcreateserial -days 10000 -out server.crt

cp base.pem assets/client/tls/ngrokroot.crt
```



## 编译服务端

```
sudo make release-server
```

- 如果一切正常，ngrok/bin 目录下应该有 ngrok、ngrokd 两个可执行文件。
  ngrokd 为服务器端使用的，ngrok 是 linux 客户端使用的



## 服务端

- 前面生成的 ngrokd 就是服务端程序了，指定证书、域名和端口启动它（证书就是前面生成的，注意修改域名）：

```
sudo ./bin/ngrokd -tlsKey=server.key -tlsCrt=server.crt -domain="liyuans.com" -httpAddr=":8081" -httpsAddr=":8082"
```

- 到这一步，ngrok 服务已经跑起来了，可以通过屏幕上显示的日志查看更多信息。
- httpAddr、httpsAddr 分别是 ngrok 用来转发 http、https 服务的端口，可以随意指定。
- ngrokd 还会开一个 4443 端口用来跟客户端通讯（可通过 -tunnelAddr=":xxx" 指定），如果你配置了 iptables 规则，需要放行这三个端口上的 TCP 协议。



### 测试连接

- 现在，通过 `http://liyuans.com:8081` 和 `https://blog.liyuans.com:8082` 就可以访问到 ngrok 提供的转发服务。
  为了使用方便，建议把域名泛解析到 VPS 上，这样能方便地使用不同子域转发不同的本地服务。
- 可以看到这样一行提示：`Tunnel liyuans.com:8081 not found`，这说明万事俱备，只差客户端来连了。



## 编译客户端

```
#windows
GOOS=windows GOARCH=amd64 make release-client
#mac
GOOS=darwin GOARCH=amd64 make release-client
```



## 客户端

- 如果要把 linux 上的服务映射出去，客户端就是前面生成的 ngrok 文件。（在 bin 文件夹内）
- 写一个简单的配置文件，随意命名如 ngrok.cfg：

```
server_addr: imququ.com:4443
trust_host_root_certs: false
```

- 指定子域、要转发的协议和端口，以及配置文件，运行客户端：

```
./ngrok -subdomain pub -proto=http -config=ngrok.cfg 80
```

- 不出意外可以看到这样的界面，这说明已经成功连上远端服务了