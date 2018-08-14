问题：
# [Conflict with dependency 'com.android.support:support-annotations' in project ':app'. Resolved versions for app (26.1.0) and test app (27.1.1) differ.](https://stackoverflow.com/questions/50117626/conflict-with-dependency-com-android-supportsupport-annotations-in-project)

解决方案：
1. 添加依赖：
    implementation 'com.android.support:support-annotations:27.1.1'
然后sync 下你的项目


2.在App的build.gradle 配置：
```
android {
    //...
    ////增加这行
    configurations.all {
        resolutionStrategy.force 'com.android.support:support-annotations:27.1.1'
    }
}
```
