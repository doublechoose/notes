## android中的IPC机制

- 在GNU/Linux
  - Pipes（管道）
  - Shared Memory（共享内存）
  - Message Queue（消息队列）
- 在Android
  - Binder

## 为什么用Binder而不是传统的IPC

- Binder具有socket没有的附加功能，比如binder允许跨进程传递文件描述符。
- 管道无法执行RPC
- 对象引用计数，对象映射
- Binder有精心设计的数据引用策略，它不是一个简单的内核驱动程序。

## Binder

- 一个内核驱动程序，使进程间通信变得容易。
- 轻量级RPC（远程过程通信）机制
- 每个进程的线程池用于处理请求
- 同步通信b / w进程

## IPC内部从下到上

- IPC在Binder内核驱动
- IPC在中间层
- IPC在应用层

### IPC在Binder内核驱动

![1531705844(1).png](https://upload-images.jianshu.io/upload_images/3509189-16d7686c0e338fd4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- Binder Driver支持文件操作open,mmap,release poll和系统调用ioctl（ioctl是设备驱动程序中对设备的I/O通道进行管理的函数）。

- 应用程序必须做的第一件事是打开Binder内核模块（“/ dev / Binder”）。

- 这会把文件描述符与该线程相关联

- 内核模块使用描述符来识别Binder IPC的发起者和接收者

- 与驱动程序的所有交互都将通过ioctl()的一个小命令集进行

  - BINDER_WRITE_READ
    BINDER_SET_MAX_THREADS
    BINDER_SET_CONTEXT_MGR
    BINDER_THREAD_EXIT
    BINDER_VERSION 

- 关键命令是BINDER_WRITE_READ，它是所有IPC操作的基础

  - ioctl(fd, BINDER_WRITE_READ, &bwt); 

- 要启动IPC事务，将调用带有BINDER_READ_WRITE命令的ioctl调用

  ​

要传递给ioctl（）调用的数据是struct binder_write_read类型：

```
struct binder_write_read
{
ssize_t write_size; /*bytes to write*/
ssize_t write_consumed; /*bytes consumed*/
const void* write_buffer;
ssize_t read_size; /*bytes to be read*/
void* read_buffer; /*bytes consumed*/
};
```

- 写缓冲区包含一个枚举bcTRANSACTION，后跟一个binder_transaction_data。
- 在此结构中，target是应该接收事务的对象的句柄

```
struct binder_transaction_data {
union {
size_t handle; /* target descriptor of command transaction */
void *ptr; /* target descriptor of return transaction */
}target;
void *cookie; /* target object cookie */
unsigned int code; /* transaction command */
/* General information about the transaction. */
unsigned int flags;
pid_t sender_pid;
uid_t sender_euid;
size_t data_size; /* number of bytes of data */
size_t offsets_size; /* number of bytes of offsets */
.........
};
```

![1531705930(1).png](https://upload-images.jianshu.io/upload_images/3509189-2e14c9a3920b9f2b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


### 用户进程如何接收目标进程的句柄？

#### Binder Driver IPC

![1531706018(1).png](https://upload-images.jianshu.io/upload_images/3509189-ee8063ca2ae6cfc0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- Binder在两个进程之间执行对象映射。
- 线程池与每个服务相关联以处理传入的IPC

### Service Manager 

![1531706108(1).png](https://upload-images.jianshu.io/upload_images/3509189-3750ee28b2e102a1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- Service_manager为其他进程提供注册服务
- 它必须在任何其他服务运行之前启动
- 它首先打开“/ dev / binder”驱动程序
- 然后调用BINDER_SET_CONTEXT_MGR ioctl让binder内核驱动程序知道它充当管理器
- service_manager首先运行，它将用句柄0来注册自己
- 另一个进程必须使用此句柄与service_manager进行通信

![1531706282(1).png](https://upload-images.jianshu.io/upload_images/3509189-4903ad10b2d51c4d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- 使用0作为句柄，服务提供者向服务管理器注册服务
- binder将为服务生成句柄（假设为10）
- 服务管理器将会存储名称和句柄
- 使用0作为句柄，客户端尝试获取特定服务
- 服务管理器发现该特定服务也将返回服务器的句柄“10”，以便客户端可以直接与服务器通信

### IPC在中间层

![1531706905(1).png](https://upload-images.jianshu.io/upload_images/3509189-9863a717db5de805.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


- Binder内核驱动程序上的C ++框架
- 负责marshalling（按顺序安排或组装）和unmarshalling的高级接口
- 访问应用程序的内核驱动程序
![1531707219(1).png](https://upload-images.jianshu.io/upload_images/3509189-06397e3ca688bd65.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




![image.png](https://upload-images.jianshu.io/upload_images/3509189-425e7940db90199f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


参考：
http://gityuan.com/2015/10/31/binder-prepare/
https://blog.csdn.net/boyupeng/article/details/47011383
