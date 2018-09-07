# logstash 启动报无法找到主类解决方案

# https://www.jianshu.com/p/93bc46fbc594

当logstash启动时，首先要注意正确配置java

并且最近版本的logstash要求java8

在搞定以上后确认环境变量没有问题

再确认logstash所在的目录 不存在含有空格的文件夹名称

**在这所有所有之后还是会报错：找不到或无法加载主类 （乱序地址)**

# 解决方案

废话不多说：找到logstash/bin目录下的logstash.bat
打开编辑,找到如下行
%JAVA% %JAVA_OPTS% -cp "%CLASSPATH%" org.logstash.Logstash %*
这行与你的应该有所区别，没错

**将%CLASSPATH%改为"%CLASSPATH%"即可解决**

让我学习一下批处理写法 理解一下这行为什么这样，之后，有空再解释原因

------

2018年3月9日17:19:19更新

# 产生原因

> PS G:\Users\XXX\Desktop> ./logstash.bat
> 错误: 找不到或无法加载主类 Files\Java\jdk1.8.0_161\lib;G:"Program

以上是错误命令运行的输出 可以看到 找不到或无法加载主类，而后跟着的目录为

> Files\Java\jdk1.8.0_161\lib;G:"Program

因为我的jdk 放在G:\Program Files\java\jdk1.8.0_161\lib下了，因此一开始百思不得其解，什么错误会产生位置字符串中间截断然后颠倒这种迷之错误。

因为logstash启动文件是个批处理，这样调试起来就很方便在，在各行插入**pause**语句调试，最后将错误定位到52行

```
%JAVA% %JAVA_OPTS% -cp %CLASSPATH% org.logstash.Logstash %*

```

今天学习了一下批处理语法，这一句无非是将一些变量组合成为新的语句再执行而已，那么错误不在批处理程序，因为自己再写批处理的话难保拿到的变量与运行时完全一样所以直接在logstash.bat中插入了一些语句将其输出(因为没那么多时间阅读全文，前面已经提到了直接定位到了出错是这一句)

```
%JAVA% %JAVA_OPTS% -cp %CLASSPATH% org.logstash.Logstash %*
pause
echo %JAVA% >>a.txt
echo " " >>a.txt
echo %JAVA_OPTS%>>a.txt
echo " "  >>a.txt
echo %CLASSPATH%>>a.txt
echo " "  >>a.txt
echo %*>>a.txt
echo " "  >>a.txt
echo "%CLASSPATH%" >>a.txt
pause

```

将上面的语句改写成这样，将变量全部输出到a.txt，检查该文件

> "G:\Program Files\Java\jdk1.8.0_161\bin\java.exe"
>
> -Xms1------很长的字符串------/urandom
>
> .;G:\Program Files\Java\jdk1.8.0_161\lib;G:\Program Files\Java\jdk1.8.0_161\lib\tools.jar;"E:\logstash-6.2.2\logstash-core\lib\jars\animal-sniffer-annotations-1.14.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\commons-compiler-3.0.8.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\error_prone_annotations-2.0.18.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\google-java-format-1.5.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\guava-22.0.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\j2objc-annotations-1.1.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\jackson-annotations-2.9.1.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\jackson-core-2.9.1.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\jackson-databind-2.9.1.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\jackson-dataformat-cbor-2.9.1.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\janino-3.0.8.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\javac-shaded-9-dev-r4023-3.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\jruby-complete-9.1.13.0.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\jsr305-1.3.9.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\log4j-api-2.9.1.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\log4j-core-2.9.1.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\log4j-slf4j-impl-2.9.1.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\logstash-core.jar";"E:\logstash-6.2.2\logstash-core\lib\jars\slf4j-api-1.7.25.jar"
>
> -f ../config/pipeline.conf

**抱歉我知道上面这坨太冗杂了**但是相信我，比较重要吧。
观察上面这些输出，再结合logstash.bat中的实际语序，可以发现这实际上是一句简单的java程序启动的cmd.

```
java -opt1 -opt2 -cp "classpath" org.logstash.Logstash -f ../config/pipeline.conf

```

那么到这一步 再结合错误输出为找不到或无法加载主类，可以猜测是-cp 之后的classpath出现了问题。
仔细观察classpath，发现一些问题，该字符串明显为拼接字符串，然而有些地址用双引号（**""**）括起来了，有些没有。再观察，可以发现括起来的为logstash自己的jar包，没有的则为系统本身的CLASSPATH环境变量的值。

*猜测由双引号引起该问题，再加上前面的解决方案是在整个%CLASSPATH%变量外面加 \**""** 可以猜测为系统本身的CLASSPATH没有加上双引号引起的，按照他的style将双引号加在每个地址上，**问题解决**。*

继续研究。回到**logstash/bat**文件，发现

```
:concat
IF not defined CLASSPATH (
  set CLASSPATH="%~1"
) ELSE (
  set CLASSPATH=%CLASSPATH%;"%~1"
)

```

很明显 该代码段产生了整个批处理文件中实际调用的CLASSPATH
调用该代码段的地方是

```
for %%i in ("%LS_HOME%\logstash-core\lib\jars\*.jar") do (
    call :concat "%%i"
)

```

很容易懂的一个循环，对logstash目录下的\logstash-core\lib\jars\下的所有jar包循环，将包名作为参数执行上上的那个代码段，即
**将logstash jar包目录下的所有jar包的所在路径连接到系统本身的CLASSPATH路径之后**  
那么到此CLASSPATH的产生方式已经很明显了，错误也很明显了，产生CLASSPATH时，因为系统中有CLASSPATH变量因此直接执行ELSE部分，将系统变量通过 **"%CLASSPATH%"** 的方式直接读取，在之后加上;"%~1"
这里%~1的作用是取第一个参数并去掉双引号，第一个参数是循环的当时系数，而去掉双引号之后又加上了双引号所以最后的结果是有双引号的，这也就是我们看到的 调用的CLASSPATH后面的logstash的包都有双引号的原因。而在循环第一次执行的时候，直接用了系统的%CLASSPATH%这里是没有双引号的，因此结果也没有（**不能在这里加双引号，因为随着循环，引号会被递归加上，整个路径会乱掉**）

> 这里有一个另外的思考，前面的输出a.txt文件可以看到，直接用%JAVA%输出的java.exe所在目录实际上竟然是有双引号的，而我自己写了个批处理 "echo %JAVA%显示的是echo 开关状态，证明找不到JAVA这个系统变量，这是显然的，但是我在logstash.bat中竟然没有找到对变量JAVA的set操作，也就是说找不到这个JAVA地址是在何处获得并赋值的，也就无法研究java.exe的路径为何是有双引号的。

# 重要的解释

我认为还需要解释一下为什么不加引号就会炸，大家还记得最开始的错误输出吧

> PS G:\Users\XXX\Desktop> ./logstash.bat
> 错误: 找不到或无法加载主类 Files\Java\jdk1.8.0_161\lib;G:"Program

这其实并不是地址断掉了或者说倒置了，而是Program FIile 中间有一个**空格**，批处理文件以空格作为分格符，由于我的jdk放置在系统盘的program file文件夹下，因此我的环境变量的classpath中有两个包含空格的路径，批处理命令将第一个空格前的内容作为java -cp命令中的classpath地址传入， 后两个空格间的"**Files\Java\jdk1.8.0_161\lib;G:"Program**"自然就作为主类传入了，因此产生了如此奇怪的输出。而解决空格的方法就是:

> ### 将有空格或其他特殊字符的字符串用("")括起来