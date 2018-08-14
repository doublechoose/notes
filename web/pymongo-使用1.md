### 获取文档中的数组，叠加并设置新的字段

```
from pymongo import MongoClient

# mongodb 设置
MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017  # MONGO 端口
MONGO_DB = "football"
MONGO_COLL = "wlist"

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = client[MONGO_DB]  # 获取数据库句柄
coll = db[MONGO_COLL]  # 获取collection句柄

player_list = coll.find()

for player in player_list:
    print(player["name"])
    total = 0
    for i in player["capabilityValues"]["extend"]:
        total = total + int(i)
    coll.update_one({"_id": player["_id"]}, {'$set': {'capabilitySum': total}})

```

### 根据sum值进行降序，保存到文本中

```
from pymongo import MongoClient
import pymongo

# mongodb 设置
MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017  # MONGO 端口
MONGO_DB = "football"
MONGO_COLL = "wlist"

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = client[MONGO_DB]  # 获取数据库句柄
coll = db[MONGO_COLL]  # 获取collection句柄

position = ['ST', 'LW', 'RW', 'LF', 'CF', 'RF', 'CAM',
            'LM', 'CM', 'RM', 'CDM', 'LWB',
            'LB', 'CB', 'RB', 'RWB', 'GK', ]

# player_list = coll.find()
file = open("Ranking.txt", 'w')

for p in position:
    player_list = coll.find({"jobCode": p}).sort("capabilitySum", pymongo.DESCENDING).limit(5)
    file.write("---------%s----------\n" % p)
    for player in player_list:
        print("name:%s\n" % player["name"])
        file.write("name:%s       " %player["name"])
        print("capabilitySum:%s" % player["capabilitySum"])
        file.write("capabilitySum:%s\n" % player["capabilitySum"])

file.close()

# for player in player_list:
#     print(player["name"])
#     total = 0
#     jobCode = player["basicInfo"]["jobCode"]
#     print(jobCode)
#     coll.update_one({"_id": player["_id"]}, {'$set': {'jobCode': jobCode}})

```
