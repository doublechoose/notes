越来越感觉到开源的伟大，开心。

最近在看OkHttp的源码，虽说是看，但是还是参考着先吃螃蟹的人的资料来看。这样也能顺藤摸瓜的了解，不至于不知道自己在干嘛。

## 把握整体

看源码，很多人都说要自上而下的看，了解整个框架的设计，而不是像看书那样，从第一页看到最后一页，所以首先先了解下OkHttp3执行的大致流程，下为OkHttp 的流程图<sup>1<sup>

![okhttp_full_process](http://upload-images.jianshu.io/upload_images/3509189-cd1805103063dc3e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 基本使用

sample中的guide/GetExample.java<sup>2<sup>

```java
public class GetExample {
  OkHttpClient client = new OkHttpClient();

  String run(String url) throws IOException {
    Request request = new Request.Builder()
        .url(url)
        .build();

    try (Response response = client.newCall(request).execute()) {
      return response.body().string();
    }
  }

  public static void main(String[] args) throws IOException {
    GetExample example = new GetExample();
    String response = example.run("https://raw.github.com/square/okhttp/master/README.md");
    System.out.println(response);
  }
}
```

一开始我是用的vscode看的源码，感觉挺麻烦的，后面换成了IntelliJ IDEA就开心多了，进入到相应方法，快了很多。从上面的`GetExample`类中，首先是先获取`OkHttpClient` :

```java
OkHttpClient client = new OkHttpClient();
```

所以先看`OkHttpClient.java`,不急着看代码，先看下说明:

```java
/**
 * Factory for {@linkplain Call calls}, which can be used to send HTTP requests and read their
 * responses.
 * ...
 **/
```

`Call`的工厂，可以发送HTTP请求，和读取他们的响应。

这是OkHttp整个的入口，形象代言人。是起着统筹兼顾，运筹帷幄的关键先生。说明中说当你使用唯一的OkHttpClient实例和在你的所有http调用中都重用这个实例，OkHttp的效率是最高的。

然后执行了：


```java
GetExample example = new GetExample();
String response = example.run("https://raw.github.com/square/okhttp/master/README.md");
```

创建了一个请求然后丢给client.newCall()

```java
try (Response response = client.newCall(request).execute()) {
      return response.body().string();
    }
```

newCall创建一个RealCall来执行这个请求。

```java
OkHttpClient.java
/**
 * Prepares the {@code request} to be executed at some point in the future.
 * 准备在未来的某个点执行这个请求
 */
@Override public Call newCall(Request request) {
  return RealCall.newRealCall(this, request, false /* for web socket */);
}
```

newRealCall 实例化一个RealCall，然后执行

```java
RealCall.java
  
@Override public Response execute() throws IOException {
  synchronized (this) {
    if (executed) throw new IllegalStateException("Already Executed");
    executed = true;
  }
  captureCallStackTrace();
  try {
    client.dispatcher().executed(this);
    Response result = getResponseWithInterceptorChain();//看这
    if (result == null) throw new IOException("Canceled");
    return result;
  } finally {
    client.dispatcher().finished(this);
  }
}
```

`getResponseWithInterceptorChain()`字面意思是使用拦截器链获得响应。

```java
RealCall.java

Response getResponseWithInterceptorChain() throws IOException {
  // Build a full stack of interceptors.
  // 建立一个全栈的拦截器
  List<Interceptor> interceptors = new ArrayList<>();
  interceptors.addAll(client.interceptors());
  interceptors.add(retryAndFollowUpInterceptor);
  interceptors.add(new BridgeInterceptor(client.cookieJar()));
  interceptors.add(new CacheInterceptor(client.internalCache()));
  interceptors.add(new ConnectInterceptor(client));
  if (!forWebSocket) {
    interceptors.addAll(client.networkInterceptors());
  }
  interceptors.add(new CallServerInterceptor(forWebSocket));

  Interceptor.Chain chain = new RealInterceptorChain(
      interceptors, null, null, null, 0, originalRequest, this, eventListener);
  return chain.proceed(originalRequest);//拦截器链是怎么炼成的
}
```

可以看到使用了一个`ArrayList`保存了好几个拦截器，那链是怎么形成的呢？

```java
RealInterceptorChain.java
  
public Response proceed(Request request, StreamAllocation streamAllocation, HttpCodec httpCodec,
    RealConnection connection) throws IOException {
  
  ...
  // blablabla 省略一些代码

  // Call the next interceptor in the chain.
  // 调用链的下一个拦截器
  RealInterceptorChain next = new RealInterceptorChain(interceptors, streamAllocation, httpCodec,
      connection, index + 1, request, call, eventListener);
  Interceptor interceptor = interceptors.get(index);
  Response response = interceptor.intercept(next);//是不是想点进去看

 ...
  // blablabla 省略一些代码

  return response;
}
```

拦截器除了最后一个`CallServerInterceptor`,都在	`interceptor.intercept(next)`中调用了`realChain.proceed();`来实现链式推进，就像流水线一样（有个高大尚的名字：责任链模式），不过有些拦截器觉得没必要推进了就会拦截。如一开始看的图所示。

最后得到响应（response）。

可能分析中有问题，欢迎一起谈论哈


## 参考资料

1. Piasy的拆OkHttp: https://blog.piasy.com/2016/07/11/Understand-OkHttp/
2. OkHttp的github: https://github.com/square/okhttp
