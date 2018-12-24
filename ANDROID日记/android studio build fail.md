# android studio build fail

升级Android Studio 从3.0.1 到 3.2出现的问题：

根目录下执行：

```
gradlew assembleDebug --stacktrace
```



可以看到错误：找不到符号等日志

原因：

依赖由`compile`改为`implement`

**implementation**不可以依赖传递；依赖对app Module 是不可见的

**compile**可以依赖传递；依赖对app Module 是可见的

改为`api`

### The SourceSet 'instrumentTest' is not recognized by the Android Gradle 

升级后Gradle编译的时候提示：The SourceSet 'instrumentTest' is not recognized by the Android Gradle Plugin. Perhaps you misspelled something?

解决办法：在gradle中请找到：instrumentTest.setRoot(‘tests’)
 更换为：        androidTest.setRoot('tests')即可