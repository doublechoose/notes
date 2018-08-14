了解了整体后，来看下使用了责任链模式的拦截器。

> 面向接口编程

在上篇[OkHttp3 阅读与理解(一) 整体篇 ](http://www.jianshu.com/p/44b64c90fa21)中，看到五花八门的拦截器，为了响应面向接口编程，首先要有一个拦截器的接口是不是：

```java
Interceptor.java
/**
 * 观察, 修改, 和潜在短路请求出去和相应的响应回来。通常拦截器会在请求或响应中添加，删除或变换头文件。
 */
  
public interface Interceptor {
  Response intercept(Chain chain) throws IOException;

  interface Chain {
    Request request();

    Response proceed(Request request) throws IOException;

    /**
     * 返回请求将执行的连接。这仅适用于网络拦截器的链;对于应用拦截器，这总是为空。
     */
    @Nullable Connection connection();
  }
}
```

可以看到，链`Chain`就在拦截器中.

我们从最后一个拦截器`CallServerInterceptor`开始看哈。

```java
CallServerInterceptor.java
/** This is the last interceptor in the chain. It makes a network call to the server. */
/** 这是拦截器链中的最后一个拦截器. 它对服务器进行网络访问. */
```

看拦截器的拦截方法：

```java
CallServerInterceptor.java
  
@Override public Response intercept(Chain chain) throws IOException {
  RealInterceptorChain realChain = (RealInterceptorChain) chain;
  //获得http流
  HttpCodec httpCodec = realChain.httpStream();
  //流的分配
  StreamAllocation streamAllocation = realChain.streamAllocation();
  //连接
  RealConnection connection = (RealConnection) realChain.connection();
  //请求
  Request request = realChain.request();

  long sentRequestMillis = System.currentTimeMillis();
  httpCodec.writeRequestHeaders(request);

  Response.Builder responseBuilder = null;
  if (HttpMethod.permitsRequestBody(request.method()) && request.body() != null) {
    // 如果请求头存在"Expect: 100-continue"，就在传输请求体前等待"HTTP/1.1 100
    // Continue" 响应。如果我们没得到这个响应，就不传输请求体，直接返回我们得到的响应
    // （如4xx响应）
    if ("100-continue".equalsIgnoreCase(request.header("Expect"))) {
      httpCodec.flushRequest();
      responseBuilder = httpCodec.readResponseHeaders(true);
    }

    if (responseBuilder == null) {
      // 当"Expect: 100-continue"存在，写入请求体
      Sink requestBodyOut = httpCodec.createRequestBody(request, request.body().contentLength());
      BufferedSink bufferedRequestBody = Okio.buffer(requestBodyOut);
      request.body().writeTo(bufferedRequestBody);
      bufferedRequestBody.close();
    } else if (!connection.isMultiplexed()) {
      // 如果没有"Expect: 100-continue"，避免HTTP/1 connection被重用。
      // 否则，我们仍然有义务传送请求主体以使连接保持状态一致。
      streamAllocation.noNewStreams();
    }
  }

  httpCodec.finishRequest();

  if (responseBuilder == null) {
    responseBuilder = httpCodec.readResponseHeaders(false);
  }

  Response response = responseBuilder
      .request(request)
      .handshake(streamAllocation.connection().handshake())//三次握手
      .sentRequestAtMillis(sentRequestMillis)
      .receivedResponseAtMillis(System.currentTimeMillis())
      .build();

  int code = response.code();
  if (forWebSocket && code == 101) {
    // 连接升级，但我们需要保证拦截器看到是非空响应体
 	// 101 表示需要切换协议，服务器通过 Upgrade 响应头字段通知客户端。
    response = response.newBuilder()
        .body(Util.EMPTY_RESPONSE)
        .build();
  } else {
    response = response.newBuilder()
        .body(httpCodec.openResponseBody(response))
        .build();
  }

  if ("close".equalsIgnoreCase(response.request().header("Connection"))
      || "close".equalsIgnoreCase(response.header("Connection"))) {
    streamAllocation.noNewStreams();
  }

  // 204  服务器成功处理了请求，但不需要返回任何实体内容，204响应禁止包含任何消息体。
  // 浏览器收到该响应后不应产生文档视图的变化。
  // 205  服务器成功处理了请求，但不需要返回任何实体内容，205响应禁止包含任何消息体。
  // 与204不同的是，返回此状态码的响应要求请求者重置文档视图。
  // 所以响应体不应有内容
  if ((code == 204 || code == 205) && response.body().contentLength() > 0) {
    throw new ProtocolException(
        "HTTP " + code + " had non-zero Content-Length: " + response.body().contentLength());
  }

  return response;
}
```



是不是看的雾煞煞，一到细节部分就要起效了。



## ConnectInterceptor

唉，为啥不从这个开始呢，这个这么短，唉，选错拦截器分析了

```java
/** Opens a connection to the target server and proceeds to the next interceptor. */
/** 对目标服务器打开连接，执行下一个拦截器. */
```



```java
ConnectInterceptor.java

@Override public Response intercept(Chain chain) throws IOException {
  RealInterceptorChain realChain = (RealInterceptorChain) chain;
  Request request = realChain.request();
  StreamAllocation streamAllocation = realChain.streamAllocation();

  // We need the network to satisfy this request. Possibly for validating a conditional GET.
  // 我们需要网络来满足这个请求，可能用于验证GET 条件
  boolean doExtensiveHealthChecks = !request.method().equals("GET");
  HttpCodec httpCodec = streamAllocation.newStream(client, doExtensiveHealthChecks);
  RealConnection connection = streamAllocation.connection();

  return realChain.proceed(request, streamAllocation, httpCodec, connection);
}
```

这个很简单，就是获得RealConnection实例，并传给下一个拦截器。

## CacheInterceptor

```java
/** Serves requests from the cache and writes responses to the cache. */
/** 从缓存提供请求，并将响应写入缓存。 */
```

根据策略进行缓存

如果被禁止使用网络并且缓存为空，则失败，不再传递到下一个拦截器，返回一个504的响应

如果不需要网络，则完成了，返回缓存中的响应

进入下一个拦截器，获得服务器返回的响应

- 如果有response的缓存，我们有条件的获取

重新存储响应缓存

如果使无效，删除缓存

## BridgeInterceptor

```java
/**
 * Bridges from application code to network code. First it builds a network request from a user
 * request. Then it proceeds to call the network. Finally it builds a user response from the network
 * response.
 */
/**
 * 桥接应用code到网络code。
 * 首先，从一个user request建立一个网络request；
 * 然后，执行调用网络；
 * 最后，从网络的response建立一个user response.
 */
```

什么是user request，network Request 呢？对用户来说，做一次请求，他只需要给出请求的url，有时候要有请求体，这样就可以了吗，对于用户，他们只需要知道这么多，但是对于网络的请求，可要更多的信息，这些可以由程序自动添加，而响应也是，用户需要的响应内容只是其中的一部分，所以要筛选出来。所以这个`BridgeInterceptor`的作用，就是user Request/Response 和 network Request/Response 的转换。

然后就可以看到`BridgeInterceptor`的`intercept`方法，就有很多if-else语句来完成网络需要的请求，获取到的响应就有remove来删除不用的数据。

## RetryAndFollowUpInterceptor

```java
/**
 * This interceptor recovers from failures and follows redirects as necessary. It may throw an
 * {@link IOException} if the call was canceled.
 */
 /**
 * 这个拦截器从失败中恢复，并根据需要遵循重定向。如果呼叫被取消可能会抛出
 * {@link IOException}.
 */
```

下次再补充，下班！

