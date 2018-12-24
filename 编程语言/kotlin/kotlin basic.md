# kotlin basic



### 定义包

```
package my.demo

import java.util.*

// ...
```

### 定义函数

```
fun sum(a: Int, b: Int): Int {
	return a + b
}

fun printSum(a: Int, b: Int): Unit {
	println("sum of $a and $b is ${a + b}")
}

fun printSum(a: Int, b: Int) {
	println("sum of $a and $b is ${a + b}")
}
```

### 定义变量

```
val a: Int = 1 // immediate assignment
val b = 2 // `Int` type is inferred
val c: Int // Type required when no initializer is provided
c = 3 // deferred assignment
```

```
var x = 5 // `Int` type is inferred
x += 1
```

```
val PI = 3.14
var x = 0
fun incrementX() {
	x += 1
}
```

### 注释

```
// This is an end-of-line comment
/* This is a block comment
on multiple lines. */
```

### string 模板

```
var a = 1
// simple name in template:
val s1 = "a is $a"
a = 2
// arbitrary expression in template:
val s2 = "${s1.replace("is", "was")}, but now is $a"
```

### 条件表达式

```
fun maxOf(a: Int, b: Int): Int {
if (a > b) {
return a
} else {
return b
}
}
```

```
fun maxOf(a: Int, b: Int) = if (a > b) a else b
```

