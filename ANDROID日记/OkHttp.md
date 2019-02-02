翻译自 https://square.github.io/okhttp/

## 预览

HTTP是现代应用网络的方式。是我们改变数据和媒介的途径。高效实用HTTP会让你加载更快和节省带宽。

OkHttp 是一种默认高效的HTTP客户端：

- 支持HTTP/2，允许对同一个host做的请求共用一个socket。
- 连接池 降低请求期（如果HTTP/2 不能用）
- 透明GZIP缩小下载大小
- 响应缓存避免重复请求

当网络卡的时候，OkHttp不屈不挠：它会静静的从常用连接问题中恢复过来。如果你的服务有多个IP地址，当第一个连接失败，OkHttp会试着轮换地址。对于IPv4+IPv6和冗余数据中心的服务，这是有必要的。OkHttp使用现代的TLS特征（SNI，ALPN）初始化新的连接，当握手失败后使用TLS 1.0连接。

使用OkHttp很简单。它的请求/响应 API 使用流建造者模式设计的。它支持同步调用和异步调用。

OkHttp支持 Android 2.3+版本。对于Java，最低版本为1.7.

## 例子

### 获取一个URL

这个程序下载一个URL和用string格式打印内容。[源码](https://raw.github.com/square/okhttp/master/samples/guide/src/main/java/okhttp3/guide/GetExample.java).

```java
OkHttpClient client = new OkHttpClient();

String run(String url) throws IOException {
  Request request = new Request.Builder()
      .url(url)
      .build();

  Response response = client.newCall(request).execute();
  return response.body().string();
}
```

### 发送一个POST到服务端

这个程序发送数据到一个服务上。[源码](https://raw.github.com/square/okhttp/master/samples/guide/src/main/java/okhttp3/guide/PostExample.java).

```java
public static final MediaType JSON
    = MediaType.parse("application/json; charset=utf-8");

OkHttpClient client = new OkHttpClient();

String post(String url, String json) throws IOException {
  RequestBody body = RequestBody.create(JSON, json);
  Request request = new Request.Builder()
      .url(url)
      .post(body)
      .build();
  Response response = client.newCall(request).execute();
  return response.body().string();
}
```

## 下载

[↓ Latest JAR](https://search.maven.org/remote_content?g=com.squareup.okhttp3&a=okhttp&v=LATEST)

你也需要[Okio](http://github.com/square/okio),OkHttp用来加速I/O操作和调整缓冲区大小。下载[最新JAR](https://search.maven.org/remote_content?g=com.squareup.okio&a=okio&v=LATEST).

#### MAVEN

```
<dependency>
  <groupId>com.squareup.okhttp3</groupId>
  <artifactId>okhttp</artifactId>
  <version>(insert latest version)</version>
</dependency>
```

#### GRADLE

```
compile 'com.squareup.okhttp3:okhttp:(insert latest version)'
```

