# 设置scrapyd为系统后台服务及系统启动项

whereis scrapyd

## 一、设置为系统后台服务

### 1、新建文件/etc/init.d/scrapyd
```
vi /etc/init.d/scrapyd
sudo chmod 755 /etc/init.d/scrapyd
```
bash
```
#!/bin/bash
# chkconfig: 2345 20 80
# description: Srapyd
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