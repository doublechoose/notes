翻译自[这里]（https://github.com/Kotlin/anko/wiki/Anko-Layouts#why-anko-layouts）
## 内容

- 为虾米用Anko Layouts?
  - [Why a DSL?](https://github.com/Kotlin/anko/wiki/Anko-Layouts#why-a-dsl)
  - [Supporting existing code](https://github.com/Kotlin/anko/wiki/Anko-Layouts#supporting-existing-code)
  - [How it works](https://github.com/Kotlin/anko/wiki/Anko-Layouts#how-it-works)
  - [Is it extensible?](https://github.com/Kotlin/anko/wiki/Anko-Layouts#is-it-extensible)
- [Using Anko Layouts in your project](https://github.com/Kotlin/anko/wiki/Anko-Layouts#using-anko-layouts-in-your-project)
- Understanding Anko
  - [Basics](https://github.com/Kotlin/anko/wiki/Anko-Layouts#basics)
  - [AnkoComponent](https://github.com/Kotlin/anko/wiki/Anko-Layouts#ankocomponent)
  - [Helper blocks](https://github.com/Kotlin/anko/wiki/Anko-Layouts#helper-blocks)
  - [Themed blocks](https://github.com/Kotlin/anko/wiki/Anko-Layouts#themed-blocks)
  - [Layouts and LayoutParams](https://github.com/Kotlin/anko/wiki/Anko-Layouts#layouts-and-layoutparams)
  - [Listeners](https://github.com/Kotlin/anko/wiki/Anko-Layouts#listeners)
  - [Custom coroutine context](https://github.com/Kotlin/anko/wiki/Anko-Layouts#custom-coroutine-context)
  - [Using resource identifiers](https://github.com/Kotlin/anko/wiki/Anko-Layouts#using-resource-identifiers)
  - [Instance shorthand notation](https://github.com/Kotlin/anko/wiki/Anko-Layouts#instance-shorthand-notation)
  - [UI wrapper](https://github.com/Kotlin/anko/wiki/Anko-Layouts#ui-wrapper)
  - [Include tag](https://github.com/Kotlin/anko/wiki/Anko-Layouts#include-tag)
- Anko Support Plugin
  - [Installing Anko Support plugin](https://github.com/Kotlin/anko/wiki/Anko-Layouts#installing-anko-support-plugin)
  - [Using the plugin](https://github.com/Kotlin/anko/wiki/Anko-Layouts#using-the-plugin)
  - [XML to DSL Converter](https://github.com/Kotlin/anko/wiki/Anko-Layouts#xml-to-dsl-converter)

## 为虾米用Anko Layouts??

### 为虾米用DSL?

Android的UI默认使用XML编写，有以下不方便：

- 不是类型安全的;
- 不是null-safe;
- 强迫你对每个layout编写几乎相同的代码;
- 在设备上解析XML费电费CPU;
- 最惨的是代码不可复用

当你使用代码创建UI，这很难搞，因为代码看起来很丑，并且难以维护。这里给了简洁的kotlin版本：(如果用java写，更长):

```
val act = this
val layout = LinearLayout(act)
layout.orientation = LinearLayout.VERTICAL
val name = EditText(act)
val button = Button(act)
button.text = "Say Hello"
button.setOnClickListener {
    Toast.makeText(act, "Hello, ${name.text}!", Toast.LENGTH_SHORT).show()
}
layout.addView(name)
layout.addView(button)
```

DSL让同样的逻辑可读性更强，更容易编写并且没有运行时出错的毛病。如下:

```
verticalLayout {
    val name = editText()
    button("Say Hello") {
        onClick { toast("Hello, ${name.text}!") }
    }
}
```

看 `onClick()` 支持coroutines (接受挂起lambda) ，这样，你可以不用详写`async(UI)`调用就能编写你的异步代码.

### 支持已存在的代码

你不必用Anko重写所有你的UI.你可以保持你用Java写的旧类.此外，如果你由于某种原因，仍想（或者被逼）写一个kotlin风格的activity类和渲染一个XML布局 ，你可以使用View properties, 这会变得更简单:

```
// Same as findViewById() but simpler to use
val name = find<TextView>(R.id.name)
name.hint = "Enter your name"
name.onClick { /*do something*/ }
```

通过使用[Kotlin Android Extensions](https://kotlinlang.org/docs/tutorials/android-plugin.html).你可以让你的代码变得更简洁。

### 怎么实现的

这里没有 ![:tophat:](http://upload-images.jianshu.io/upload_images/3509189-002d82907e879ca2?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240). Anko由一些Kotlin的 [扩展函数和属性](http://kotlinlang.org/docs/reference/extensions.html) 装进 *type-safe builders* , 又叫 [under Type Safe Builders](http://kotlinlang.org/docs/reference/type-safe-builders.html)组成.

手写这些稍微冗长的拓展后，他们会自动的使用Android SDK生成源码。

### 它可拓展吗?

三个字: **yes**.

比如，你想在DSL中使用 `MapView` . 那只要在任意的可以import的kotlin文件写这几句:

```
inline fun ViewManager.mapView() = mapView(theme = 0) {}

inline fun ViewManager.mapView(init: MapView.() -> Unit): MapView {
    return ankoView({ MapView(it) }, theme = 0, init = init)
}
```

`{ MapView(it) }` 是一个你的自定义View的工厂函数.它接受`Context` 实例.

现在你可以这样写了:

```
frameLayout {
    val mapView = mapView().lparams(width = matchParent)
}
```

如果你想让你的用户应用一个自定义的theme，也这样写:

```
inline fun ViewManager.mapView(theme: Int = 0) = mapView(theme) {}

inline fun ViewManager.mapView(theme: Int = 0, init: MapView.() -> Unit): MapView {
    return ankoView({ MapView(it) }, theme, init)
}
```

## 在你的项目中使用 Anko Layouts 

包含这些依赖库:

```
dependencies {
    // Anko Layouts
    compile "org.jetbrains.anko:anko-sdk25:$anko_version" // sdk15, sdk19, sdk21, sdk23 are also available
    compile "org.jetbrains.anko:anko-appcompat-v7:$anko_version"

    // Coroutine listeners for Anko Layouts
    compile "org.jetbrains.anko:anko-sdk25-coroutines:$anko_version"
    compile "org.jetbrains.anko:anko-appcompat-v7-coroutines:$anko_version"
}
```

详情请看 [Gradle-based project](https://github.com/Kotlin/anko#gradle-based-project) 

## 理解Anko

### 基础

在Anko中,你不需要继承任何指定的类: 只要用标准的`Activity`, `Fragment`, `FragmentActivity` 或者你要的那个.

首先, import `org.jetbrains.anko.*` ，在你的类中使用Anko Layouts DSL .

DSL 在`onCreate()`可用:

```
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    
    verticalLayout {
        padding = dip(30)
        editText {
            hint = "Name"
            textSize = 24f
        }
        editText {
            hint = "Password"
            textSize = 24f
        }
        button("Login") {
            textSize = 26f
        }
    }
}
```

 ![:penguin:](http://upload-images.jianshu.io/upload_images/3509189-cd751bb5759e980c?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) *这里没有明确调用setContentView(R.layout.something): Anko 自动的为Activities（只为Acitivitys）调用sets content views .* 


`hint` 和`textSize` 是[合成拓展属性](https://kotlinlang.org/docs/reference/java-interop.html#getters-and-setters) 对应JavaBean-style 的 getters 和 setters, `padding` is Anko的 [拓展属性](http://kotlinlang.org/docs/reference/extensions.html#extension-properties) . 这些属性对大多数的`View`都有，允许你编写 `text = "Some text"` 替代`setText("Some text")`.

`verticalLayout` (`LinearLayout` 但已经加上`LinearLayout.VERTICAL` orientation), `editText` 和`button` 是[拓展函数](http://kotlinlang.org/docs/reference/extensions.html) 构建新的 `View` 实例和添加到parent. 我们称这样的函数 *blocks*.

Blocks 在Android 框架中的每个 `View` 几乎存在,并且他们运行在`Activities`, `Fragments` (都是默认并且是从`android.support` 包中) 甚至对于 `Context`也是. 比如,如果你有一个`AnkoContext` 实例，你可以这样写blocks :

```
val name: EditText = with(ankoContext) {
    editText {
        hint = "Name"
    }
}
```

### AnkoComponent

虽然你可以直接使用DSL (在`onCreate()` 或者任何地方), 不用创建一个额外的类, 把UI放在一个隔开的类中，会带来方便。如果你使用提供的 `AnkoComponent` interface, 你也可以方便的得到一个 DSL [布局预览](https://github.com/Kotlin/anko/blob/master/doc/preview.png) 特性.

```
class MyActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?, persistentState: PersistableBundle?) {
        super.onCreate(savedInstanceState, persistentState)
        MyActivityUI().setContentView(this)
    }
}

class MyActivityUI : AnkoComponent<MyActivity> {
    override fun createView(ui: AnkoContext<MyActivity>) = with(ui) {
        verticalLayout {
            val name = editText()
            button("Say Hello") {
                onClick { ctx.toast("Hello, ${name.text}!") }
            }
        }
    }
}
```

### Helper blocks

你可能之前注意到了，`button()` 函数在之前的部分接受一个`String`参数。这样的helper blocks对于常使用的view如`TextView`, `EditText`, `Button` 和 `ImageView`中存在.

如果你对某个特别的view不需要设置任何属性，你可以这样缺省`{}` 并编写`button("Ok")` 或者直接这样 `button()`:

```
verticalLayout {
    button("Ok")
    button(R.string.cancel)
}
```

### Themed blocks

Anko 提供 "themeable"  blocks版本, 包括helper blocks:

```
verticalLayout {
    themedButton("Ok", theme = R.style.myTheme)
}
```

### Layouts 和 `LayoutParams`

组件在父容器中的位置，可以使用 `LayoutParams`.在XML 它长这样:

```
<ImageView 
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:layout_marginLeft="5dip"
    android:layout_marginTop="10dip"
    android:src="@drawable/something" />
```

在 Anko, 在View后使用`lparams()`具体指定:

```
linearLayout {
    button("Login") {
        textSize = 26f
    }.lparams(width = wrapContent) {
        horizontalMargin = dip(5)
        topMargin = dip(10)
    }
}
```

如果你指定`lparams()`, 但省略 `width` 和/或 `height`, 他们的默认值都是h `wrapContent`. 但你可以明确传值: use [命名变量](http://kotlinlang.org/docs/reference/functions.html#named-arguments).

一些方便的helper properties值得关注的:

- `horizontalMargin` 设置left和right margins,

- `verticalMargin` 设置 top 和bottom ones, and

- `margin` 同时设置四个margins


注意到`lparams()` 对不同的layouts是不同的,比如 `RelativeLayout`:

```
val ID_OK = 1

relativeLayout {
    button("Ok") {
        id = ID_OK
    }.lparams { alignParentTop() }
  
    button("Cancel").lparams { below(ID_OK) }
}
```

### Listeners

Anko 有无缝支持 coroutines 的listener helpers .你可以在你的listeners中写异步代码。

```
button("Login") {
    onClick {
    	val user = myRetrofitService.getUser().await()
        showUser(user)
    }
}
```

几乎等于这个:

```
button.setOnClickListener(object : OnClickListener {
    override fun onClick(v: View) {
    	launch(UI) {
    	    val user = myRetrofitService.getUser().await()
            showUser(user)
    	}
    }
})
```

当你的listeners 有大量的方法的时候，Anko十分有用。看看没有使用Anko的代码:

```
seekBar.setOnSeekBarChangeListener(object : OnSeekBarChangeListener {
    override fun onProgressChanged(seekBar: SeekBar, progress: Int, fromUser: Boolean) {
        // Something
    }
    override fun onStartTrackingTouch(seekBar: SeekBar?) {
        // Just an empty method
    }
    override fun onStopTrackingTouch(seekBar: SeekBar) {
        // Another empty method
    }
})
```

现在使用Anko:

```
seekBar {
    onSeekBarChangeListener {
        onProgressChanged { seekBar, progress, fromUser ->
            // Something
        }
    }
}
```

如果你设置 `onProgressChanged()` 和 `onStartTrackingTouch()` 给同样的 `View`, 这2个  "部分定义" listeners将被merged.对于同样的listener方法，采用最后一个.

### 自定义coroutine context

你可以传一个custom coroutine context 给listener helpers:

```
button("Login") {
    onClick(yourContext) {
    	val user = myRetrofitService.getUser().await()
        showUser(user)
    }
}
```

### 使用resource identifiers

在之前的篇章中，所有的例子使用原始的 Java strings,但这不优雅. 典型的做法是你把你的string 资源放在`res/values/` 文件夹中，并且在运行时调用的时候使用,比如, `getString(R.string.login)`.

幸运的, 在Anko你可以传resource identifiers 给helper blocks (`button(R.string.login)`) 和拓展属性 (`button { textResource = R.string.login }`).

注意名字不一样: 不是 `text`, `hint`, `image`, 我们现在用 `textResource`, `hintResource` 和 `imageResource`.

![:penguin:](http://upload-images.jianshu.io/upload_images/3509189-832dae5f22768b4b?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) *资源属性读取的时候抛AnkoException.* 

### Instance shorthand notation

有时候你需要传一个 `Context`给一些你的Activity代码中的Android SDK方法 通常你可以直接用 `this`, 但如果你在一个内部类中呢?你可能这样写，用java的话： `SomeActivity.this` 和用kotlin的这样`this@SomeActivity` 

用 Anko的话，你可以直接写`ctx`. 这是一个拓展属性可以用在 `Activity`and `Service` 甚至是 `Fragment` (它使用getActivity()`方法). 你也可以使用act获取一个 `Activity实例.

### UI wrapper

最开始，Anko经常使用 `UI` tag作为一个顶级的 DSL 元素:

```
UI {
    editText {
        hint = "Name"
    }
}
```

你仍可以使用这个标签.并且这用来拓展DSL当你不得不声明只有个 `ViewManager.customView` 函数的时候更简单。详情请看 [Extending Anko](https://github.com/Kotlin/anko/wiki/doc/ADVANCED.md#extending-anko) 

### Include tag

插入一个 XML layout 到 DSL很简单. 使用`include()`函数：

```
include<View>(R.layout.something) {
    backgroundColor = Color.RED
}.lparams(width = matchParent) { margin = dip(12) }
```

你可以继续使用 `lparams()` ,并且如果你提供一个指定类型取代 `View`, 你也可以使用这个类型在 `{}`里面:

```
include<TextView>(R.layout.textfield) {
    text = "Hello, world!"
}
```

## Anko Support plugin

Anko 支持插件在 IntelliJ IDEA 和 Android Studio都可用. 它允许你直接在IDE的tool窗口预览用Anko写的 `AnkoComponent` 类。

 ![:warning:](http://upload-images.jianshu.io/upload_images/3509189-7110445981f7b082?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) *The Anko Support plugin 当前只支持Android Studio 2.4+.* 

### 安装Anko Support plugin

你可以在 [这里](https://plugins.jetbrains.com/update/index?pr=&updateId=19242)下载 Anko Support plugin

### 使用插件

假设你有了这些用Anko写的类:

```
class MyActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?, persistentState: PersistableBundle?) {
        super.onCreate(savedInstanceState, persistentState)
        MyActivityUI().setContentView(this)
    }
}

class MyActivityUI : AnkoComponent<MyActivity> {
    override fun createView(ui: AnkoContext<MyActivity>) = ui.apply {
        verticalLayout {
            val name = editText()
            button("Say Hello") {
                onClick { ctx.toast("Hello, ${name.text}!") }
            }
        }
    }.view
}
```

把指针放进 `MyActivityUI` 声明中, 打开*Anko Layout Preview* tool window ("View" → "Tool Windows" → "Anko Layout Preview") 并且按 *Refresh*.

这会building the project, 所以要花点时间才会显示.

### XML to DSL Converter

The plugin 也支持转XML 的layout为 Anko Layouts 代码. 打开一个XML file 和选中  "Code" → "Convert to Anko Layouts DSL". 你可以同时转化多个XML layout文件
