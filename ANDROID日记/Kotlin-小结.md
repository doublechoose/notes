## Hello World

```kotlin
fun main(args: Array<String>) {
    println("Hello, world!")
}
```

## 变量

```kotlin
val array = arrayListOf<String>()
val pair = Pair(1, "one")

```





## IF ELSE

```kotlin
fun main(args: Array<String>) {
    println(max(args[0].toInt(), args[1].toInt()))
}

fun max(a: Int, b: Int) = if (a > b) a else b
```

判断 `is`,`!is`

```kotlin
fun getStringLength(obj: Any): Int? {
    if (obj is String)
        return obj.length // no cast to String is needed
    return null
}
```



## WHILE 

```kotlin
fun main(args: Array<String>) {
    var i = 0
    while (i < args.size)
        println(args[i++])
}
```

## FOR

```kotlin
fun main(args: Array<String>) {
    for (arg in args)
        println(arg)

    // or
    println()
    for (i in args.indices)
        println(args[i])
}
```

## WHEN（switch）

```kotlin
fun main(args: Array<String>) {
    cases("Hello")
    cases(1)
    cases(0L)
    cases(MyClass())
    cases("hello")
}

fun cases(obj: Any) {
    when (obj) {
        1 -> println("One")
        "Hello" -> println("Greeting")
        is Long -> println("Long")
        !is String -> println("Not a string")
        else -> println("Unknown")
    }
}

class MyClass() {
}
```

## CLASS

```kotlin
fun main(args: Array<String>) {
    val pair = Pair(1, "one")
    val (num, name) = pair

    println("num = $num, name = $name")
}

class Pair<K, V>(val first: K, val second: V) {
    operator fun component1(): K {
        return first
    }

    operator fun component2(): V {
        return second
    }
}
//////////////////////////////////////////////////////////
data class User(val name: String, val id: Int)

fun getUser(): User {
    return User("Alex", 1)
}

fun main(args: Array<String>) {
    val user = getUser()
    println("name = ${user.name}, id = ${user.id}")

    // or

    val (name, id) = getUser()
    println("name = $name, id = $id")

    // or

    println("name = ${getUser().component1()}, id = ${getUser().component2()}")
}
```
