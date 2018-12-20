# zipline in IPython Notebook

### 安装zipline-ebyf

```
pip install  --extra-index-url http://172.16.89.145:9010/simple/ zipline_ebyf --trusted-host 172.16.89.145
```

### 修改.zipline里文件

#### 修改extension.py

在jupyter notebook 里的一个cell里写上：

```
%%writefile /home/jovyan/.zipline/extension.py
# %load /home/jovyan/.zipline/extension.py

from zipline.data.bundles import register
from zipline_ebyf import ebyf

equities1 = {
    # BEGIN
    '000001','000002','600004','600028',
    # END
}

register(
       'ebyf-db-bundle',  # name this whatever you like
        ebyf(equities1),
        calendar_name='ebyf'
)

```

#### 添加db.yaml

```
%%writefile /home/jovyan/.zipline/db.yaml
mysqldb:
        host : '172.16.88.71'
        user : 'algo'
        password : 'algo'
        database : 'algo_trd'
        table_securities : 'securities'
        table_eod : 'securitidies_eod'
```

### ingest ebyf-db-bundle

```
!zipline ingest -b ebyf-db-bundle
```

### 安装依赖

```
!pip install cn_stock_holidays
!pip install pymysql
```



### 执行测试脚本

加载zipline环境，在jupyter notebook 的一个cell里：

```
%load_ext zipline
%matplotlib inline
```

#### 测试脚本

在下一个cell写上测试脚本：

```python
%%zipline --bundle ebyf-db-bundle --start 2017-12-1 --end 2018-1-1 -o buycndemo.pickle --trading-calendar ebyf

from zipline.api import order, record, symbol
from zipline.finance import commission, slippage


def initialize(context):
    context.asset = symbol('000001')

    # Explicitly set the commission/slippage to the "old" value until we can
    # rebuild example data.
    # github.com/quantopian/zipline/blob/master/tests/resources/
    # rebuild_example_data#L105
    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())


def handle_data(context, data):
    order(context.asset, 10)
    record(AAPL=data.current(context.asset, 'price'))


# Note: this function can be removed if running
# this algorithm on quantopian.com
def analyze(context=None, results=None):
    import matplotlib.pyplot as plt
    # Plot the portfolio and asset data.
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (RMB)')
    ax2 = plt.subplot(212, sharex=ax1)
    results.AAPL.plot(ax=ax2)
    ax2.set_ylabel('000001 price (RMB)')

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.show()

```

