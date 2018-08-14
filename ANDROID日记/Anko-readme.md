<img src="doc/logo.png" alt="Anko logo" height="101" width="220" />

Anko是一个 让Android应用开发更快和更简单的[Kotlin](http://www.kotlinlang.org/) 库. 这让你的代码干净和易读,并且让你忘记AndroidSDK的粗糙。

Anko包含几个部分:

* *Anko Commons*: 包含intents, dialogs, logging等的helpers 轻量级库;
* *Anko Layouts*: 快速和类型安全的写动态Android layouts;
* *Anko SQLite*: 一个查询DSL 和解析的 Android SQLite;
* *Anko Coroutines*: 基于 [kotlinx.coroutines](https://github.com/Kotlin/kotlinx.coroutines) library的公用工具。

## Anko Commons

*Anko Commons* 是Kotlin Android开发者的  一个"工具箱".库包含大量的Android SDK的helpers，包括但不止于此:

* Intents ([wiki](https://github.com/Kotlin/anko/wiki/Anko-Commons-–-Intents));
* Dialogs and toasts ([wiki](https://github.com/Kotlin/anko/wiki/Anko-Commons-–-Dialogs));
* Logging ([wiki](https://github.com/Kotlin/anko/wiki/Anko-Commons-–-Logging));
* Resources and dimensions ([wiki](https://github.com/Kotlin/anko/wiki/Anko-Commons-–-Misc)).

## Anko Layouts ([wiki](https://github.com/Kotlin/anko/wiki/Anko-Layouts))

*Anko Layouts*s是一个DSL用于写动态Android layouts; 这是个用Anko DSL编写的简单的UI：

```kotlin
verticalLayout {
    val name = editText()
    button("Say Hello") {
        onClick { toast("Hello, ${name.text}!") }
    }
}
```

上面的代码创建了一个button在 `LinearLayout`里面，并且带有一个 `OnClickListener`. 而且, `onClick` 接收一个 [`suspend` lambda](http://kotlinlang.org/docs/reference/coroutines.html), 所以你可以直接在listener中写你的异步代码。

注意，这是个完整的layout 代码.不需要XML!

<img src="doc/helloworld.png" alt="Hello world" height="90" width="373" />

也有一个[plugin](https://github.com/Kotlin/anko/wiki/Anko-Layouts#anko-support-plugin) 给Android Studio支持预览Anko DSL layouts.

## Anko SQLite ([wiki](https://github.com/Kotlin/anko/wiki/Anko-SQLite))

你是否还在无力的使用Android cursors解析 SQLite 查询结果? *Anko SQLite* 提供大量的helpers来简化SQLite数据库.

比如，这个为如何在一个用户列表中获取John的信息：

```kotlin
fun getUsers(db: ManagedSQLiteOpenHelper): List<User> = db.use {
    db.select("Users")
            .whereSimple("family_name = ?", "John")
            .doExec()
            .parseList(UserParser)
}
```

## Anko Coroutines ([wiki](https://github.com/Kotlin/anko/wiki/Anko-Coroutines))

*Anko Coroutines* 是基于[`kotlinx.coroutines`](https://github.com/kotlin/kotlinx.coroutines) 库和提供:

* [`bg()`](https://github.com/Kotlin/anko/wiki/Anko-Coroutines#bg) 函数在一个普通池执行你的代码.
* [`asReference()`](https://github.com/Kotlin/anko/wiki/Anko-Coroutines#asreference) 函数创建一个弱引用包装.默认的, 一个 coroutine holds引用去抓取对象直到它完成或者取消。如果你的异步框架不支持取消，你在异步块中的值就会泄漏。 `asReference()`保护你避免这个.

## 使用Anko

### Gradle-based project

Anko有一个元依赖，这个会一次性将添加所有的特性 (包括 Commons, Layouts, SQLite)到你的项目:

```gradle
dependencies {
    compile "org.jetbrains.anko:anko:$anko_version"
}
```
确认你有在你的项目层的gradle设置 ```$anko_version``` :

```
ext.anko_version='0.10.3'
```

如果你只需要一些其他特性，你可以随便用Anko中的部分：

```gradle
dependencies {
    // Anko Commons
    compile "org.jetbrains.anko:anko-commons:$anko_version"

    // Anko Layouts
    compile "org.jetbrains.anko:anko-sdk25:$anko_version" // sdk15, sdk19, sdk21, sdk23 are also available
    compile "org.jetbrains.anko:anko-appcompat-v7:$anko_version"

    // Coroutine listeners for Anko Layouts
    compile "org.jetbrains.anko:anko-sdk25-coroutines:$anko_version"
    compile "org.jetbrains.anko:anko-appcompat-v7-coroutines:$anko_version"

    // Anko SQLite
    compile "org.jetbrains.anko:anko-sqlite:$anko_version"
}
```

这还有些关于Android支持库的:

```gradle
dependencies {
    // Appcompat-v7 (only Anko Commons)
    compile "org.jetbrains.anko:anko-appcompat-v7-commons:$anko_version"

    // Appcompat-v7 (Anko Layouts)
    compile "org.jetbrains.anko:anko-appcompat-v7:$anko_version"
    compile "org.jetbrains.anko:anko-coroutines:$anko_version"

    // CardView-v7
    compile "org.jetbrains.anko:anko-cardview-v7:$anko_version"

    // Design
    compile "org.jetbrains.anko:anko-design:$anko_version"
    compile "org.jetbrains.anko:anko-design-coroutines:$anko_version"

    // GridLayout-v7
    compile "org.jetbrains.anko:anko-gridlayout-v7:$anko_version"

    // Percent
    compile "org.jetbrains.anko:anko-percent:$anko_version"

    // RecyclerView-v7
    compile "org.jetbrains.anko:anko-recyclerview-v7:$anko_version"
    compile "org.jetbrains.anko:anko-recyclerview-v7-coroutines:$anko_version"

    // Support-v4 (only Anko Commons)
    compile "org.jetbrains.anko:anko-support-v4-commons:$anko_version"

    // Support-v4 (Anko Layouts)
    compile "org.jetbrains.anko:anko-support-v4:$anko_version"
}
```

这有一个demo [example project](https://github.com/kotlin/anko-example)展示如何include Anko库到你的Android Gradle project.

### IntelliJ IDEA project

如果你的project不是基于Gradle的, 只要使用 [jcenter repository](https://jcenter.bintray.com/org/jetbrains/anko/) 的JARs 依赖就好了.
