# 部署 scrapy

### 安装scrapyd

```bash
sudo pip install scrapyd

#客户端安装
sudo pip install scrapyd-client
```

### windows下无法运行scrapyd-deploy问题：

在python/Scripts目录下，创建

scrapyd-deploy.bat

```bash
# scrapyd-deploy.bat 文件中输入以下内容：
@echo off
D:\Python36\python D:\Python36\Scripts\scrapyd-deploy %*
```

其中python 和scrapyd-deploy路径根据安装或者虚拟环境的实际情况而定

### scrapyd配置文件：

在/etc/scrapyd/scrapyd.conf 配置

如果没有，则创建之。

```
[scrapyd]
eggs_dir    = eggs
logs_dir    = logs
items_dir   =
jobs_to_keep = 5
dbs_dir     = dbs
max_proc    = 0
max_proc_per_cpu = 4
finished_to_keep = 100
poll_interval = 5.0
bind_address = 127.0.0.1
http_port   = 6800
debug       = off
runner      = scrapyd.runner
application = scrapyd.app.application
launcher    = scrapyd.launcher.Launcher
webroot     = scrapyd.website.Root

[services]
schedule.json     = scrapyd.webservice.Schedule
cancel.json       = scrapyd.webservice.Cancel
addversion.json   = scrapyd.webservice.AddVersion
listprojects.json = scrapyd.webservice.ListProjects
listversions.json = scrapyd.webservice.ListVersions
listspiders.json  = scrapyd.webservice.ListSpiders
delproject.json   = scrapyd.webservice.DeleteProject
delversion.json   = scrapyd.webservice.DeleteVersion
listjobs.json     = scrapyd.webservice.ListJobs
daemonstatus.json = scrapyd.webservice.DaemonStatus
```

配置具体内容：https://scrapyd.readthedocs.io/en/stable/config.html

如果要能被访问，设置bind_address为具体ip。

使用`scrapyd`启动



### 部署写的爬虫到scrapyd

在爬虫项目的根目录下（可以看到scrapy.cfg文件的目录），修改scrapy.cfg:

```
# 将 url = xxx 的注释#拿掉
# url = http://127.0.0.1:6800/
```

在根目录下执行

```
scrapyd-deploy
```

启动爬虫命令

```
curl http://localhost:6800/schedule.json -d project=PROJECT_NAME -d spider=SPIDER_NAME
```

查看爬虫列表：

```
curl http://localhost:6800/listspiders.json?project=myproject
```



### 设置scrapyd成服务

待续