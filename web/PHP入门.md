## 语法

PHP 脚本可以放在文档中的任何位置。

PHP 脚本以 **<?php** 开始，以 **?>** 结束：

```php
<?php
// PHP 代码
?>
```

## 变量

```php
<?php
$x=5;
$y=6;
$z=$x+$y;
echo $z;
?>
```

## echo & print

echo 和 print 区别:

- echo - 可以输出一个或多个字符串
- print - 只允许输出一个字符串，返回值总为 1

**提示：**echo 输出的速度比 print 快， echo 没有返回值，print有返回值1。

## 数据类型

```php
<?php 
$x = "Hello world!";
echo $x;
echo "<br>"; 
$x = 'Hello world!';
echo $x;

$x = 5985;
var_dump($x);
echo "<br>"; 
$x = -345; // 负数 
var_dump($x);
echo "<br>"; 
$x = 0x8C; // 十六进制数
var_dump($x);
echo "<br>";
$x = 047; // 八进制数
var_dump($x);

$x = 10.365;
var_dump($x);
echo "<br>"; 
$x = 2.4e3;
var_dump($x);
echo "<br>"; 
$x = 8E-5;
var_dump($x);

$x=true;
$y=false;

$cars=array("Volvo","BMW","Toyota");
var_dump($cars);


 var $color;
  function Car($color="green") {
    $this->color = $color;
  }
  function what_color() {
    return $this->color;
  }

$x=null;
?>
```

## 常量

```php
<?php
// 区分大小写的常量名
define("GREETING", "欢迎访问 Runoob.com");
echo GREETING;    // 输出 "欢迎访问 Runoob.com"
echo '<br>';
echo greeting;   // 输出 "greeting"
?>
```

## String

```php
<?php 
$txt1="Hello world!"; 
$txt2="What a nice day!"; 
echo $txt1 . " " . $txt2; 

echo strlen("Hello world!"); 

echo strpos("Hello world!","world"); 
?>
```

## if ... else

```php
<?php
$t=date("H");
if ($t<"20")
{
    echo "Have a good day!";
}
?>
```

## switch

```php
<?php
switch (n)
{
case label1:
    如果 n=label1，此处代码将执行;
    break;
case label2:
    如果 n=label2，此处代码将执行;
    break;
default:
    如果 n 既不等于 label1 也不等于 label2，此处代码将执行;
}
?>
```

## 数组

```php
<?php
$cars=array("Volvo","BMW","Toyota");
echo "I like " . $cars[0] . ", " . $cars[1] . " and " . $cars[2] . ".";

echo count($cars);

for($x=0;$x<$arrlength;$x++)
{
    echo $cars[$x];
    echo "<br>";
}

$age=array("Peter"=>"35","Ben"=>"37","Joe"=>"43");
echo "Peter is " . $age['Peter'] . " years old.";

foreach($age as $x=>$x_value)
{
    echo "Key=" . $x . ", Value=" . $x_value;
    echo "<br>";
}
?>
```

## 排序

```php
<?php
$cars=array("Volvo","BMW","Toyota");
sort($cars);
//降序
rsort($cars);

$age=array("Peter"=>"35","Ben"=>"37","Joe"=>"43");
//根据值升序
asort($age);
//根据key升序
ksort($age);
//根据值降序
arsort($age);
//根据key降序
krsort($age);
?>
```

## 超级全局变量

PHP 超级全局变量列表:

- $GLOBALS
- $_SERVER
- $_REQUEST
- $_POST
- $_GET
- $_FILES
- $_ENV
- $_COOKIE
- $_SESSION

## while

```php+HTML
<html>
<body>

<?php
$i=1;
while($i<=5)
{
echo "The number is " . $i . "<br>";
$i++;
}

$i=1;
do
{
$i++;
echo "The number is " . $i . "<br>";
}
while ($i<=5);
?>
?>

</body>
</html>
```

## for

```php+HTML
<html>
<body>

<?php
for ($i=1; $i<=5; $i++)
{
echo "The number is " . $i . "<br>";
}
?>

</body>
</html>
```

## 函数

```php+HTML
<html>
<body>

<?php
function writeName()
{
echo "Kai Jim Refsnes";
}

echo "My name is ";
writeName();

function writeName($fname)
{
echo $fname . " Refsnes.<br>";
}

function add($x,$y)
{
$total=$x+$y;
return $total;
}
?>

</body>
</html>
```

## 魔术变量

## 命名空间

## 面向对象

```php
<?php 
class Site { 
  /* 成员变量 */ 
  var $url; 
  var $title; 
   
  /* 成员函数 */ 
  function setUrl($par){ 
     $this->url = $par; 
  } 
   
  function getUrl(){ 
     echo $this->url . PHP_EOL; 
  } 
   
  function setTitle($par){ 
     $this->title = $par; 
  } 
   
  function getTitle(){ 
     echo $this->title . PHP_EOL; 
  } 
} 

$taobao = new Site; 
$google = new Site; 

// 调用成员函数，设置标题和URL 
$taobao->setTitle( "淘宝" ); 
$google->setTitle( "Google 搜索" ); 

$taobao->setUrl( 'www.taobao.com' ); 
$google->setUrl( 'www.google.com' ); 

// 调用成员函数，获取标题和URL 
$taobao->getTitle(); 
$google->getTitle(); 

$taobao->getUrl(); 
$google->getUrl(); 
?>
```

