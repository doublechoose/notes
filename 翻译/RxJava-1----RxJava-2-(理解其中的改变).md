翻译自：https://blog.kaush.co/2017/06/21/rxjava1-rxjava2-migration-understanding-changes/

如果你还没听说过，跟你说下：[RxJava2](https://github.com/ReactiveX/RxJava/wiki/What%27s-different-in-2.0https://github.com/ReactiveX/RxJava/wiki/What%27s-different-in-2.0) 已经发布啦。RxJava2被大规模的重写并改了api（但是有好处的）。大多依赖库已经升级，你可以安全的迁移到你的代码库中。

一开始就使用Rx2的人可能会喜欢这个指南，如果是从Rx1开始的人，可能会感到欣喜若狂。

我已经将这个指南分为3个部分：

1. [理解其中的改变](http://blog.kaush.co/2017/06/21/rxjava1-rxjava2-migration-understanding-changes/)
2. [处理订阅](http://blog.kaush.co/2017/06/21/rxjava-1-rxjava-2-disposing-subscriptions/)
3. 各种改变

第一部分，我想从Rx1用户的角度来看，深入了解Rx2的变化。

## 为什么RxJava2变了

### [Reactive Streams](http://www.reactive-streams.org/) spec 反应流规范

[Reactive Streams](http://www.reactive-streams.org/)对于*Reactive* Programming是一个标准，RxJava现在在版本2.x中实现了反应流规范（Reactive Streams spec）。RxJava是reactive programming领域中的开拓者之一，但它不是唯一的库。还有其他的处理反应式的库。但是现在所有的库都遵循反应流规范（Reactive Streams spec），这样库之间的操作更容易一些。

每个说明的规格都是非常简单的，只有4个接口：

1. **Publisher** (任何可以发布事件的, 如 `Observable`,`Flowable` 等. - 下文详细说明)
2. **Subscriber** (任何可以监听**Publisher** 的)
3. **Subscription** (`Publisher.subscribe(Subscriber) => Subscription` 当你加入一个发布者Publisher 和一个订阅者Subscriber时, 你将得到一个连接，也叫订阅 `Subscription`)
4. **Processor** (a Publisher + a Subscriber, 是不是有点熟悉？是的，对于RxJava1用户来说，叫`Subject`)

如果你有点好奇为啥要这样设计，我建议看下下面这些资源：

- [What’s different in 2.0](https://github.com/ReactiveX/RxJava/wiki/What%27s-different-in-2.0) wiki 页面 - 这个是当我需要理解细节的时候，我经常看和参考的地方。
- [Fragmented Ep #53 with JakeWharton](http://fragmentedpodcast.com/episodes/053-jake-wharton-on-rxjava-2/) (forgive the shameless promotion) - ultimate lazy person’s guide to understand why/what things changed with RxJava2, as explained by an actual demigod. This was the one that really made it first click for me.
- [Thought process behind the 2.0 design](https://github.com/ReactiveX/RxJava/issues/2787) for the truly loyal
- [Ep 11 of The Context ](https://github.com/artem-zinnatullin/TheContext-Podcast/blob/master/show_notes/Episode_11.md) —  by my friends Hannes and Artem :)

我们应该可以从中得到一个重要的改变：

## 依赖改了

搜索：

```
compile "io.reactivex:rxjava:${rxJavaVersion}"
compile "io.reactivex:rxandroid:${rxAndroidVersion}"

compile "com.jakewharton.rxbinding:rxbinding:${rxBindingsVersion}"
compile "com.squareup.retrofit2:adapter-rxjava:${retrofit2Version}"
```

换成:

```
compile "io.reactivex.rxjava2:rxjava:${rxJavaVersion}"
compile "io.reactivex.rxjava2:rxandroid:${rxAndroidVersion}"
 
compile "com.jakewharton.rxbinding2:rxbinding:${rxBindingsVersion}"
compile "com.squareup.retrofit2:adapter-rxjava2:${retrofit2Version}"
```

在你的gradle里的小改变（“2”后缀）

实际的类被移动到了一个新的包 *io.reactivex* (vs *rx*)里. 所以你必须修改这些import语句。

理论上你也可同时使用 Rx1 和Rx2 ，但这是个坏主意，因为基本数据结构如 Observables 对于流的处理不同 (背压backpressure). 在这个过渡期间，你必须记住这行为差异，这可能是个梦魇. 并且如果你碰巧同时使用了Rx1 和 Rx2 Observables 你必须谨慎的明确指定他们的包名 (`rx.Observable` or `io.reactivex.Observable`). 这很容易混淆和搞错。

> Bite the bullet and migrate it all in one shot.
>
> 快刀斩乱麻

另一个超级重要的变化：

Observable -> Flowable

```
搜索 : `import rx.Observable;`
替换 : `import io.reactivex.Flowable;`
```

- Flowable 是新的Observable. 简单的说 - 它是能支持背压的反应式基类。
- 现在开始使用Flowable ，**不是** Observable. 默认用Flowable .
- Observables 仍然可以用, 但除非你真的理解了背压(backpressure), 否则你可能再也不想用他们了。

> Flowable = Observable + backpressure handling
>
> Flowable = Observable + 背压（backpressure ）处理

# 注意 “Publisher”s:

记得`Publisher`吗？它基本上是生成事件的任何事件的“反应流”接口 (*如果对这个没有印象，重读上面的 Reactive Streams spec 片段*).

`Flowable` 实现`Publisher`. 这是我们新的默认的反应式基类和实现反应流规范 1 <-> 1. Think of of Flowable as primero uno “Publisher” (这也是为啥我推荐默认使用Flowable  的原因).

另一个反应式基类是 Publishers 包括 Observable, Single, Completable 和 Maybe. 但他们没有直接实现 `Publisher` 接口.

**为虾米?**

恩，其他基类现在被认为是具有与Rx有关的专门行为的“Rx”特定结构。而这些不一定是您在“反应流”规范中找到的概念。

我们可以看一下实际的接口声明，这将会很清楚的。

# 注意 “Subscriber”s:

如果 `Publisher` 是“反应流”事件制造者, `Subscriber` 是反应流“监听者” (将这些条款牢固地固定在我们的头上是非常有帮助的，因此不断重复).

Looking at the actual interface code declaration should offer more clarity to the above two sections.

查看实际的接口代码声明应该能够让上述两个部分更加清晰一点。

```
// Reactive Streams spec 

// Flowable implements Publisher

interface Publisher<T> {
    void subscribe(Subscriber<? super T> s);
}
```

如前所述, `Publisher` 和`Subscriber` 是反应流规范的一部分. Flowable -现在是实现`Publisher`.的反应基类。到目前为止,一切都好。

但是其他的反应性基类，如Observable和Single，我们如何来爱和使用?

在发布方面, 其他事件制造者实现了一个类似的接口，替代实现标准的`Publisher`接口。

```
// RxJava specific constructs

// Observable implements "ObservableSource"
interface ObservableSource<T> {
    void subscribe(Observer<? super T> observer);
    // notice "Observer" here vs the standard "Subscriber"
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

注意: 其他反应式基类 (`Observable`, `Single` 等)不是使用标准的`Subscriber` (反应流标准)，现在符合”专门的“Rx 明确的`Subscriber` 或者事件监听器叫“Observer”s.

这是第一部分，[下一部分](http://blog.kaush.co/2017/06/21/rxjava-1-rxjava-2-disposing-subscriptions/),，我们将讨论 **处理订阅**。
