# 自定义view

横：x

竖：y

画线：

```java
canvas.drawLine(startx, starty, stopx, stopy, mLinePaint);
```

画矩形：

```java
canvas.drawRect(mSelectRect, mSelectPaint);
```



设置属性：

在styles.xml

添加：

```xml
<declare-styleable name="CustomView">
    <attr name="default_color" format="color"/>
</declare-styleable>
```

不要在onDraw new东西。

获取宽，高

getWidth()

getHeight()

dp，px的转换

```java
public int dpToPx(int dp) {
    DisplayMetrics displayMetrics = getContext().getResources().getDisplayMetrics();
    return Math.round(dp * (displayMetrics.xdpi / DisplayMetrics.DENSITY_DEFAULT));
}
public int pxToDp(int px) {
        DisplayMetrics displayMetrics = getContext().getResources().getDisplayMetrics();
        return Math.round(px / (displayMetrics.xdpi / DisplayMetrics.DENSITY_DEFAULT));
    }
```

刷新view

invalidate()

获取颜色：

```java
mLineColor = ContextCompat.getColor(context, R.color.line_color);
```
