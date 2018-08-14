## 基础知识

- 位置参数
- MotionEvent
- TouchSlop
- VelocityTracker
- GestureDetector
- Scroller

理解：首先讲的view，是放在屏幕中的，在布局上，需要知道它的位置，要个位置参数很正常吧，然后要有交互行为，当手在接触屏幕的时候(ACTION_DOWN)，手指在屏幕上移动的时候(ACTION_MOVE)，离开屏幕的时候(ACTION_UP)，谁来处理这些事件呢？MotionEvent，没错，是他是他就是他。接触屏幕和离开屏幕好办，问题是怎么确定在移动呢，这时候就要规定一个滑动的最小距离（TouchSlop），当手指在屏幕上移动超过这个距离就认为是在移动状态了。光是知道在移动还不够，你肯定好奇移动的速度是多少，这就要一个速度的追踪器(VelocityTracker)。

接下来是手势检测，大部分的手势，无非是单击，滑动，长按，双击等行为。如果用之前的ACTION_DOWN，ACTION_MOVE，ACTION_UP要写很多东西，如

单击：ACTION_DOWN，ACTION_UP，中间的时间要短

滑动：ACTION_DOWN，ACTION_MOVE 一段时间，ACTION_UP

长按：ACTION_DOWN，ACTION_UP，中间的时间要长

使用GestureDetector，就可以免去很多麻烦，人家帮你检测好了，拿去判断吧。

在实际生活中，滑动是不是有很多种滑动，比如加速度滑、匀速滑，加速度后减速滑等，使用Scroller，滑动者，致力于各种花式滑动，找他就对了。

## 滑动

滑动的实现有三种：

- View本身提供的scrollTo/scrollBy 方法
- 动画对view施加平移效果
- 改变view的布局参数(LayoutParams)

### scrollTo/scrollBy

scrollTo是绝对滑动

scrollBy是相对滑动

实际上scrollBy里还是使用的scrollTo。

### 使用动画





### 改变布局参数

```java
MarginLayoutParams params = (MarginLayoutParams)mButton.getLayoutParams();
params.width += 100;
params.leftMargin +=100;
mButton.requestLayout();
//or mButton.setLayoutParams(params);
```

### 总结

- scrollTo/scrollBy : 操作简单，适合对View内容的滑动，只有内容移动，View不动。
- 动画：操作简单，适用于没有交互的View和实现复杂动画效果
- 改变布局参数：操作稍微复杂，适用于有交互的View

## 弹性滑动



