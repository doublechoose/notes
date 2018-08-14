转自：https://code.tutsplus.com/tutorials/introduction-to-android-architecture--cms-28749 


Android自从2005年诞生，在这12年中获得了巨大的成功，成为安装次数最多移动操作系统。在这段时间发布了14个不同版本的系统，随着android逐渐的成熟，却一直忽略了android平台的一个领域：一个标准的架构模式，有效处理android平台的特性和让每个开发者很容易理解和采纳。

迟来的总比没有好，在最新的 Google I/O大会上, Android 团队终于决定讲下这个问题，和响应全世界的开发者的反馈，宣布一个android应用架构和提供实现它的构建模块的官方推荐方案：新的架构组件。不仅如此，他们不仅做到了，并且不违反我们所知道和热爱的系统开发性。

![Architecture Components](http://upload-images.jianshu.io/upload_images/3509189-d590c73073c8ab46.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

在这片教程中，我们将探究Android团队在 Google I/O上提出的标准架构，和了解在新架构组件中的主要元素：: `Lifecycle`, `ViewModel`, `LifeData`, 和 `Room`.我们不会花太多时间在代码上，而是专注在这些主题里的概念和逻辑。我们也会看下一些简短的片段，他们都是用Kotlin编写的，一个现在被android官方支持的神奇的语言。

## 1. Android 究竟少了什么？

如果你是个刚入门的开发者，很有可能你不太知道我在讲什么。毕竟，应用架构一开始就是一个晦涩难懂的话题。但相信我，过不久，你将会了解到它的重要性！当一个应用成长和变得更加复杂，它的架构将越来越重要。好不夸张的说，它可以成为你工作的福分，或者你的梦魇。

### 应用架构

大概的说，一个应用架构是开发开始之前就需要进行的统一规划，这个规划提供如何组织和绑定不同应用组件的蓝图，它提供在开发过程中应该被遵守的方针，和强制一些牺牲（一般关于更多的类和模板），最后将帮助你构造一个更容易测试，更容易扩展，更容易维护的程序。

> 软件应用架构是定义一个架构解决方案，集合所有技术和操作要求，完善公共的质量属性如性能，安全和易管理性的过程。它涉及一系列基于一个大范围因素的决定，并且每个决定都可能影响到质量，性能，可维护性，应用总体的成功。

> — 微软软件架构和设计指导

好的架构需要考虑许多因素，特别是系统特性和限制。现在有许多不同的架构解决方案，这些方案都有被赞同的，也有被反对的。然而在所有的眼光中一些[关键概念](https://en.wikipedia.org/wiki/Software_architecture#Characteristic)是共同的。

### 过去的错误

直到最近的 Google I/O,在此之前android系统并没有为应用开发推荐任何确切的架构。这意味着你完全自由的使用任意模型：MVP，MVC，MVPP，或者一点模式都不用。最重要的是，Android框架甚至没有为系统本身的问题提供原生的解决方案，尤其是组件的生命周期。

![Great news at the Google IO 2017](http://upload-images.jianshu.io/upload_images/3509189-e64774f1bfc05793.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

因此，如果你想在你的应用上采用 Model View Presenter模式，你需要从头开始提供解决方案，写一堆模板代码，或者采用一个第三方库，因缺乏标准，创造了一堆堆积烂代码，难以维护和测试的应用。

就像我说的，这个情况已经被骂了很多年了，实际上，我最近在我的 [如何在Android上应用 Model View Presenter模式](https://code.tutsplus.com/series/how-to-adopt-model-view-presenter-on-android--cms-1012)系列中描述了这个问题和如何解决它。但是重点是过了12年，Android团队终于决定听到了我们的抱怨，并且帮助我们解决这个问题。

## 2. Android 架构

新的 [Android 架构指南](https://developer.android.com/topic/libraries/architecture/guide.html)定义了一些关键原则：一个优秀的Android应用应该具有的和一个开发者创建一个好应用的安全的路。然而，该指南明确指出，提出的路线并不是强制性的，最终是否采纳由开发者决定，决定采纳何种架构。

根据指南，一个优秀的Android应用应该提供一个坚固的解耦和模型驱动UI，任何不能处理UI或者操作系统交互的代码不应该放在Activity或者Fragment上，因为分的越清楚，将帮助你更好的避免生命周期相关问题。毕竟，系统任何时候都可以摧毁Activities或者Fragments，而且，数据应该在models中处理，独立于UI，因此避免了生命周期问题。

### 新的推荐架构

Android推荐的架构不能简单的贴上我们之前了解的标签。它像一个 Model View Controller模式，但是它是如此贴合系统架构以至于难以用已知的约定习俗来为每个元素贴上标签，这不确切，但是，重要的是它依赖心的架构组件来创造解耦，并且完美的可测性和易维护性。更爽的是，它很容易实现。

为了理解Android团队是怎么打算的，我们有必要理解架构组件的所有的元素，因为他们要为了我们做重活。有四个组件，每个都有确切的角色： **Room**, **ViewModel **和 **Lifecycle**，**LiveData**， 他们都有自己的职责，并且一起配合工作来创造一个稳固的架构。让我们简单的看下架构图来更好的理解。

![Android Architecture](http://upload-images.jianshu.io/upload_images/3509189-ae91e3196a0e673f.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以看到，我们有三个主要元素，每个有它自己的职责。

1. **Activity** 和**Fragment** 代表 **View** 层,不处理业务逻辑和复杂操作。它只配置view，处理用户交互，和最重要的是，观察和展示从 **ViewModel**中获取的 **LiveData** 。
2.  **ViewModel** 自动的观察view的 **Lifecycle** ,在配置改变和其他Android生命周期事件发生时，保存数据一致。view对它请求数据，它从 **Repository**获取数据，由可观察的 **LiveData**提供。重点理解：`ViewModel`从不直接引用 `View`，更新数据都是使用**LiveData**.
3.  **Repository**不是一个特别Android组件，它是一个简单类，没有特殊实现，职责为从所有可行的资源中获取数据，从一个数据库到web服务。它处理所有的数据，逐渐的将数据转化为可观察的 **LiveData**，并使其可用于 **ViewModel**.
4.  **Room**数据库是一个帮助处理数据库的SQLite 映像库，它自动的写一堆模板代码，运行时检查错误，更爽的是它能直接返回查询的可观察 **LiveData**.

我相信你已经注意到了我们讲了很多可观察。观察者模式是 **LiveData** 元素和 **Lifecycle** 组件的基础之一。这个模式允许一个对象通知一堆观察者关于它的状态和数据的改变。因此，当一个Activity观察一个 `LiveData`,这个数据收到任意修改，它（Activity）都将收到更新。

另一个Android推荐是使用依赖注入系统来统一它的架构。就像Google的 [Dagger 2](https://google.github.io/dagger/) 或者使用 [Service Locator](https://en.wikipedia.org/wiki/Service_locator_pattern)模式（比DI简单，但没有它的许多优点）。我们不会在这个教程中介绍DI或者Service Locator，但是 Envato Tuts+有一些出色的教程。然而请注意，使用Dagger 2和Android组件有一些特殊之处，这将在本系列的第二部分中解释。

- [![img](http://upload-images.jianshu.io/upload_images/3509189-84add6e1cabdc0f0.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)ANDROID SDKDependency Injection With Dagger 2 on AndroidKerry Perez Huanca](http://code.tutsplus.com/tutorials/dependency-injection-with-dagger-2-on-android--cms-23345)

## 3. 架构组件

我们必须深入到新组件的各个方面，才能真的理解和适配这个架构模式。然而我们不会在这篇深入到所有的细节。由于每个组件的复杂度，在这个教程中，我们只讲每个组件的总体概念和看些简短的代码片段。我们将试着覆盖足够的基础来展示组件，并让你开始工作。别害怕，因为将来这个系列将挖的更深和覆盖所有架构组件的特性。



### Lifecycle-Aware Components

大多数的Android应用组件都有生命周期，由系统本身管理。直到最近,它还是由开发者来监控组件的状态，并在适当的时候进行相应的初始化和结束工作。然而，很容易在这种类型的操作上感到困惑和犯错。但是 `android.arch.lifecycle` 包，改变了一切（此处应有掌声）。

现在， Activities 和Fragments有一个 `Lifecycle`对象，能被`LifecycleObserver`类观察，如一个 `ViewModel` 或者任意实现这个接口的对象。这意味着观察者将收到关于它观察的对象状态改变的更新，如当一个Activity暂停的时候或者它开始的时候。它也能检查被观察对象的当前状态。因此它更容易处理必须考虑框架生命周期的操作。

![LifecycleObserver reacts to LifecycleEvents](http://upload-images.jianshu.io/upload_images/3509189-3f0e1787cb594ac1.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

现在，为了创建一个Activity或者Fragment符合这个新的标准，你必须要继承一个 [`LifecycleActivity`](https://developer.android.com/reference/android/arch/lifecycle/LifecycleActivity.html) 或者[`LifecycleFragment`](https://developer.android.com/reference/android/arch/lifecycle/LifecycleFragment.html)。然而，这有可能不是一直需要的,因为Android团队的模板是将这些新工具与框架完全集成。

 `LifecycleObserver` 接收`Lifecycle` 事件，然后通过注解响应。不需要覆盖方法。



###  `LiveData` 组件

 `LiveData`组件是一个数据持有者，包含了可以被观察的值。考虑到观察者在 `LiveData`实例化时，提供了生命周期， `LiveData`将根据`Lifecycle` 来工作。如果观察者的 `Lifecycle` 是 `STARTED` 或者`RESUMED`，观察者是活跃的，否则是不活跃的。

`LiveData`知道当数据改变时和如果观察者是活跃的，那应该接收更新。 `LiveData`的另一个好玩的特性是它能移除观察者，当它在 `Lifecycle.State.DESTROYED`状态时。当被Activities and Fragments观察时，能避免内存泄漏。

![LiveData value updating process](http://upload-images.jianshu.io/upload_images/3509189-8352719d6ce46104.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

 `LiveData`必须实现 `onActive` and `onInactive`方法。

为了观察一个 `LiveData`组件，你必须调用 `observer(LifecycleOwner, Observer<T>)`.

###  `ViewModel` 组件

 `ViewModel`是新的架构组件最重要的类之一，被设计来联系数据和UI。维持它的全部，如屏幕旋转。 `ViewModel`可以和 `Repository`打交道，从它那获取`LiveData`,然后使liveData能被View观察。 `ViewModel`在配置改变后不需要重新调用`Repository`，从而优化了代码。

![ViewModel is tight to UI Lifecycle](http://upload-images.jianshu.io/upload_images/3509189-f371b07067686aa1.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

为了创建一个view model，继承 `ViewModel` class.

为了联结view，你可以调用 `ViewProviders.of(Activity|Fragment).get(ViewModel::class)`,这个工厂方法将返回一个新的`ViewModel`实例或者获取保留的一个，适当的时候。

###  `Room` 组件

Android一开始就支持SQLite ，然而，为了让他工作，需要写大量的样板代码。而且SQLite 不保存 POJOs (plain-old Java objects)，而且在编译时不检查。于是 `Room`来解决这些问题了。它是一个SQLite 映像库，能保存POJO，直接转化为对象，在运行时检查错误。而且从查询结果中制造 `LiveData`.`Room`是一个有一些带有有趣的Android扩展的  [Object Relational Mapping](https://en.wikipedia.org/wiki/Object-relational_mapping)库。

直到现在，你能用其他ORMAndroid库做大部分的事情。然而他们都不是官方支持的，并且最重要的是他们不能制造出 `LifeData`. `Room`库在Android架构的存储层完美适用。

为了创建一个 `Room`数据库，你将需要一个 `@Entity`来固定，可以是任何 Java POJO，`@Dao` 接口来制造查询和输入输出操作， `@Database` 抽象类 必须继承`RoomDatabase`.



### 添加架构组件到你的项目

现在，为了使用新的架构组件，你需要添加Google repository 到你的`build.gradle`文件，详情请看 [官方指南](https://developer.android.com/topic/libraries/architecture/adding-components.html).

## 结论

可以看到，Android提供的标准架构涉及大量的概念。先不要期望完全理解这个话题。毕竟我们很少介绍这个主题。但你现在有足够的知识去理解这架构背后的逻辑和不同架构组件扮演的角色。

我们谈论了Android架构和它的组件，然而关于组件详细实现和一些扩展，如 `Repository`类和 Dagger 2 系统不能覆盖到，我们将在下一次推送中探索这些主题。

See you soon!
