# ubuntu node 安装

修改为可执行文件

```
chmod +x xxx.sh
```

手动删除，仍未全删除掉

使用：

```
#apt-get 卸载
sudo apt-get remove --purge npm
sudo apt-get remove --purge nodejs
sudo apt-get remove --purge nodejs-legacy
sudo apt-get autoremove

#手动删除 npm 相关目录
rm -r /usr/local/bin/npm
rm -r /usr/local/lib/node-moudels
find / -name npm
rm -r /tmp/npm* 
```

升级

```
sudo npm install n -g


```

