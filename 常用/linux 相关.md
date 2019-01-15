# linux 相关

查看某服务状态

```bash
systemctl status elasticsearch.service
```

添加新用户
在root下，
```
adduser es
```
更改用户密码
```
passwd es
```

授权
```
sudoers
```
未找到命令
```
whereis sudoers
```

找到这个文件位置后再查看权限：
```
ls -l /etc/sudoers
```
只有只读权限，如果要修改需要添加w权限
```
chmod -v u+w /etc/sudoers
```

vim /etc/sudoers

```
## Allow root to run any commands anywher  
root    ALL=(ALL)       ALL  
es  ALL=(ALL)       ALL  #这个是新增的用户
```

wq退出
收回写权限
chmod -v u-w /etc/sudoers


No such file or directory: 'xdg-open': 'xdg-open'

```
yum install xdg-utils
```