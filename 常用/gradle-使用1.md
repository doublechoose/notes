

1.安装gradle

```
brew install gradle
```

初始化一个项目

首先创建一个文件夹

mkdir basic-demo

cd basic-demo

使用```gradle init```创建一个项目

创建一个任务

一个项目包含许多个任务。

Gradle附带了一个可以在您自己的项目中配置的任务库。比如拷贝，从一个位置拷贝到另一个位置。拷贝十分有用。但现在尽量简单。跟着下面步骤走：

1. 创建一个src的文件夹
2. 在src中添加一个命名为myfile.txt的文件。内容随意（可以为空）。但为了方便添加一行Hello，World！
3. 在你的build文件定义一个任务叫copy的类型Copy（注意大小写），拷贝src文件夹到新的文件夹dest中（不必创建这个dest文件夹，task会自动帮你创建）

```
build.gradle

task copy(type: Copy,group:"Custom",description:"Copies sources to the dest directory"){
    from "src"
    into "dest"
}
```

这里，group和description可以是你希望的任何东西。您甚至可以省略它们，但这样做也会在以后使用的任务报告中省略它们。

现在执行你的copy task

```
./gradlew copy
```

添加插件

Gradle包含一系列插件，Gradle插件门户提供了许多插件。 该发行版附带的插件之一是基本插件。 结合名为Zip的核心类型，您可以使用已配置的名称和位置创建项目的zip存档。

使用插件语法将base插件添加到构建脚本文件中。 请务必在文件顶部添加插件{}块

```
plugins {
    id "base"
}
```

现在添加一个task从src文件夹创建一个zip压缩包

```
task zip(type: Zip, group: "Archive", description: "Archives sources in a zip file") {
    from "src"
    setArchiveName "basic-demo-1.0.zip"
}
```

base插件在build/distributions中创建一个档案文件叫basic-demo-1.0.zip

```
./gradlew zip
```

探索和调试你的build

tasks命令列出了您可以调用的Gradle任务，包括基本插件添加的任务，以及您刚刚添加的自定义任务。

分析和调试你的debug

gradle也提供了丰富的，基于web view的你的build，叫build scan。

通过使用--scan选项或者明确的应用build scan到你的项目中，你可以创建一个build scan。

properties 命令告诉你一个项目的属性

默认情况下，项目的名称与文件夹的名称匹配。 您还可以指定组和版本属性，但目前它们采用默认值，如描述。

buildFile属性是构建脚本的完全限定路径名，默认情况下位于projectDir中。

您可以更改许多属性。 例如，您可以尝试将以下行添加到构建脚本文件中，然后重新执行gradle属性。

```
description = "A trivial Gradle build"
version = "1.0"
```
