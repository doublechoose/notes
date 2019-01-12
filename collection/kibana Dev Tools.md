GET site/_search
{
  "query": {
    "match_all": {}
  }
}




PUT io/doc/3
{
  "title":"xxx",
  "url":"https://xxx.io/news/post/29/"
}

DELETE io/doc/3

GET site/_search
GET io/_search

GET xx/_search

GET _search
{
  "_source": ["title","url","doc_type"],
  
    "query": {
        "multi_match": {
            "query": "演辞1", 
            "fields":  [ "title", "page_title" ]
        }
    }
    , "highlight": {
      "fields": {
        "title": {},
        "content": {}
      }
    }
}

# 删除xx index下的所有文档
POST site/_delete_by_query?refresh&slices=3&pretty
{
  "query": {
    "match_all": {}
  }

}

# 删除某文档
DELETE io/doc/_DLFC2cBZee-FbMqfeYG

DELETE site