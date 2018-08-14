
## Hello world

```kotlin
fun main(args: Array<String>) {
    println("Hello, world!")
}
```

## Read a name from arg

```kotlin
fun main(args: Array<String>) {
    if (args.size == 0) {
        println("Please provide a name as a command-line argument")
        return
    }
    println("Hello, ${args[0]}!")
}
```

## Read many name

```kotlin
fun main(args: Array<String>) {
    for (name in args)
        println("Hello, $name!")
}
```

## A multi-language Hello

```kotlin
fun main(args: Array<String>) {
    val language = if (args.size == 0) "EN" else args[0]
    println(when (language) {
        "EN" -> "Hello!"
        "FR" -> "Salut!"
        "IT" -> "Ciao!"
        else -> "Sorry, I can't greet you in $language yet"
    })
}
```

## A object-orientd Hello

```kotlin
class Greeter(val name: String) {
    fun greet() {
        println("Hello, ${name}");
    }
}

fun main(args: Array<String>) {
    Greeter(args[0]).greet()
}
```
