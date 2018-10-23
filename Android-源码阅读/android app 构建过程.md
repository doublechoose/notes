# android app 构建过程



> 我们平时在android studio中点击run ，就能把代码编译成一个apk文件并安装到手机上。那么这个过程中都具体发生了什么 ？我们是怎么把代码和资源文件打包成一个apk文件，并安装到手机上的呢 ？ 今天就详细研究一下这个流程  。

## Apk构建基本流程



![img](https:////upload-images.jianshu.io/upload_images/1951128-f6985fb6e1f74f24.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/747/format/webp)

build-simplified.png

上图是Android官方提供的打包简略流程图。清晰地展示了一个Android Project经过编译和打包后生成apk文件，然后再经过签名，就可以安装到设备上

我们将一个实际的apk文件后缀改为zip并解压后，得到的内容如下



![img](https:////upload-images.jianshu.io/upload_images/1951128-22e8271dd5e65ede.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

apk_component_1.png

和上图的描述一致。apk包内容包括：

- classes.dex…
- resources.arsc
- assets
- res
- AndroidManifest.xml
- META-INF

其中：

1. res中图片和raw文件下内容保持原样，res中其他xml文件内容均转化为二进制形式；assets文件内容保持原样
2. res中的文件会被映射到R.java文件中，访问的时候直接使用资源ID即R.id.filename；assets文件夹下的文件不会被映射到R.java中，访问的时候需要AssetManager类

## 在看下这张图 ，android apk构建详细流程图



![img](https:////upload-images.jianshu.io/upload_images/1951128-812d5a5d0a7ee64a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/670/format/webp)

QQ截图20161230105534.png

#### 打包步骤：

#### 1. 通过aapt打包res资源文件，生成R.java、resources.arsc和res文件（二进制 & 非二进制如res/raw和pic保持原样） ，详细步骤如下

- 检查AndroidManifest.xml，主要做一些检查并使用parsePackage初始化并设置一些attribute，比如package, minSdkVersion, uses-sdk。
- 添加被引用资源包使用table.addIncludedResources(bundle, assets)添加被引用资源包，比如系统的那些android:命名空间下的资源。
- 收集资源文件,处理overlay（重叠包，如果指定的重叠包有和当前编译包重名的资源，则使用重叠包的）:
- 将收集到的资源文件加到资源表(ResourceTable)对res目录下的各个资源子目录进行处理，函数为makeFileResources:makeFileResources会对资源文件名做合法性检查，并将其添加到ResourceTable内。
- 编译values资源并添加到资源表,在上一步添加过程中，其实并没有对values资源进行处理，因为values比较特殊，需要经过编译之后，才能添加到资源表中。
- 给bag资源分配id,在继续编译其他资源之前，我们需要先给bag资源（attrs，比如orientation这种属性的取值范围定义的子元素）分配id，因为其他资源可能对它们有引用。
- 编译xml资源文件,最后我们终于可以编译xml文件了，因为我们已经为它准备好了一切可能引用到的东西（value, drawable等）。程序会对layouts, anims, animators等逐一调用
- ResourceTable.cpp的,进行编译，内部流程又可以分为：解析xml文件，赋予属性名称资源id，解析属性值，扁平化为二进制文件。
- 编译AndroidManifest.xml文,拿到AndroidManifest.xml文件,清空原来的数据，重新解,处理package name重载，把各种相对路径的名字改为绝对路径,编译manifest xml文件,生成最终资源表.9.生成R.java文件

**生成我们解压后看到的那个resources.arsc:**

#### 2. 处理.aidl文件，生成对应的Java接口文件

- aidl，全名Android Interface Definition Language，即Android接口定义语言。
   输入：aidl后缀的文件。输出：可用于进程通信的C/S端java代码，位于build/generated/source/aidl。

#### 3. 通过Java Compiler编译R.java、Java接口文件、Java源文件，生成.class文件

我们有了R.java和aidl生成的Java文件，再加上工程的源代码，现在可以使用javac进行正常的java编译生成class文件了。

输入：java source的文件夹（另外还包括了build/generated下的：R.java, aidl生成的java文件，以及BuildConfig.java）。输出：对于gradle编译，可以在build/intermediates/classes里，看到输出的class文件。

源码编译之后，我们可能还会对其进行代码的混淆，混淆的作用是增加反编译的难度，同时也将一些代码的命名进行了缩短，减少代码占用的空间。混淆完成之后，会生成一个混淆前后的映射表，这个是用来在反应我们的应用执行的时候的一些堆栈信息，可以将混淆后的信息转化为我们混淆前实际代码中的内容。

#### 4. 通过dex命令，将.class文件和第三方库中的.class文件处理生成classes.dex

调用dx.bat将所有的class文件（上一步生成的以及第三方库的）转化为classes.dex文件，dx会将class转换为Dalvik字节码，生成常量池，消除冗余数据等。

#### 5. 通过apkbuilder工具，将aapt生成的resources.arsc和res文件、assets文件和classes.dex一起打包生成apk

打包生成APK文件。旧的apkbuilder脚本已经废弃，现在都已经通过sdklib.jar的ApkBuilder类进行打包了。输入为我们之前生成的包含resources.arcs的.ap_文件，上一步生成的dex文件，以及其他资源如jni、jar包内的资源。

大致步骤为
 以包含resources.arcs的.ap_文件为基础，new一个ApkBuilder，设置debugMode
 apkBuilder.addZipFile(f);
 apkBuilder.addSourceFolder(f);
 apkBuilder.addResourcesFromJar(f);
 apkBuilder.addNativeLibraries(nativeFileList);
 apkBuilder.sealApk(); // 关闭apk文件
 generateDependencyFile(depFile, inputPaths, outputFile.getAbsolutePath());

#### 6. 通过Jarsigner工具，对上面的apk进行debug或release签名

对apk文件进行签名。APK需要签名才能在设备上进行安装很多时候我们在逆向改完后，会因为没有签名文件导致最后的apk无法正常使用，又细分为本地验证和服务器验证。

#### 7. 通过zipalign工具，将签名后的apk进行对齐处理。

调用buildtoolszipalign，对签名后的apk文件进行对齐处理，使apk中所有资源文件距离文件起始偏移为4字节的整数倍，从而在通过内存映射访问apk文件时会更快。同时也减少了在设备上运行时的内存消耗。这样我们的最终apk就生成完毕了。

> 关于zipalign工具，根据名字就知道是个zip文件对齐的工具。使得apk中的资源文件偏离文件起始位置4个字节，从而可以通过mmap()直接访问，从而减少RAM占用。

## 参考文档

[1、官网 ：配置构建](https://link.jianshu.com?t=https://developer.android.com/studio/build/index.html?hl=zh-cn)
 [2、apk 构建流程](https://www.jianshu.com/p/a679669d6be2)
 [3、Android打包系列——打包流程梳理](https://link.jianshu.com?t=http://mouxuejie.com/blog/2016-08-04/build-and-package-flow-introduction/)
 [4、APK打包安装过程](https://link.jianshu.com?t=https://segmentfault.com/a/1190000004916563)



链接：https://www.jianshu.com/p/4962634901fb

