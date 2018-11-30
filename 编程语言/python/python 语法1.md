# python 语法1

`isinstance(obj,class)`

`isinstance(crawler_or_spidercls, Crawler)`

判断该对象是不是属于某class

### ImportError:attempted relative import with no known parent package

### [python: how to convert a valid uuid from String to UUID?](https://stackoverflow.com/questions/15859156/python-how-to-convert-a-valid-uuid-from-string-to-uuid)

Just pass it to `uuid.UUID`:

```py
import uuid

o = {
    "name": "Unknown",
    "parent": "Uncategorized",
    "uuid": "06335e84-2872-4914-8c5d-3ed07d2a2f16"
}

print uuid.UUID(o['uuid']).hex
```

