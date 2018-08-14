翻译自：https://gofore.com/en/ode-to-kotlin/

我讨厌用Java工作。真的。它总让我有种无力感和无聊。然而我还是要在每个我做的项目用到它-这个或那个。我知道许多公司使用Java的原因，但是基于与我作为程序员的完全不同的原因。在这篇文章，我将告诉你为虾米我这么想，和介绍一个特别流弊的，可替代Java的语言，-》Kotlin，根据我在Kotlin从普通Kotlin到Spring 5 WebFlux和Android的项目的经验。我希望这篇文章描述的东西能鼓励你考虑下Kotlin来替代你的所爱的Java。

## 我在Java上遇到的坑

描述我讨厌Java的每件事可以写一箩筐。在这篇文章，我主要讲下我在开发web时最常遇到的部分。

Java最大的问题是非人性化特性，特别是周围的生态系统。让我们来看看几个在做web开发时经常写的代码例子。首先是POJOs（简单老Java对象），需要建模应用的数据结构。下为符合习惯的java代码：

```java
class Person {
  private String name;
  private Integer age;

  public Person(String name, Integer age) {
    this.name = name;
    this.age = age;
  }

  public String getName() {
    return name;
  }
  public setName(String name) {
    this.name = name;
  }

  public Integer getAge() {
    return age;
  }
  public setAge(Integer age) {
    this.age = age;
  }
}
```

这个模型有20行代码，其中竟然没有一半可用。让我们看下同样的模型，Kotlin的写法：

```kotlin
data class Person(var name: String, var age: Int)
```

是不是看起来很简单。那如何使用呢？我们来声明一个这种model类型的数组，首先Java：

```java
final List<Person> persons = new ArrayList<>(Arrays.asList(new Person("John", 36), new Person("Mary", 29)));
```

然后Kotlin:

```
val persons: MutableList<Person> = mutableListOf(Person("John", 36), Person("Mary", 29))
```

好的，那至少在我看来，即使是创建对象，看起来也是Kotlin比较紧凑。

Kotlin是一个现代编程语言中优秀的例子，对开发者友好的编程语言。Kotlin不断发布社区最需要功能的新版本。它经常发布小批而不是像Java那样X年后发布个大的更新。实践中，Java的最新发布（Java 8）是2014年，而Kotlin已经发布一次（1.1）和大量的小批更新，预览版和发布候选版本今年至少在年底前会发布1.2版本。

一般来说，我相信代码越少，越好维护。人们可能认为，由于你必须编写少量代码来实现同样的效果，那你必须跳过一些重要的东西，或者隐含的东西（通常叫魔法），需要明确写出来才能清楚。但事实并不是这样。光看下上面的例子，他们和Java代码相比，并不缺什么，但他们自从在真正要实现上少了些噪音，显然更好写和读。

Java开发也过于复杂。我根本不能将所有的Java EE东西塞进我脑子里。我也一点都不想尝试，因为我知道这是行不通的路。使用如Spring Boot这样的解决方案，最近成为做web服务的标准，已经有了很大的进步。尽管如此，Java程序员做的该解决方案往往遵循与过去相同的强化实践。这不是轻易可以改变的东西。难怪Spring 5的WebFlux内置了Kotlin的支持。

在我眼里，Java开发者是一个完全被锁在Java中完成事情的开发者，这显然是他/她唯一可接受的方式。他们依赖XML，在我看来XML和Java有同样的问题。本质上，它用起来一点都不人性化。Java开发者，在我的经验中，倾向于相信其他语言只是宠物项目的某种玩具语言，并无法构建他们需要构建的复杂的企业应用程序（不管啥意思）。这些开发者总是认为他们的应用是如此大和复杂，以至于它只能用世界上唯一的企业级编程语言— Java 来解决。通常构建的服务实际上是相当简单的并且可以使用某种更合适的工具如Node.js实现。然而，唯一有能力的语言被认为是Java。

好的，这相当刻薄，并且不能准确的描述许多Java开发者，但是你懂的，对吧？不过，俗话说"歹竹出好笋"（闽南语）。对于Java也是如此，比如Java最流弊的部分是下一节要讲的JVM。Java周围的生态系统也是不错的。

## 那Kotlin怎么样?

首先，让我告诉你Kotlin是虾米吧。 [Kotlin](https://kotlinlang.org/)是[JetBrains](https://www.jetbrains.com/) (IntelliJ IDEA 和其他软件项目相关的IDEs 背后的公司）写的一个现代编程语言。它继续列出了基于JVM的语言，如 [Groovy](https://en.wikipedia.org/wiki/Groovy_(programming_language)), [Scala](https://en.wikipedia.org/wiki/Scala_(programming_language)) 和 [Clojure](https://en.wikipedia.org/wiki/Clojure).Kotlin，在2011年发布，不仅运行在JVM之上，而且可以与Java[完全互操作](https://kotlinlang.org/docs/reference/java-interop.html) 。这意味着该公司可以逐步迁移现有的代码库到Kotlin，无需额外的麻烦，仍可以使用Java周围的大型生态系统。Kotlin也可以用来做Android开发而没有性能问题。它还支持编译Node.js或浏览器应用程序的JavaScript。

但造成使用Kotlin比用Java更人性化的原因是虾米呢？Kotlin旨在尽可能简洁，并消除在Java上编写的应用程序中发现大量的样板代码。Kotlin的[主页](https://kotlinlang.org/) 上给了大量的例子，在使用Kotlin的所有最佳使用的例子。自从我们早就提到的POJOs，让我们从之前用到的例子开始：

```kotlin
data class Person(var name: String, var age: Int)
```

哇哦，太简洁了。那对于setters和getters呢（作为Java开发者会问），当我需要得到每个该死的属性的时候，尽管他们不包含任何逻辑。嗯，当我们使用`val` （*value*, 常量）的时候，Kotlin已经为我们自动生成getters了。如果我们使用var（变量），setter也将被生成。我不会亲自发现getter和setter的价值是非常好的，我很乐意使用公共字段。是的，我熟悉使用私有领域和getter / setter的想法，但是我从来没有在getter和setter中做任何特殊的操作，所以我很乐意在实际需要时重构公共字段对getter / setter的直接用法。但是现在我不会去讨论这个讨论，因为这篇文章的范围是不合适的。

另一个相当重要的特性，许多语言（如 [Swift](https://en.wikipedia.org/wiki/Swift_programming_language)）已经实现了，由于java等语言的空指针安全问题是[Optionals](https://en.wikipedia.org/wiki/Option_type)的概念。是的，[Optionals](https://en.wikipedia.org/wiki/Option_type)最后在Java8实现了，但是它太晚了。Kotlin使得语言的[null-safety](https://kotlinlang.org/docs/reference/null-safety.html)主要特征得以实现。以下是可选代码的示例：

这会造成编译错误：

```kotlin
val myString: String = "foo"
myString = null
```

当我们明确的允许空值，这就会编译通过：

```kotlin
val myString: String? = "foo" // Non-null value
myString = null
```

同样的，如果我们有可能为空值，我们不能只这样调用方法：

```kotlin
val l = myString.length // // error: variable 'myString' can be null
```

我们需要明确安全的调用`?.` 而不是 `.`。这样，如果操作符的左侧为空，则结果为null。

你可能仍会得到`NullPointerException`异常，或者一些外部Java抛出的，但这些是特殊情况，并不会在Kotlin中发生。

Java的一个非常烦人的特征一直是它只支持面向对象编程。即使是基本的lambda功能也不可用，在Java 8之前.Kotlin提供了基本的OOP功能，同时为功能编程提供了极大的支持，其功能如一等公民和鼓励使用不变性。

除了这里突出强调的功能外，Kotlin还有很多功能与Java相比有优势。这些东西包括更好的语法，新颖的使用协同程序的异步编码和IntelliJ IDEA的很好的工具支持。最后一个很好的例子是自动将Java代码转换为Kotlin的选项。已经使用了很多，已被证明这做的相当好。

## 结论

技术选择总是至少与某些技术的成本和风险进行某种评估。经常听到的关注是团队将如何适应新技术的速度。由于Kotlin与Java建立在同一处所，Java程序员很容易适应。基本类型是相同的，代码看起来是一样的。此外，围绕Java构建的整个生态系统也很容易在Kotlin项目中使用。这些事实结合了从Java到Kotlin的自动转换，以了解Kotlin将会如何看待Kotlin，从而使Java开发人员更容易学习Kotlin。

第二个问题涉及对技术的未来预期支持。 Kotlin由JetBrains本身支持和使用，JetBrains本身是软件相关工具的关键角色之一。目前没理由期望他们能够长期停止发展的脚步。它也被许多知名公司使用，列在Kotlin的主页上。 Kotlin也被Google推荐用于Android开发。

Kotlin的Java互操作性也是一个非常重要的方面，因为它可以让您使用所有的Java库和框架。此外，还可以不仅将Java代码转换为Kotlin，而且反之亦然（尽管工具没有明确支持），以防您想要摆脱Kotlin。

作为一个结论，Kotlin采取了Java的最好的部分，并结合了现代语言与伟大的工具。其高级功能允许您编写简洁干净的代码，而不需要在其周围编写不必要的样板代码。还要继续关注即将发布的Spring 5即将发布的帖子，特别是其新的WebFlux模块。
