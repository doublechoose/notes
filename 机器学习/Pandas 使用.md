#  Pandas 使用

时间：20181129



```
import pandas as pd
import tushare as ts
pro = ts.pro_api('f46408b88d556b0b3d9c8dc27a9402dcde9eb368584057ef4434aa6d')

df = pro.index_daily(ts_code='000002.SH',start_date='20180101', end_date='20181011')

# 排序
df =df.sort_values(by='trade_date')
```

返回第0行，`close`列的值

```
df.loc[0,'close']
```

