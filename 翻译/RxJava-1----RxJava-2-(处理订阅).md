翻译自 https://blog.kaush.co/2017/06/21/rxjava-1-rxjava-2-disposing-subscriptions/ 

这是这三部分的继续:

1. [理解其中的变化](http://www.jianshu.com/p/6ad38ff7b838)
2. [处理订阅](http://blog.kaush.co/2017/06/21/rxjava-1-rxjava-2-disposing-subscriptions/)
3. 各种改变

# 处理订阅

这是我最初发现最棘手的部分，但作为一个Android开发者,最需要知道的（内存泄漏和所有）。

Jedi master Karnok 在wiki中解释得最清楚:

> 在RxJava 1.x,  rx.Subscription接口负责流和资源生命周期管理, 即取消订阅一个序列和释放一般资源如scheduled tasks.Reactive-Streams规范使用此名称来指定源和消费者之间的交互点：org.reactivestreams.Subscription 允许从上游请求正量并允许取消序列。

单从这个定义，似乎没有任何改变，但绝对不是这样。在我的第一篇文章中，我指出：

```
Publisher.subscribe(Subscriber) => Subscription

```

 => 和 = 比是故意的.如果你再看 [`Publisher`的订阅方法源代码](https://github.com/reactive-streams/reactive-streams-jvm/blob/v1.0.0/api/src/main/java/org/reactivestreams/Publisher.java#L28) , 你会注意到一个返回为`void`类型. 它没有返回一个Subscription 给你，让你塞进 CompositeSubscription中 (然后在onStop/onDestroy方便的处理).

```
interface Publisher<T> {
    // return type void (not Subscription like before)
    void subscribe(Subscriber<? super T> s);
}

```

Karnok 又说:

> 因为Reactive-Streams 基于接口, org.reactivestreams.Publisher 定义subscribe() 方法为空, Flowable.subscribe(Subscriber) 不再返回任何 Subscription (或者 Disposable). 其他反应基类也遵循这些签名及其各自的用户类型。

因此你再看下声明

```
// RxJava specific constructs    

// Observable implements "ObservableSource"
interface ObservableSource<T> {
    void subscribe(Observer<? super T> observer);
}

// Single implements SingleSource
interface SingleSource<T> {
    void subscribe(SingleObserver<? super T> observer);
}

interface CompletableSource {
    void subscribe(CompletableObserver observer);
}

interface MaybeSource<T> {
    void subscribe(MaybeObserver<? super T> observer);
}
```

会注意到返回类型全为`void` .

## 如何持有 Subscriptions

因此你可能会问那要怎么才能持有 Subscription  (为了您可以像负责任的公民正确地取消或处理它)?

我们来看一下 [`Subscriber`的 onSubscribe](https://github.com/reactive-streams/reactive-streams-jvm/blob/v1.0.0/api/src/main/java/org/reactivestreams/Subscriber.java#L31) 方法:

```
public interface Subscriber<T> {
  
    public void onSubscribe(Subscription s);
  
    // Subscriptions are additionally cool cause they have:
    // s.request(n) -> request data
    // s.cancel()   -> cancel this connection
    
    public void onNext(T t);
    public void onError(Throwable t);
    public void onComplete();
}
```

现在，你已经将Subscription类作为onSubscribe回调中的参数。因此，在`onSubscribe`方法中，您可以持有该订阅，然后可以在`onSubscribe`回调中方便地处理Subscription。

这实际上是一个很好的想法，因为这使得一个Subscriber的接口轻量化。在RxJava 1中，订阅者更“重”，因为他们不得不处理大量的内部处理。

...呵呵，开玩笑：这一点都不方便（至少对需要订阅者来依赖我们的生命周期的人来说），我宁愿像以前一样开心的将所有内容都推到CompositeSubscription中。但是，这是反应流规范的规则。

谢天谢地，仁慈的RxJava的维护者意识到了这种让步，并用方便的helper类来补救。

但首先，一些更多的定义：

## `Disposable` 是新的 `Subscripton`

我们在RxJava1中叫 `Subscription`现在叫`Disposable`.

**为虾米我们不能继续叫Subscription? (根据我的理解):**

1. 你必须记住，Reactive Streams规范已经保留了这个名称，而RxJava 2的维护者对于遵守规范是认真的。我们不想混淆关于Rx订阅与其他Reactive Stream规范附加库的更多功能
2. 我们仍然想要RxJava 1的一些行为和便利，如CompositeSubscriptions。

因此如果Disposables是我们正在使用的，那我们有一个 CompositeDisposable 可以让你将所有的 Disposables 放入进行处理。它的功能与我们之前使用CompositeSubscription的方式非常相似。

好的，回到最开始的问题:我怎么做才能持有Disposable?

## 持有Disposables

现在在我们进行之前, 如果您直接以lambdas的形式添加回调，这并不是一个问题，因为大多数可观察的数据源在没有提供订阅者对象的情况下使用其订阅方法调用返回Disposable：

```
Flowable.subscribe(Subscriber)
// void return type

Flowable.subscribe(nextEvent -> {}, error -> {}, () -> {})
// return Disposable so we're good

```

因此如果你看一些示例代码,下面正常工作没问题：

```
disposable =
    myAwesomeFlowable
        .observeOn(AndroidSchedulers.mainThread())
        .subscribe(event -> {
           // onNext
        }, throwable -> {
           // onError
        }, () -> {
            // onComplete
        });

compositeDisposable.add(disposable);

```

然而如果我重写代码，就有点不同了:

```
disposable =
    myAwesomeFlowable
        .observeOn(AndroidSchedulers.mainThread())
        .subscribe(new FlowableSubscriber<TextViewTextChangeEvent>() {
          @Override
          public void onSubscribe(Subscription subscription) {
          }

          @Override
          public void onNext(TextViewTextChangeEvent textViewTextChangeEvent) {
          }

          @Override
          public void onError(Throwable t) {
          }

          @Override
          public void onComplete() {
          }
        });
// ^ THIS IS WRONG. Won't work       错的，无法工作 
// compositeDisposable.add(disposable);
```

上面这段代码编译不了。如果你想传递一个 Subscriber 对象(如上面的`FlowableSubscriber`, `ObservableSource` 或者`Observer`) 这将无法工作.

大量现存的 RxJava 1代码这样写，所以菩萨心肠的 RxJava 维护者添加一个简单方法，在 Publishers 调用`subscribeWith`的时候.  wiki里说:

> 由于Reactive-Streams 规范, Publisher.subscribe 返回为空，它在2.0将不再工作。为了补救, 方法 E subscribeWith(E subscriber) 被添加进每个反应基类来返回它输入的 subscriber/observer.

```
E subscribeWith(E subscriber)

```

如果你还跟得上节奏的话，你会问。。。等下，这没返回一个 Disposable 啊! 为虾米这样看起来更绕路的会更方便？

额。。他说 你传递的`Subscriber`通过 `subscribeWith`返回给你. 但如果你的 Subscriber 本身”实现了“ Disposable 接口呢?如果您有一个DisposableSubscriber，您可以将所有实际用途作为一个disposable ，并将其添加到CompositeDisposable上，同时仍将其用作Subscriber。这通常是你想采用的模式。这些代码应该使这些技术清楚：

```
disposable =
    myAwesomeFlowable
        .observeOn(AndroidSchedulers.mainThread())
        .subscribeWith(new getDisposableSubscriber<TextViewTextChangeEvent>() {
            @Override
            public void onNext(TextViewTextChangeEvent event) {}

            @Override
            public void onError(Throwable e) {}

            @Override
            public void onComplete() { }
        });

compositeDisposable.add(disposable);

```

除了 `DisposableSubscriber`, 还有一个 `ResourceSubscriber` 实现了Disposable. 也有 `DefaultSubscriber` 没有实现 Disposable 接口, 那你就不能用 `subscribeWith`(你可以用，但是你从那里得不到一个“disposable” 出来).

 DisposableSubscriber 和 ResourceSubscriber 看起来好像做着一样的事情，你可能会问，既生瑜何生亮？

在1.x Subscriber 有能力采用Subscriptions 处理添加资源特别是生命周期结束或者Subscriber 被取消订阅时需要特定订阅者，既然2.x Subscriber是从外部声明的接口，旧的功能必须通过一个单独的抽象类“ResourceSubscriber”实现。一个关键的区别是您可以创建和关联Disposable资源，并将它们从你实现的onError（）和onComplete（）方法中处理在一起。看看 [文档中的例子](http://reactivex.io/RxJava/2.x/javadoc/io/reactivex/subscribers/ResourceSubscriber.html)

# to .clear or to .dispose

CompositeDisposable再也不能调用`unsubscribe` .已经被改名叫`dispose`☝️️，但你不想使用任何一个。`clear`还在的，可能就是你想用的那个方法。

## 这有啥区别?

unsubscribe/dispose [终止即使是未来的订阅，但clear 不会](https://github.com/kaushikgopal/RxJava-Android-Samples/commit/1e7d4b2f867a97b32a0cde81cb488c3d17d4952f) 允许你重用CompositeDisposable.

在下一部分并且是最后一部分，我们将一起看一些杂项变化.
