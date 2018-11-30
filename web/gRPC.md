# gRPC

## 什么是gRPC

在gRPC，client应用可以在不同的机器上直接调用server应用的方法，就像是该对象就在本地一样，使得更容易创建分布式应用程序和服务。与许多RPC系统一样，gRPC基于定义服务的思想，指定可以使用其参数和返回类型远程调用的方法。 在服务器端，服务器实现此接口并运行gRPC服务器来处理客户端调用。 在客户端，客户端有一个存根（在某些语言中称为客户端），它提供与服务器相同的方法。

![Concept Diagram](https://grpc.io/img/landing-2.svg)

gRPC客户端和服务器可以在各种环境中相互运行和通信 - 从Google内部的服务器到您自己的桌面 - 并且可以使用任何gRPC支持的语言编写。 因此，例如，您可以使用Go，Python或Ruby轻松创建Java中的gRPC服务器。 此外，最新的Google API将具有gRPC版本的界面，让您可以轻松地在应用程序中构建Google功能。

### 使用Protocol Buffers

默认情况下，gRPC使用协议缓冲区，这是Google成熟的开源机制，用于序列化结构化数据（尽管它可以与其他数据格式（如JSON）一起使用）。 这是一个如何工作的快速介绍。 如果您已经熟悉协议缓冲区，请随时跳到下一部分。

使用协议缓冲区的第一步是定义要在proto文件中序列化的数据的结构：这是一个扩展名为.proto的普通文本文件。 协议缓冲区数据被构造为消息，其中每条消息是包含一系列称为字段的名称 - 值对的信息的小型逻辑记录。 这是一个简单的例子：

```
message Person {
  string name = 1;
  int32 id = 2;
  bool has_ponycopter = 3;
}
```

然后，一旦指定了数据结构，就可以使用协议缓冲区编译器protoc从原型定义生成首选语言的数据访问类。 这些为每个字段提供了简单的访问器（如name（）和set_name（）），以及将整个结构序列化/解析为原始字节的方法 - 例如，如果您选择的语言是C ++，则运行编译器 上面的例子将生成一个名为Person的类。 然后，您可以在应用程序中使用此类来填充，序列化和检索Person协议缓冲区消息。

正如您将在我们的示例中更详细地看到的那样，您可以在普通的proto文件中定义gRPC服务，并将RPC方法参数和返回类型指定为协议缓冲区消息：

```
// The greeter service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
```

gRPC还使用带有特殊gRPC插件的protoc来生成proto文件中的代码。 但是，使用gRPC插件，您可以生成gRPC客户端和服务器代码，以及用于填充，序列化和检索消息类型的常规协议缓冲区代码。 我们将在下面更详细地看一下这个例子。

您可以在Protocol Buffers文档中找到有关协议缓冲区的更多信息，并了解如何使用所选语言的快速入门获取和安装带有gRPC插件的protoc。

### 缓冲区协议版本

虽然协议缓冲区已经有一段时间可用于开源用户，但我们的示例使用了一种新的协议缓冲区，称为proto3，它具有略微简化的语法，一些有用的新功能，并支持更多语言。 目前提供Java，C ++，Python，Objective-C，C＃，来自协议缓冲区GitHub repo的lite-runtime（Android Java），Ruby和JavaScript，以及来自golang / protobuf GitHub的Go语言生成器。 repo，开发中有更多语言。 您可以在proto3语言指南和每种语言的参考文档中找到更多信息。 参考文档还包括.proto文件格式的正式规范。

通常，虽然您可以使用proto2（当前默认协议缓冲版本），但我们建议您将proto3与gRPC一起使用，因为它允许您使用全系列gRPC支持的语言，并避免与proto2客户端通信时的兼容性问题 proto3服务器，反之亦然。



## 快速开始gRPC （python）

### 安装

### Install gRPC

Install gRPC:

```
$ python -m pip install grpcio
```

Or, to install it system wide:

```
$ sudo python -m pip install grpcio
```

On El Capitan OSX, you may get the following error:

```
$ OSError: [Errno 1] Operation not permitted: '/tmp/pip-qwTLbI-uninstall/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/six-1.4.1-py2.7.egg-info'
```

You can work around this using:

```
$ python -m pip install grpcio --ignore-installed
```

### 安装gRPC tool

Python的gRPC工具包括协议缓冲区编译器protoc和用于从.proto服务定义生成服务器和客户端代码的特殊插件。 对于我们的快速入门示例的第一部分，我们已经从helloworld.proto生成了服务器和客户端存根，但是您将需要其他快速入门的工具，以及后续教程和您自己的项目。

要安装gRPC工具，请运行：

```
python -m pip install grpcio-tools googleapis-common-protos
```

### 下载例子

```
$ # Clone the repository to get the example code:
$ git clone -b v1.16.0 https://github.com/grpc/grpc
$ # Navigate to the "hello, world" Python example:
$ cd grpc/examples/python/helloworld
```

### 运行示例

From the `examples/python/helloworld` directory:

1. Run the server

   ```
   $ python greeter_server.py
   ```

2. In another terminal, run the client

   ```
   $ python greeter_client.py
   ```

Congratulations! You’ve just run a client-server application with gRPC.



### 更新一个gRPC服务

现在让我们看看如何使用服务器上的额外方法更新应用程序以供客户端调用。 我们的gRPC服务是使用协议缓冲区定义的; 您可以在什么是gRPC中找到有关如何在.proto文件中定义服务的更多信息？ 和gRPC基础知识：Python。 现在您需要知道的是，服务器和客户端“存根”都有一个SayHello RPC方法，该方法从客户端获取HelloRequest参数并从服务器返回HelloResponse，并且此方法定义如下：

```
// The greeting service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
```

让我们更新一下，以便Greeter服务有两种方法。 编辑examples / protos / helloworld.proto并使用新的SayHelloAgain方法更新它，具有相同的请求和响应类型：

```
// The greeting service definition.
service Greeter {
  // Sends a greeting
  rpc SayHello (HelloRequest) returns (HelloReply) {}
  // Sends another greeting
  rpc SayHelloAgain (HelloRequest) returns (HelloReply) {}
}

// The request message containing the user's name.
message HelloRequest {
  string name = 1;
}

// The response message containing the greetings
message HelloReply {
  string message = 1;
}
```

### 生成gRPC 代码

接下来，我们需要更新应用程序使用的gRPC代码以使用新的服务定义。

从examples / python / helloworld目录中，运行：

```
$ python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. ../../protos/helloworld.proto
```

这将重新生成helloworld_pb2.py，其中包含我们生成的请求和响应类以及helloworld_pb2_grpc.py，其中包含我们生成的客户端和服务器类。



### 更新和运行应用

我们现在有了新生成的服务器和客户端代码，但是我们仍然需要在示例应用程序的人工编写部分中实现并调用新方法。

#### 更新server

在同一目录中，打开greeter_server.py。 像这样实现新方法：

```
class Greeter(helloworld_pb2_grpc.GreeterServicer):

  def SayHello(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)

  def SayHelloAgain(self, request, context):
    return helloworld_pb2.HelloReply(message='Hello again, %s!' % request.name)
...
```

#### 更新client

在同一目录中，打开greeter_client.py。 像这样调用新方法：

```
def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = helloworld_pb2_grpc.GreeterStub(channel)
  response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
  print("Greeter client received: " + response.message)
  response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='you'))
  print("Greeter client received: " + response.message)
```

#### 运行！

1. Run the server

   ```
   $ python greeter_server.py
   ```

2. In another terminal, run the client

   ```
   $ python greeter_client.py
   ```

##  gRPC 基础（python）

1. 定义一个service到.proto 文件
2. 生成服务和客户端代码，使用缓存协议编译器
3. 使用python的gRPC API写一个简单的客户端和服务端

### 为什么使用gRPC

此示例是一个简单的路由映射应用程序，它允许客户端获取有关其路由上的功能的信息，创建其路由摘要，以及与服务器和其他客户端交换路由信息（如流量更新）。

使用gRPC，您可以在.proto文件中定义您的服务一次，并使用任何gRPC支持的语言实现客户端和服务器，而这些语言又可以在从Google内部服务器到您自己的平板电脑的各种环境中运行，并且具有所有复杂的通信 gRPC为您处理不同的语言和环境。 您还可以获得使用协议缓冲区的所有优势，包括高效的序列化，简单的IDL和简单的接口更新。

### 示例代码和设置

示例代码位置：[grpc/grpc/examples/python/route_guide](https://github.com/grpc/grpc/tree/v1.16.0/examples/python/route_guide)

```
cd grpc/examples/python/route_guide
```

### 定义服务

To define a service, you specify a named `service` in your .proto file:

```
service RouteGuide {
   // (Method definitions not shown)
}
```

然后在服务定义中定义rpc方法，指定它们的请求和响应类型。 gRPC允许您定义四种服务方法，所有这些都在RouteGuide服务中使用：

- 一个简单的RPC，客户端使用存根向服务器发送请求并等待响应返回，就像正常的函数调用一样。

  - ```
    // Obtains the feature at a given position.
    rpc GetFeature(Point) returns (Feature) {}
    ```

- 响应流RPC，客户端向服务器发送请求并获取流以读取消息序列。 客户端从返回的流中读取，直到没有更多消息。 正如您在示例中所看到的，您可以通过将stream关键字放在响应类型之前来指定响应流方法。

  - ```
    // Obtains the Features available within the given Rectangle.  Results are
    // streamed rather than returned at once (e.g. in a response message with a
    // repeated field), as the rectangle may cover a large area and contain a
    // huge number of features.
    rpc ListFeatures(Rectangle) returns (stream Feature) {}
    ```

- 请求流式RPC，客户端再次使用提供的流写入一系列消息并将其发送到服务器。 客户端完成消息编写后，等待服务器全部读取并返回响应。 您可以通过将stream关键字放在请求类型之前来指定请求流方法。

  ```
  // Accepts a stream of Points on a route being traversed, returning a
  // RouteSummary when traversal is completed.
  rpc RecordRoute(stream Point) returns (RouteSummary) {}
  ```

- 双向流式RPC，双方使用读写流发送一系列消息。 这两个流独立运行，因此客户端和服务器可以按照他们喜欢的顺序进行读写：例如，服务器可以在写入响应之前等待接收所有客户端消息，或者它可以交替读取消息然后写入消息， 或其他一些读写组合。 保留每个流中的消息顺序。 您可以通过在请求和响应之前放置stream关键字来指定此类方法。

  - ```
    // Accepts a stream of RouteNotes sent while a route is being traversed,
    // while receiving other RouteNotes (e.g. from other users).
    rpc RouteChat(stream RouteNote) returns (stream RouteNote) {}
    ```

您的.proto文件还包含我们的服务方法中使用的所有请求和响应类型的协议缓冲区消息类型定义 - 例如，这里是Point消息类型：

```
// Points are represented as latitude-longitude pairs in the E7 representation
// (degrees multiplied by 10**7 and rounded to the nearest integer).
// Latitudes should be in the range +/- 90 degrees and longitude should be in
// the range +/- 180 degrees (inclusive).
message Point {
  int32 latitude = 1;
  int32 longitude = 2;
}
```

### 生成客户端和服务端的代码

```
python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. ../../protos/route_guide.proto
```

Note that as we’ve already provided a version of the generated code in the example directory, running this command regenerates the appropriate file rather than creates a new one. The generated code files are called `route_guide_pb2.py` and `route_guide_pb2_grpc.py` and contain:

- classes for the messages defined in route_guide.proto
- classes for the service defined in route_guide.proto
  - `RouteGuideStub`, which can be used by clients to invoke RouteGuide RPCs
  - `RouteGuideServicer`, which defines the interface for implementations of the RouteGuide service
- a function for the service defined in route_guide.proto
  - `add_RouteGuideServicer_to_server`, which adds a RouteGuideServicer to a `grpc.Server`

Note: The `2` in pb2 indicates that the generated code is following Protocol Buffers Python API version 2. Version 1 is obsolete. It has no relation to the Protocol Buffers Language version, which is the one indicated by `syntax = "proto3"` or `syntax = "proto2"` in a .proto file.



## Creating the server





First let’s look at how you create a `RouteGuide` server. If you’re only interested in creating gRPC clients, you can skip this section and go straight to [Creating the client](https://grpc.io/docs/tutorials/basic/python.html#client) (though you might find it interesting anyway!).

Creating and running a `RouteGuide` server breaks down into two work items:

- Implementing the servicer interface generated from our service definition with functions that perform the actual “work” of the service.
- Running a gRPC server to listen for requests from clients and transmit responses.

You can find the example `RouteGuide` server in[examples/python/route_guide/route_guide_server.py](https://github.com/grpc/grpc/blob/v1.16.0/examples/python/route_guide/route_guide_server.py).

### Implementing RouteGuide

`route_guide_server.py` has a `RouteGuideServicer` class that subclasses the generated class `route_guide_pb2_grpc.RouteGuideServicer`:

```
# RouteGuideServicer provides an implementation of the methods of the RouteGuide service.
class RouteGuideServicer(route_guide_pb2_grpc.RouteGuideServicer):
```

`RouteGuideServicer` implements all the `RouteGuide` service methods.

#### Simple RPC

Let’s look at the simplest type first, `GetFeature`, which just gets a `Point` from the client and returns the corresponding feature information from its database in a `Feature`.

```
def GetFeature(self, request, context):
  feature = get_feature(self.db, request)
  if feature is None:
    return route_guide_pb2.Feature(name="", location=request)
  else:
    return feature
```

The method is passed a `route_guide_pb2.Point` request for the RPC, and a `grpc.ServicerContext` object that provides RPC-specific information such as timeout limits. It returns a `route_guide_pb2.Feature` response.

#### Response-streaming RPC

Now let’s look at the next method. `ListFeatures` is a response-streaming RPC that sends multiple `Feature`s to the client.

```
def ListFeatures(self, request, context):
  left = min(request.lo.longitude, request.hi.longitude)
  right = max(request.lo.longitude, request.hi.longitude)
  top = max(request.lo.latitude, request.hi.latitude)
  bottom = min(request.lo.latitude, request.hi.latitude)
  for feature in self.db:
    if (feature.location.longitude >= left and
        feature.location.longitude <= right and
        feature.location.latitude >= bottom and
        feature.location.latitude <= top):
      yield feature
```

Here the request message is a `route_guide_pb2.Rectangle` within which the client wants to find `Feature`s. Instead of returning a single response the method yields zero or more responses.

#### Request-streaming RPC

The request-streaming method `RecordRoute` uses an [iterator](https://docs.python.org/2/library/stdtypes.html#iterator-types) of request values and returns a single response value.

```
def RecordRoute(self, request_iterator, context):
  point_count = 0
  feature_count = 0
  distance = 0.0
  prev_point = None

  start_time = time.time()
  for point in request_iterator:
    point_count += 1
    if get_feature(self.db, point):
      feature_count += 1
    if prev_point:
      distance += get_distance(prev_point, point)
    prev_point = point

  elapsed_time = time.time() - start_time
  return route_guide_pb2.RouteSummary(point_count=point_count,
                                      feature_count=feature_count,
                                      distance=int(distance),
                                      elapsed_time=int(elapsed_time))
```

#### Bidirectional streaming RPC

Lastly let’s look at the bidirectionally-streaming method `RouteChat`.

```
def RouteChat(self, request_iterator, context):
  prev_notes = []
  for new_note in request_iterator:
    for prev_note in prev_notes:
      if prev_note.location == new_note.location:
        yield prev_note
    prev_notes.append(new_note)
```

This method’s semantics are a combination of those of the request-streaming method and the response-streaming method. It is passed an iterator of request values and is itself an iterator of response values.

### Starting the server

Once you have implemented all the `RouteGuide` methods, the next step is to start up a gRPC server so that clients can actually use your service:

```
def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
      RouteGuideServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
```

Because `start()` does not block you may need to sleep-loop if there is nothing else for your code to do while serving.



## Creating the client





You can see the complete example client code in[examples/python/route_guide/route_guide_client.py](https://github.com/grpc/grpc/blob/v1.16.0/examples/python/route_guide/route_guide_client.py).

### Creating a stub

To call service methods, we first need to create a *stub*.

We instantiate the `RouteGuideStub` class of the `route_guide_pb2_grpc` module, generated from our .proto.

```
channel = grpc.insecure_channel('localhost:50051')
stub = route_guide_pb2_grpc.RouteGuideStub(channel)
```

### Calling service methods

For RPC methods that return a single response (“response-unary” methods), gRPC Python supports both synchronous (blocking) and asynchronous (non-blocking) control flow semantics. For response-streaming RPC methods, calls immediately return an iterator of response values. Calls to that iterator’s `next()` method block until the response to be yielded from the iterator becomes available.

#### Simple RPC

A synchronous call to the simple RPC `GetFeature` is nearly as straightforward as calling a local method. The RPC call waits for the server to respond, and will either return a response or raise an exception:

```
feature = stub.GetFeature(point)
```

An asynchronous call to `GetFeature` is similar, but like calling a local method asynchronously in a thread pool:

```
feature_future = stub.GetFeature.future(point)
feature = feature_future.result()
```

#### Response-streaming RPC

Calling the response-streaming `ListFeatures` is similar to working with sequence types:

```
for feature in stub.ListFeatures(rectangle):
```

#### Request-streaming RPC

Calling the request-streaming `RecordRoute` is similar to passing an iterator to a local method. Like the simple RPC above that also returns a single response, it can be called synchronously or asynchronously:

```
route_summary = stub.RecordRoute(point_iterator)
route_summary_future = stub.RecordRoute.future(point_iterator)
route_summary = route_summary_future.result()
```

#### Bidirectional streaming RPC

Calling the bidirectionally-streaming `RouteChat` has (as is the case on the service-side) a combination of the request-streaming and response-streaming semantics:

```
for received_route_note in stub.RouteChat(sent_route_note_iterator):
```

## Try it out!





Run the server, which will listen on port 50051:

```
$ python route_guide_server.py
```

Run the client (in a different terminal):

```
$ python route_guide_client.py
```