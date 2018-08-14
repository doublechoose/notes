## mongodb概念

基本概念：文档，集合，数据库

| database    | database    | 数据库                     |
| ----------- | ----------- | ----------------------- |
| table       | collection  | 数据库表/集合                 |
| row         | document    | 数据记录行/文档                |
| column      | field       | 数据字段/域                  |
| index       | index       | 索引                      |
| table joins |             | 表连接,MongoDB不支持          |
| primary key | primary key | 主键,MongoDB自动将_id字段设置为主键 |



## 打开mongo shell

```
cd <mangodb所在文件夹>
./bin/mongo 
```

## 数据库

### 显示所有数据库的列表

```
show dbs
# 显示当前数据库
db
```

### 使用指定数据库

默认为test,若数据库名不存在则创建

```
use <database>
```

## 文档

文档是一组键值对（key-value）。不需要设置相同的字段，并且相同字段不需要相同的数据类型。

一个简单文档：

```
{"name":"mongo","position":"here"}
```

数据库术语：

| RDBMS | MongoDB                     |
| :---- | :-------------------------- |
| 数据库   | 数据库                         |
| 表格    | 集合                          |
| 行     | 文档                          |
| 列     | 字段                          |
| 表联合   | 嵌入文档                        |
| 主键    | 主键 (MongoDB 提供了 key 为 _id ) |

- MongoDB区分类型和大小写。
- MongoDB的文档不能有重复的键。

## 集合

就是一堆文档的集合，类似于关系型数据的表

集合存在于数据库中，集合没有固定的结构，这意味着你在对集合可以插入不同格式和类型的数据，但通常情况下我们插入集合的数据都会有一定的关联性。

ObjectId 类似唯一主键，包含12个字节：

- 前 4 个字节表示创建 **unix** 时间戳,格林尼治时间 **UTC** 时间，比北京时间晚了 8 个小时
- 接下来的 3 个字节是机器标识码
- 紧接的两个字节由进程 id 组成 PID
- 最后三个字节是随机数

### 简单查询

```
db.myCollection.find();
//or
db.getCollection("myCollection").find()
// myCollection为集合名
```

### 删除数据库

```
db.dropDatabase()
```

### 删除集合

```
db.collection.drop()
//collection为集合名
show tables
//显示集合列表
```

### 创建集合

```
db.createCollection(name,options)
//name：要创建的集合名
//options : 可选参数，指定有关内存大小和索引的选项
```

options 可以是如下参数：

| 字段          | 类型   | 描述                                       |
| ----------- | ---- | ---------------------------------------- |
| capped      | 布尔   | （可选）如果为 true，则创建固定集合。固定集合是指有着固定大小的集合，当达到最大值时，它会自动覆盖最早的文档。**当该值为 true 时，必须指定 size 参数。** |
| autoIndexId | 布尔   | （可选）如为 true，自动在 _id 字段创建索引。默认为 false。    |
| size        | 数值   | （可选）为固定集合指定一个最大值（以字节计）。**如果 capped 为 true，也需要指定该字段。** |
| max         | 数值   | （可选）指定固定集合中包含文档的最大数量。                    |

```
db.createCollection("z")
//创建固定集合 mycol，整个集合空间大小 6142800 KB, 文档最大个数为 10000 个
 db.createCollection("mycol", { capped : true, autoIndexId : true, size : 
   6142800, max : 10000 } )
```

当插入一些文档的时候，会自动创建集合

```
db.z.insert({name:"mongo"})
```

### 插入文档

```
db.collection_name.insert(document)
```

例：

```
db.z.insert({title:"mongo入门1",date:"2018-07-26",content:"mongo的增删改查"})
//or 
document = ({title:"mongo入门2",date:"2018-07-26",content:"mongo的增删改查"})
db.z.insert(document)
```

### 更新文档

```
db.collection_name.update(
<query>,
<update>,
{
  upsert:<boolean>,
  multi:<boolean>,
  writeConcern:<document>
}
)
```

- **query **: update的查询条件，类似sql update查询内where后面的。
- **update **: update的对象和一些更新的操作符（如$,$inc...）等，也可以理解为sql update查询内set后面的
- **upsert **: 可选，这个参数的意思是，如果不存在update的记录，是否插入objNew,true为插入，默认是false，不插入。
- **multi **: 可选，mongodb 默认是false,只更新找到的第一条记录，如果这个参数为true,就把按条件查出来多条记录全部更新。
- **writeConcern **:可选，抛出异常的级别。

```
db.z.update({"title":"mongo入门1"},{$set:{"title":"MongoDB入门1"}})
```

以上语句只会修改第一条发现的文档，如果你要修改多条相同的文档，则需要设置 multi 参数为 true。

```
db.z.update({"title":"mongo入门1"},{$set:{"title":"MongoDB入门1"}},{multi:true})
```

### save()

save() 方法通过传入的文档来替换已有文档。

```
db.collection.save(
   <document>,
   {
     writeConcern: <document>
   }
)
```

- **document **: 文档数据。
- **writeConcern **:可选，抛出异常的级别。

例子:

```
db.z.save({"_id":ObjectId("56052f89ade2f21f36b03136"),title:"mongo入门2",date:"2018-07-26",content:"mongo的增删改查"})
```

### 删除文档

```
db.collection.remove(
   <query>,
   {
     justOne: <boolean>,
     writeConcern: <document>
   }
)
```

- **query **:（可选）删除的文档的条件。
- **justOne **: （可选）如果设为 true 或 1，则只删除一个文档。
- **writeConcern **:（可选）抛出异常的级别。

```
db.z.remove({"title":"mongo入门2"})
```

### 查询文档

```
db.collection.find(query, projection)
```

- **query** ：可选，使用查询操作符指定查询条件
- **projection** ：可选，使用投影操作符指定返回的键。查询时返回文档中所有键值， 只需省略该参数即可（默认省略）。

语法比较

| 等于    | `{<key>:<value>`}        | `db.z.find({"title":"mongo入门"}).pretty()` | `where title = 'mongo入门'` |
| ----- | ------------------------ | ---------------------------------------- | ------------------------- |
| 小于    | `{<key>:{$lt:<value>}}`  | `db.col.find({"likes":{$lt:50}}).pretty()` | `where likes < 50`        |
| 小于或等于 | `{<key>:{$lte:<value>}}` | `db.col.find({"likes":{$lte:50}}).pretty()` | `where likes <= 50`       |
| 大于    | `{<key>:{$gt:<value>}}`  | `db.col.find({"likes":{$gt:50}}).pretty()` | `where likes > 50`        |
| 大于或等于 | `{<key>:{$gte:<value>}}` | `db.col.find({"likes":{$gte:50}}).pretty()` | `where likes >= 50`       |
| 不等于   | `{<key>:{$ne:<value>}}`  | `db.col.find({"likes":{$ne:50}}).pretty()` | `where likes != 50`       |

#### and

```
db.col.find({key1:value1, key2:value2}).pretty()
```

#### or

```
db.col.find(
   {
      $or: [
         {key1: value1}, {key2:value2}
      ]
   }
).pretty()
```

### 条件操作符

- (>) 大于 - $gt
- (<) 小于 - $lt
- (>=) 大于等于 - $gte
- (<= ) 小于等于 - $lte

```
db.col.find({"likes" : {$gt : 100}})
```

### Limit

```
db.COLLECTION_NAME.find().limit(NUMBER)
```

### skip

跳过指定数量的数据。

```
db.COLLECTION_NAME.find().limit(NUMBER).skip(NUMBER)
```

### 排序

```
db.COLLECTION_NAME.find().sort({KEY:1})
```

## 索引

索引能够提高查询效率，如果没有索引，MongoDB在读取数据时必须扫描集合中的每个文件并选取那些符合查询条件的记录。这种扫描全集合的查询效率是非常低的，特别在处理大量的数据时，查询可以要花费几十秒甚至几分钟，这对网站的性能是非常致命的。索引是特殊的数据结构，索引存储在一个易于遍历读取的数据集合中，索引是对数据库表中一列或多列的值进行排序的一种结构。

```
db.collection.createIndex(keys, options)
```

## 聚合

聚合(aggregate)主要用于处理数据(诸如统计平均值,求和等)，并返回计算后的数据结果。有点类似sql语句中的 count(*)。

```
db.COLLECTION_NAME.aggregate(AGGREGATE_OPERATION)
```

