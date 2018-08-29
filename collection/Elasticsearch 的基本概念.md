# Elasticsearch 的基本概念

- Index： 用来存储数据的逻辑区域，类似于关系型数据库中的database。一个index可以在一个或多个shard（碎片）上，同时一个shard也可能有多个replicas（副本）。
- Document： 存储的实体数据，类似于关系数据的一个表里的一行数据。由多个field组成，不同的document里面同名的field一定具有相同的类型。document里的field可以重复出现，也就是一个field会有多个值。
- Document type：为了查询需要，一个index可能有多种document，也就是document type。它类似于关系型数据库中的表概念。但需要注意，不同document里面同名的field一定要是相同类型的。
- Mapping：它类似于关系型数据库中的 schema 定义概念。存储field的相关映射信息，不同document type会有不同的mapping。

## python Elasticsearch DSL使用

### 创建文档

```
from datetime import datetime
from fnmatch import fnmatch

from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, Document
from elasticsearch_dsl.connections import connections

# 定义一个默认的es客户端

ALIAS = 'test-blog'
PATTERN = ALIAS + '-*'

# initiate the default connection to elasticsearch
connections.create_connection()


class BlogPost(Document):
    title = Text()
    published = Date()
    tags = Keyword(multi=True)
    content = Text()

    def is_published(self):
        return self.published and datetime.now() > self.published

    @classmethod
    def _matches(cls, hit):
        # override _matches to match indices in a pattern instead of just ALIAS
        # hit is the raw dict as returned by elasticsearch
        return fnmatch(hit['_index'], PATTERN)

    class Index:
        # we will use an alias instead of the index
        name = ALIAS
        # set settings and possibly other attributes of the index like
        # analyzers
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }


def setup():
    """
    Create the index template in elasticsearch specifying the mappings and any
    settings to be used. This can be run at any time, ideally at every new code
    deploy.
    """
    # create an index template
    index_template = BlogPost._index.as_template(ALIAS, PATTERN)
    # upload the template into elasticsearch
    # potentially overriding the one already there
    index_template.save()

    # create the first index if it doesn't exist
    if not BlogPost._index.exists():
        migrate(move_data=False)


def migrate(move_data=True, update_alias=True):
    """
    Upgrade function that creates a new index for the data. Optionally it also can
    (and by default will) reindex previous copy of the data into the new index
    (specify ``move_data=False`` to skip this step) and update the alias to
    point to the latest index (set ``update_alias=False`` to skip).

    Note that while this function is running the application can still perform
    any and all searches without any loss of functionality. It should, however,
    not perform any writes at this time as those might be lost.
    """
    # construct a new index name by appending current timestamp
    # 通过添加当前时间戳构建一个新的索引
    next_index = PATTERN.replace('*', datetime.now().strftime('%Y%m%d%H%M%S%f'))

    # get the low level connection 获得连接
    es = connections.get_connection()

    # create new index, it will use the settings from the template
    # 创建新索引
    es.indices.create(index=next_index)

    if move_data:
        # move data from current alias to the new index
        es.reindex(
            body={"source": {"index": ALIAS}, "dest": {"index": next_index}},
            request_timeout=3600
        )
        # refresh the index to make the changes visible
        es.indices.refresh(index=next_index)

    if update_alias:
        # repoint the alias to point to the newly created index
        es.indices.update_aliases(body={
            'actions': [
                {"remove": {"alias": ALIAS, "index": PATTERN}},
                {"add": {"alias": ALIAS, "index": next_index}},
            ]
        })


article = BlogPost(meta={'id': 1}, title='Hello elasticsearch!', tags=['elasticsearch'])
article.body = ''' looong text '''
article.published_from = datetime.now()
article.save()

```

创建了一个索引为test-blog，文档为article的Elasticsearch数据库和表。
必须执行`Article.init()`方法。 这样Elasticsearch才会根据你的DocType产生对应的Mapping。否则Elasticsearch就会在你第一次创建Index和Type的时候根据你的内容建立对应的Mapping。

现在我们可以通过Elasticsearch Restful API来检查