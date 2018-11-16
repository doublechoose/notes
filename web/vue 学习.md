vue 学习

http://jiongks.name/blog/vue-code-review/

webpack 是一个模块打包机

它做的事情是，分析你的项目结构，找到JavaScript模块以及其它的一些浏览器不能直接运行的拓展语言（Scss，TypeScript等），并将其打包为合适的格式以供浏览器使用。

es6 主要有2个功能：export 和import

export 用于对外输出本模块（一个文件理解为一个模块）变量的接口

import 用于在一个模块中加载另一个含有export接口的模块

```
export default
```

1、export与export default均可用于导出常量、函数、文件、模块等
2、你可以在其它文件或模块中通过import+(常量 | 函数 | 文件 | 模块)名的方式，将其导入，以便能够对其进行使用
3、在一个文件或模块中，export、import可以有多个，export default仅有一个
4、通过export方式导出，在导入时要加{ }，export default则不需要



这样来说其实很多时候export与export default可以实现同样的目的，只是用法有些区别。注意第四条，通过export方式导出，在导入时要加{ }，export default则不需要。使用export default命令，为模块指定默认输出，这样就不需要知道所要加载模块的变量名。



列出数组的每个元素：

```
<button onclick="numbers.forEach(myFunction)">点我</button>
<p id="demo"></p>
 
<script>
demoP = document.getElementById("demo");
var numbers = [4, 9, 16, 25];
 
function myFunction(item, index) {
    demoP.innerHTML = demoP.innerHTML + "index[" + index + "]: " + item + "<br>"; 
}
</script>
```



