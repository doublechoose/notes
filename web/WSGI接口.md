WSGI接口

了解了HTTP协议和HTML文档，我们其实就明白了一个Web应用的本质就是：

1. 浏览器发送一个HTTP请求；
2. 服务器收到请求，生成一个HTML文档；
3. 服务器把HTML文档作为HTTP响应的Body发送给浏览器；
4. 浏览器收到HTTP响应，从HTTP Body取出HTML文档并显示。

所以，最简单的Web应用就是先把HTML用文件保存好，用一个现成的HTTP服务器软件，接收用户请求，从文件中读取HTML，返回。Apache、Nginx、Lighttpd等这些常见的静态服务器就是干这件事情的。

如果要动态生成HTML，就需要把上述步骤自己来实现。不过，接受HTTP请求、解析HTTP请求、发送HTTP响应都是苦力活，如果我们自己来写这些底层代码，还没开始写动态HTML呢，就得花个把月去读HTTP规范。

正确的做法是底层代码由专门的服务器软件实现，我们用Python专注于生成HTML文档。因为我们不希望接触到TCP连接、HTTP原始请求和响应格式，所以，需要一个统一的接口，让我们专心用Python编写Web业务。

这个接口就是WSGI：Web Server Gateway Interface。

无论多么复杂的Web应用程序，入口都是一个WSGI处理函数。HTTP请求的所有输入信息都可以通过`environ`获得，HTTP响应的输出都可以通过`start_response()`加上函数返回值作为Body。

复杂的Web应用程序，光靠一个WSGI函数来处理还是太底层了，我们需要在WSGI之上再抽象出Web框架，进一步简化Web开发。



client browser  nginx uWSGI Django

es api 化

1. 删除
2. 增
3. 改



```
pip install djangorestframework
```

settings.py

```
INSTALLED_APPS = [
    # ..
    'rest_framework',
]

REST_FRAMEWORK = {
'DEFAULT_PERMISSION_CLASSES':[
'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
]
}
```

allow users to create,update,delete,but read-only access for anonymous user

定义serializers

- Serializer: Provides serialization for normal Python class
  instances

- ModelSerializer: Provides serialization for model instances

- HyperlinkedModelSerializer: The same as ModelSerializer, but it 

  represents object relationships with links rather than primary keys 

serializers.py 



理解parsers和renders

序列化数据在返回给HTTP响应前，必须渲染成一个指定格式。同样的，当你得到一个http请求，你也要讲数据解析并反序列化。rest 框架包含renders和parsers来处理这些问题。

给定一个json字符串输入，可以用JSONParser类来转化为Python 对象。



