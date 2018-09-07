# FileBeat

[安装](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation.html)

win:

1. [下载](https://www.elastic.co/downloads/beats/filebeat)
2. 提取zip文件到C:\Program Files
3. 将filebeat-<version>-windows重命名为Filebeat
4. 打开终端执行管理员权限
5. `PowerShell.exe -ExecutionPolicy UnRestricted -File .\install-service-filebeat.ps1`

配置Filebeat

1. 定义log文件的文件目录

```
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/*.log
```

2. 配置输出，Filebeat支持多种输出，通常发送事件给Elasticsearch，或者Logstash。

Elasticsearch：

```
output.elasticsearch:
  hosts: ["myEShost:9200"]
```

Logstash

```
curl -H 'Content-Type: application/pdf' -XPOST localhost:9200/test/1 -d @/cygdrive/c/test/test.pdf
```