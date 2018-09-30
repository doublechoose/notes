# mysql 使用 （with python）

使用requirements.txt安装环境

```
pip freeze >requirements.txt

pip install -r requirements.txt
```



数据库是按照数据结构来组织、存储和管理数据的仓库。

每个数据库都有一个或者多个不同的api用于创建、访问、管理、搜索和复制所保存的数据

python3 使用 mysql

```
pip install pymysql
```

使用

```
# 打印mysql数据库版本
import pymysql

db = pymysql.connect("localhost","username","password","database_name")

cursor = db.cursor()

cursor.execute("SELECT VERSION()")

data = cursor.fetchone()
print("Database version : %s"%data)

db.close()
```

linux进入mysql命令行

```
mysql -uusername -ppassword
```

退出

```
exit
```

```
当前使用的是mysql5.6版本，在命令行使用时写了命令后需要 \g 才能执行

1.终端启动 MySQL：/etc/init.d/mysql start

2.登录 MySQL：mysql -uroot -p (用 root 账户登录),然后输入密码 

3.查看所有的数据库名字：show databases; 

4.选择一个数据库操作： use database_name; 

5.查看当前数据库下所有的表名：show tables; 

6.创建一个数据库：create database database_name; 

7.删除一个数据库：drop database database_name; 

8.创建一个表: create table mytest( uid bigint(20) not null primary key, uname varchar(20) not null); 

9.删除一个表: drop table mytest; 

10.SQL 插入语句：insert into table_name(col1,col2) values(value1,value2); 

11.SQL 更新语句：update table_name set col1='value1',col2='value2' where where_definition; 

12.SQL 查询语句：select * from table_name where.......

13.SQL 删除语句：delete from table_name where... 

14.增加表结构的字段：alert table table_name add column field1 date ,add column field2 time... 

15.删除表结构的字段：alert table table_name drop field1; 

16.查看表的结构：show columns from table_name; 

17.limit 的使用：select * from table_name limit 3;   //每页只显示 3 行 

select * from table_name limit 3,4;   //从查询结果的第三个开始，显示四项结果。 此处可很好的用来作分页处理。 

18.对查询结果进行排序: select * from table_name order by field1,orderby field2;多重排序 

19.退出 MySQL:exit; 

20.删除表中所有数据： truncate table 数据表名称 （不可恢复）
```

创建数据库

```
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""
 
cursor.execute(sql)
```

插入操作

```
sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
        lAST_NAME,AGE,SEX,INCOME)
        VALUES ('mac','Mohan',20,'M',2000)"""
# or
# sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
#      LAST_NAME, AGE, SEX, INCOME) \
#      VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
#      ('Mac', 'Mohan', 20, 'M', 2000)
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

```

查询

```
sql = "SELECT * FROM EMPLOYEE \
        WHERE INCOME > '%d'"%(1000)
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        fname = row[0]
        lname = row[1]
        age = row[2]
        sex = row[3]
        income = row[4]
        print("fname=%s,lname=%s,age=%d,sex=%s,income=%d"% \
        (fname,lname,age,sex,income))
except:
    print("error: unable to fetch data")
```

