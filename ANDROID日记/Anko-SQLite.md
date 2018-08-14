你是否疲于用Android cursor解析SQLite 查询结果？你被逼着写大量的模板代码，只是为了解析结果，然后用许许多多的 `try..finally`关闭所有打开的资源。

Anko提供了大量的拓展函数来简化执行于 SQLite 

## 在你的项目中使用 Anko SQLite 

添加 `anko-sqlite` 依赖到你的 `build.gradle`:

```
dependencies {
    compile "org.jetbrains.anko:anko-sqlite:$anko_version"
}
```

## Accessing the database

如果你使用 `SQLiteOpenHelper`, 你通常调用 `getReadableDatabase()` 或者 `getWritableDatabase()`(在代码上是一样的), 但是你一定要在接收到`SQLiteDatabase`后保证调用 `close()`方法,你也要缓存helper class, 并且如果你从多个线程使用，你一定要考虑并发。这些都相当烦人.这就是为虾米Android 开发者不喜欢用原生的SQLite API而偏爱贵重包装类如ORMs

Anko提供一个特别的类 `ManagedSQLiteOpenHelper` 可以无缝的替代原生的.下面为如何使用:

```
class MyDatabaseOpenHelper(ctx: Context) : ManagedSQLiteOpenHelper(ctx, "MyDatabase", null, 1) {
    companion object {
        private var instance: MyDatabaseOpenHelper? = null

        @Synchronized
        fun getInstance(ctx: Context): MyDatabaseOpenHelper {
            if (instance == null) {
                instance = MyDatabaseOpenHelper(ctx.getApplicationContext())
            }
            return instance!!
        }
    }

    override fun onCreate(db: SQLiteDatabase) {
        // Here you create tables
        db.createTable("Customer", true, 
                    "id" to INTEGER + PRIMARY_KEY + UNIQUE,
                    "name" to TEXT,
                    "photo" to BLOB)
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        // Here you can upgrade tables, as usual
        db.dropTable("User", true)
    }
}

// Access property for Context
val Context.database: MyDatabaseOpenHelper
    get() = MyDatabaseOpenHelper.getInstance(getApplicationContext())
```

So what's the sense?现在你可以直接这样写，而不用 `try`块关闭:

```
database.use {
    // `this` is a SQLiteDatabase instance
}
```

The database将会在执行完花括号 `{}`中的所有代码后关闭.

异步调用例子：

```
class SomeActivity : Activity() {
    private fun loadAsync() {
        async(UI) {
            val result = bg { 
                database.use { ... }
            }
            loadComplete(result)
        }
    }
}
```

| ![:penguin:](http://upload-images.jianshu.io/upload_images/3509189-8b94f5f42eae8341?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) | *下面及所有的方法可能抛SQLiteException. 你不得不自己处理，因为Anko不能自己认为错误没有发生.* |
| ---------------------------------------- | ---------------------------------------- |
|                                          |                                          |

## Creating and dropping tables

有了Anko，你可以简单的创建新的表和丢掉存在的表。语法十分直接

```
database.use {
    createTable("Customer", true, 
        "id" to INTEGER + PRIMARY_KEY + UNIQUE,
        "name" to TEXT,
        "photo" to BLOB)
}
```

在SQLite, 有五种重要类型: `NULL`, `INTEGER`, `REAL`, `TEXT` 和 `BLOB`. 但每个有可能有些modifiers 如 `PRIMARY KEY` 或者 `UNIQUE`. 你可以通过 "adding"他们到元基本类型名.

删表,用 `dropTable` 函数:

```
dropTable("User", true)
```

## Inserting data

一般来说，你需要一个 `ContentValues` 来插入一行到表中.如下：

```
val values = ContentValues()
values.put("id", 5)
values.put("name", "John Smith")
values.put("email", "user@domain.org")
db.insert("User", null, values)
```

Anko让你传值就像 `insert()`方法的参数一样:

```
// Where db is an SQLiteDatabase
// eg: val db = database.writeableDatabase
db.insert("User", 
    "id" to 42,
    "name" to "John",
    "email" to "user@domain.org"
)
```

或者用 `database.use` 如下:

```
database.use {
    insert("User", 
        "id" to 42,
        "name" to "John",
        "email" to "user@domain.org"
}
```

请注意，这上面的例子 `database`是一个database helper 实例,`db` 是一个 `SQLiteDatabase` 对象

函数 `insertOrThrow()`, `replace()`, `replaceOrThrow()` 也有，并且类似的写法.

## Querying data

Anko 提供一个十分方便的查询builder. 它可能被 `db.select(tableName, vararg columns)` 创建，其中 `db` 是一个`SQLiteDatabase`实例.

| Method                                   | Description                              |
| ---------------------------------------- | ---------------------------------------- |
| `column(String)`                         | Add a column to select query             |
| `distinct(Boolean)`                      | Distinct query                           |
| `whereArgs(String)`                      | Specify raw String `where` query         |
| `whereArgs(String, args)` ![:star:](http://upload-images.jianshu.io/upload_images/3509189-fce81405b9953425?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) | Specify a `where` query with arguments   |
| `whereSimple(String, args)`              | Specify a `where` query with `?` mark arguments |
| `orderBy(String, [ASC/DESC])`            | Order by this column                     |
| `groupBy(String)`                        | Group by this column                     |
| `limit(count: Int)`                      | Limit query result row count             |
| `limit(offset: Int, count: Int)`         | Limit query result row count with an offset |
| `having(String)`                         | Specify raw `having` expression          |
| `having(String, args)` ![:star:](http://upload-images.jianshu.io/upload_images/3509189-9bbf596d715505be?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) | Specify a `having` expression with arguments |

标上 ![:star:](http://upload-images.jianshu.io/upload_images/3509189-5513ae01f9bc8d01?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) 的函数用一种特殊的方法解析参数。他们允许你提供任何命令的值和无缝支持跳过。

```
db.select("User", "name")
    .whereArgs("(_id > {userId}) and (name = {userName})",
        "userName" to "John",
        "userId" to 42)
```

这里, `{userId}` 会被 `42`替换和 `{userName}` 被 `'John'`替换.值将被跳过，如果它的类型不是数字类型 (`Int`, `Float` etc.) 或者 `Boolean`.对于其他类型，会使用 `toString()`.

`whereSimple`函数接收 `String` 类型的参数. 和`SQLiteDatabase`中的 [`query()`](http://developer.android.com/reference/android/database/sqlite/SQLiteDatabase.html#query(java.lang.String,%20java.lang.String%5B%5D,%20java.lang.String,%20java.lang.String%5B%5D,%20java.lang.String,%20java.lang.String,%20java.lang.String)) 方法一样 (question marks `?` will be replaced with actual values from arguments).

我们如何执行查找呢?用 `exec()` 函数. 它接受一个拓展函数 `Cursor.() -> T`. 它简单的启动了received extension 函数然后关掉了 `Cursor`，所以你不必亲自动手:

```
db.select("User", "email").exec {
	// Doing some stuff with emails
}
```

## Parsing query results

于是我们有了一些 `Cursor`, 那如何解析到规则的类中呢？ Anko提供了函数 `parseSingle`, `parseOpt` 和`parseList` 来更简单的完成.

| Method                          | Description             |
| ------------------------------- | ----------------------- |
| `parseSingle(rowParser): T`     | Parse exactly one row   |
| `parseOpt(rowParser): T?`       | Parse zero or one row   |
| `parseList(rowParser): List<T>` | Parse zero or more rows |

注意到 ，如果Cursor包含多于1个列，`parseSingle()` 和 `parseOpt()` 将会抛出一个异常.

现在问题是: 什么是 `rowParser`? 每个函数支持2种不同类型的解析器: `RowParser` 和 `MapRowParser`:

```
interface RowParser<T> {
    fun parseRow(columns: Array<Any>): T
}

interface MapRowParser<T> {
    fun parseRow(columns: Map<String, Any>): T
}
```

如果你想另辟蹊径的写你的query,用 RowParser (但是你必须知道每行的index). `parseRow` 接收一个 `Any`的列表 (类型 `Any` 可以是任意类型除了`Long`, `Double`, `String` or `ByteArray`). `MapRowParser`, 另一方面让你用列名来获取行值.

Anko 有对于简单的单行列的解析器（不知道翻的对不对already has parsers for simple single-column rows）:

- `ShortParser`
- `IntParser`
- `LongParser`
- `FloatParser`
- `DoubleParser`
- `StringParser`
- `BlobParser`

你也可以从类的构造函数创建一个列解析器. 假如你有一个类:

```
class Person(val firstName: String, val lastName: String, val age: Int)
```

解析器将这么简单:

```
val rowParser = classParser<Person>()
```

目前, Anko **不支持** 创建主要构造函数可选参数这样的解析器. 而且构造器会用Java反射调用，所以写一个自定义的`RowParser`用于打数据集才合适.

如果你用Anko `db.select()` builder,你可以直接调用 `parseSingle`, `parseOpt` or `parseList` 然后传一个适当的 parser.

## Custom row parsers

比如，我们来做个新的行解析器 `(Int, String, String)`. 最朴素的方法如下:

```
class MyRowParser : RowParser<Triple<Int, String, String>> {
    override fun parseRow(columns: Array<Any>): Triple<Int, String, String> {
        return Triple(columns[0] as Int, columns[1] as String, columns[2] as String)
    }
}
```

现在我们的代码中有三个明确的主角，让我们使用 `rowParser`函数摆脱他们:

```
val parser = rowParser { id: Int, name: String, email: String ->
    Triple(id, name, email)
}
```

完成! `rowParser`让所有的主角在兜里并且你可以随意命名lambda 参数.

## Cursor streams

Anko 提供一个函数式的方法访问 SQLite `Cursor` .酱调用 `cursor.asSequence()`或者 `cursor.asMapSequence()` 拓展函数来获取sequence of rows.别忘记close the `Cursor` :)

## Updating values

让我们给我们的一个user换名字:

```
update("User", "name" to "Alice")
    .where("_id = {userId}", "userId" to 42)
    .exec()
```

Update 也有一个 `whereSimple()` 方法以防你想提供一个传统的查找：

```
update("User", "name" to "Alice")
    .`whereSimple`("_id = ?", 42)
    .exec()
```

## Transactions

有个特殊的函数叫 `transaction()`，可以允许你 放入多个数据库操作在一个单次 SQLite transaction.

```
transaction {
    // Your transaction code
}
```

The transaction will be marked as successful if no exception was thrown inside the `{}` block.

| ![:penguin:](http://upload-images.jianshu.io/upload_images/3509189-da0d7b0760cedf45?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240) | *If you want to abort a transaction for some reason, just throw TransactionAbortException. You don't need to handle this exception by yourself in this case.* |
| ---------------------------------------- | ---------------------------------------- |
|                                          |                                          |
