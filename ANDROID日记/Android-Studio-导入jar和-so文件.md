## 导入jar

将jar文件放在libs文件夹中，右键该jar，点击选项 add as library，点击确认，搞定。



## 添加so文件

1. 在src/main中添加 jniLibs文件夹 ，把.so复制进去
2. 将so文件放入libs文件夹中，在gradle中添加

```
sourceSets{
        main {
            jniLibs.srcDirs = ['libs']
        }
    }
```

具体位置：

```
apply plugin: 'com.android.application'

apply plugin: 'kotlin-android'

apply plugin: 'kotlin-android-extensions'

android {
    compileSdkVersion 26
    defaultConfig {
        applicationId "com.example.administrator.xxx"
        minSdkVersion 21
        targetSdkVersion 26
        versionCode 1
        versionName "1.0"
        testInstrumentationRunner "android.support.test.runner.AndroidJUnitRunner"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }

    sourceSets{
        main {
            jniLibs.srcDirs = ['libs']
        }
    }
}

dependencies {
    implementation fileTree(include: ['*.jar'], dir: 'libs')
    implementation "org.jetbrains.kotlin:kotlin-stdlib-jre7:$kotlin_version"
    implementation 'com.android.support:appcompat-v7:26.0.0-beta1'
    implementation 'com.android.support.constraint:constraint-layout:1.0.2'
    testImplementation 'junit:junit:4.12'
    androidTestImplementation 'com.android.support.test:runner:1.0.1'
    androidTestImplementation 'com.android.support.test.espresso:espresso-core:3.0.1'
}

```

以上。
