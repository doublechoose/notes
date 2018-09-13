## Mongo导入导出



导出数据：

1.导出为json格式文件：mongoexport -d <数据库名称> -c <collection名称> -o <json文件名称>

2.导出为csv格式文件：mongoexport -d <数据库名称> -c <collection名称> --csv - f <key字段（key字段如下图所示，字段之间用逗号分隔）> - o <csv文件名称>

例子：



导入数据：

1.导入json格式文件数据： mongoimport -d <数据库名称> -c <collection名称> --file <要导入的json文件名称>

2.导入csv格式文件数据：mongoimport -d <数据库名称> -c <collection名称> --type csv --headerline --file <csv文件名称>

进入命令行模式：

mongo

显示数据库

show dbs

显示collection

use adb

show collections

