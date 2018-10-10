20181009



scrapd Log 中文乱码：

原因： 由于 Scrapyd 的 Web Interface 的 log 链接直接指向 log 文件，Response Headers 的 Content-Type 又没有声明字符集 charset=UTF-8，因此通过浏览器查看 log 会出现非 ASCII 乱码。

因为直接访问log文件，未设置headers里的：

```
Content-Type: text/html; charset=UTF-8
```

解决办法1：

chrome设置插件https://github.com/jinliming2/Chrome-Charset

解决办法2：

修改scrapd源码

website.py

```python
header_cols = [
        'Project', 'Spider',
        'Job', 'PID',
        'Start', 'Runtime', 'Finish',
        'Log','UTF8','Items',
        'Cancel',
    ]
# ...
def prep_tab_running(self):
        return '\n'.join(
            self.prep_row(dict(
                Project=p.project, Spider=p.spider,
                Job=p.job, PID=p.pid,
                Start=microsec_trunc(p.start_time),
                Runtime=microsec_trunc(datetime.now() - p.start_time),
                Log='<a href="/logs/%s/%s/%s.log">Log</a>' % (p.project, p.spider, p.job),
                # 增加这个
                UTF8="<a href='/logs/utf8.html?project=%s&spider=%s&job=%s' target='_blank'>UTF-8</a>" % (p.project, p.spider, p.job),
                Items='<a href="/items/%s/%s/%s.jl">Items</a>' % (p.project, p.spider, p.job),
                Cancel=self.cancel_button(project=p.project, jobid=p.job)
            ))
            for p in self.root.launcher.processes.values()
        )
 
    def prep_tab_finished(self):
        return '\n'.join(
            self.prep_row(dict(
                Project=p.project, Spider=p.spider,
                Job=p.job,
                Start=microsec_trunc(p.start_time),
                Runtime=microsec_trunc(p.end_time - p.start_time),
                Finish=microsec_trunc(p.end_time),
                Log='<a href="/logs/%s/%s/%s.log">Log</a>' % (p.project, p.spider, p.job),
                # 增加这行
                UTF8="<a href='/logs/utf8.html?project=%s&spider=%s&job=%s' target='_blank'>UTF-8</a>" % (p.project, p.spider, p.job),
                Items='<a href="/items/%s/%s/%s.jl">Items</a>' % (p.project, p.spider, p.job),
            ))
            for p in self.root.launcher.finished
        )
```



logs/utf8.html

```
<html>
<head><meta charset="UTF-8"></head>
<iframe src="" width="100%" height="100%"></iframe>

<script>
function parseQueryString(url) {
    var urlParams = {};
    url.replace(
        new RegExp("([^?=&]+)(=([^&]*))?", "g"),
        function($0, $1, $2, $3) {
            urlParams[$1] = $3;
        }
    );
    return urlParams;
}

var kwargs = parseQueryString(location.search);
document.querySelector('iframe').src = "/logs/" + kwargs.project + '/' + kwargs.spider + '/' + kwargs.job + '.log'
</script>
```



iframe 元素会创建包含另外一个文档的内联框架（即行内框架）。

location.search

search 属性是一个可读可写的字符串，可设置或返回当前 URL 的查询部分（问号 ? 之后的部分）。

\_\_file\_\_ 用来获取模块所在的路径

\_\_init\_\_.py 作用：

导入一个包时，实际上是导入了它的\_\_init\_\_.py文件.

标识该目录为一个模块

**关于.pyc 文件 与 .pyo 文件**

.py文件的汇编,只有在import语句执行时进行，当.py文件第一次被导入时，它会被汇编为字节代码，并将字节码写入同名的.pyc文件中。后来每次导入操作都会直接执行.pyc 文件（当.py文件的修改时间发生改变，这样会生成新的.pyc文件），在解释器使用-O选项时，将使用同名的.pyo文件，这个文件去掉了断言（assert）、断行号以及其他调试信息，体积更小，运行更快。（使用-OO选项，生成的.pyo文件会忽略文档信息）

zope.interface 与面向对象

1. 类通过继承接口，来继承接口的抽象方法；
2. 接口不是类（虽然编写类和方法的方式很类似）；
3. 类描述对象的属性和方法（实现接口的类，必须实现接口内所描述的所有方法，否则必须声明为抽象类）；
4. 接口包含类要实现的方法（接口无法被实例化，但可以被实现）；

接口定义规范，不负责具体实现。

python中也有interface的概念，但是python其本身不提供interface的实现，需要通过第三方扩展库来使用类似interface的功能，一般都是Zope.interface

