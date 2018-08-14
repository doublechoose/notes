

Yan Zhulanow edited this page on 12 May · [2 revisions](https://github.com/Kotlin/anko/wiki/Anko-Commons-%E2%80%93-Intents/_history)

## 内容

- [Using Anko `Intent` helpers in your project](https://github.com/Kotlin/anko/wiki/Anko-Commons-%E2%80%93-Intents#using-anko-intent-helpers-in-your-project)
- [`Intent` builder functions](https://github.com/Kotlin/anko/wiki/Anko-Commons-%E2%80%93-Intents#intent-builder-functions)
- [Useful `Intent` callers](https://github.com/Kotlin/anko/wiki/Anko-Commons-%E2%80%93-Intents#useful-intent-callers)

## 在你的项目中使用Anko `Intent` helpers

Intent helpers 是在 `anko-commons`里的.这样添加到你的 `build.gradle`:

```
dependencies {
    compile "org.jetbrains.anko:anko-commons:$anko_version"
}
```

## `Intent` builder functions

一般，你不得不写一堆来启动一个新 `Activity`. 并且它需要你写一个线，对你传的值都要加一行. 比如，这个是一段启动一个 `Activity`带有`("id", 5)`和一个指定的flag:

```
val intent = Intent(this, SomeOtherActivity::class.java)
intent.putExtra("id", 5)
intent.setFlag(Intent.FLAG_ACTIVITY_SINGLE_TOP)
startActivity(intent)
```

四行太多了. Anko为你提供一个更简单的方式:

```
startActivity(intentFor<SomeOtherActivity>("id" to 5).singleTop())
```

如果你不需要传任何flags, 解决方法更简单:

```
startActivity<SomeOtherActivity>("id" to 5)
```

## Useful `Intent` callers

Anko 有一些常用 `Intents`的调用包装:

| Goal    | Solution                             |
| ------- | ------------------------------------ |
| 打电话     | `makeCall(number)` 不用**tel:**        |
| 发短信     | `sendSMS(number, [text])` 不用**sms:** |
| 浏览网页    | `browse(url)`                        |
| 分享文字    | `share(text, [subject])`             |
| 发送email | `email(email, [subject], [text])`    |

方括号中的参数是可选的，如果intent发送，方法返回true.
