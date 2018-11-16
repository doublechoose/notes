node 后台运行nodejs



使用forever

```
#安装
sudo npm install -g forever

#使用
forever start 脚本文件

forever list 查看所有forever运行的进程
forever stop uid 停止运行对应uid的进程
```



node 设置局域网可访问，启动的时候：

```
D:\QQPCmgr\mongo\bin\mongod --bind_ip 172.16.88.154 --dbpath D:\data\db 
```

