# 部署 scrapy  scrapyd

安装scrapy 

pip install scrapyd

安装deploy工具

```
pip install scrapyd-client
```

部署

windows

```
在项目根目录下，修改scrapy.cfg
url = http://localhost:6800/

```

执行`scrapyd-deploy`


使用api

启动一个爬虫

```
curl http://localhost:6800/schedule.json -d project=PROJECT_NAME -d spider=SPIDER_NAME
```

停止一个爬虫

```
curl http://localhost:6800/cancel.json -d project=PROJECT_NAME -d job=JOB_ID
```

