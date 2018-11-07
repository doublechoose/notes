python mysql 插入timestamp

```
import datetime
now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")
```

mysql 



```
>describe all_fp
>
+--------------+-------------+------+-----+---------+----------------+
| Field        | Type        | Null | Key | Default | Extra          |
+--------------+-------------+------+-----+---------+----------------+
| id           | int(11)     | NO   | PRI | NULL    | auto_increment |
| timestamp    | datetime    | NO   |     | NULL    |                |
| page_url     | varchar(64) | NO   |     | NULL    |                |
| page_url_sha | varchar(64) | NO   |     | NULL    |                |
| page_status  | int(11)     | NO   |     | NULL    |                |
+--------------+-------------+------+-----+---------+----------------+
```

python 读取文件并写入文件

```
filer = open("D:\\ADev\\ceg\\search\\scrapy-script\\elasticsearchscrapy\\deduplication\ded\\times.txt",'r')

oldline = filer.readline()

times = int(oldline)

# times = int(file.readline())
filer.close()

filew = open("D:\\ADev\\ceg\\search\\scrapy-script\\elasticsearchscrapy\\deduplication\ded\\times.txt",'w')

times = times+1
newline = str(times)

filew.write(newline)
filew.close()

print(type(times))
```

