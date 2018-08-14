

Alex Saveau edited this page on 29 Oct · [7 revisions](https://github.com/Kotlin/anko/wiki/Anko-Commons-%E2%80%93-Dialogs/_history)

## 内容

- [Using Anko Dialogs in your project](https://github.com/Kotlin/anko/wiki/Anko-Commons-%E2%80%93-Dialogs#using-anko-dialogs-in-your-project)
- [Toasts](https://github.com/Kotlin/anko/wiki/Anko-Commons-%E2%80%93-Dialogs#toasts)
- [SnackBars](https://github.com/Kotlin/anko/wiki/Anko-Commons-%E2%80%93-Dialogs#snackbars)
- [Alerts](https://github.com/Kotlin/anko/wiki/Anko-Commons-%E2%80%93-Dialogs#alerts)
- [Selectors](https://github.com/Kotlin/anko/wiki/Anko-Commons-%E2%80%93-Dialogs#selectors)
- [Progress dialogs](https://github.com/Kotlin/anko/wiki/Anko-Commons-%E2%80%93-Dialogs#progress-dialogs)

## 在你的项目中使用Anko Dialogs 

Dialog helpers在 `anko-commons`中 .作为一个依赖添加到你的 `build.gradle`:

```
dependencies {
    compile "org.jetbrains.anko:anko-commons:$anko_version"
    compile "org.jetbrains.anko:anko-design:$anko_version" // For SnackBars
}
```

## Toasts

简单的显示一个 [Toast](https://developer.android.com/guide/topics/ui/notifiers/toasts.html)消息.

```
toast("Hi there!")
toast(R.string.message)
longToast("Wow, such duration")
```

## SnackBars

简单的显示一个[SnackBar](https://developer.android.com/reference/android/support/design/widget/Snackbar.html) 消息.

```
snackbar(view, "Hi there!")
snackbar(view, R.string.message)
longSnackbar(view, "Wow, such duration")
snackbar(view, "Action, reaction", "Click me!") { doStuff() }
```

## Alerts

一个显示[alert dialogs](https://developer.android.com/guide/topics/ui/dialogs.html).的小DSL

```
alert("Hi, I'm Roy", "Have you tried turning it off and on again?") {
    yesButton { toast("Oh…") }
    noButton {}
}.show()
```

上面的代码将会显示默认的 Android alert dialog.如果你想切换到appcompat 实现, 使用`Appcompat` dialog factory:

```
alert(Appcompat, "Some text message").show()
```

`Android` 和`Appcompat` dialog factories 默认包含,但你可以创建你自己的，通过实现 `AlertBuilderFactory` interface.

`alert()` 函数无缝支持 Anko layouts作为自定义views:

```
alert {
    customView {
        editText()
    }
}.show()
```

## Selectors

`selector()` 显示一个文本项的列表的alert dialog:

```
val countries = listOf("Russia", "USA", "Japan", "Australia")
selector("Where are you from?", countries, { dialogInterface, i ->
    toast("So you're living in ${countries[i]}, right?")
})
```

## Progress dialogs

`progressDialog()` 创建和显示一个[progress dialog](https://developer.android.com/reference/android/app/ProgressDialog.html).

```
val dialog = progressDialog(message = "Please wait a bit…", title = "Fetching data")
```

indeterminate progress dialog 也可以 (see `indeterminateProgressDialog()`).
