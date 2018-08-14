翻译：[http://jakewharton.github.io/butterknife/](http://jakewharton.github.io/butterknife/)
### 介绍

Butter Knife使用@BindView和一个view的ID做注解来找到layout中的view。

```java
class ExampleActivity extends Activity {
  @BindView(R.id.title) TextView title;
  @BindView(R.id.subtitle) TextView subtitle;
  @BindView(R.id.footer) TextView footer;

  @Override public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.simple_activity);
    ButterKnife.bind(this);
    // TODO Use fields...
  }
}
```

不是用慢的反射，代码是生成的，调用bind委托，上面的代码会生成如下：

``` java
public void bind(ExampleActivity activity) {
  activity.subtitle = (android.widget.TextView) activity.findViewById(2130968578);
  activity.footer = (android.widget.TextView) activity.findViewById(2130968579);
  activity.title = (android.widget.TextView) activity.findViewById(2130968577);
}
```

### 资源绑定

使用`@BindBool`, `@BindColor`, `@BindDimen`, `@BindDrawable`, `@BindInt`, `@BindString`绑定预定义的资源

```java
class ExampleActivity extends Activity {
  @BindString(R.string.title) String title;
  @BindDrawable(R.drawable.graphic) Drawable graphic;
  @BindColor(R.color.red) int red; // int or ColorStateList field
  @BindDimen(R.dimen.spacer) Float spacer; // int (for pixel size) or float (for exact value) field
  // ...
}
```



### 非Activity 绑定

你也可以通过提供你自己的view root 来绑定

```java
public class FancyFragment extends Fragment {
  @BindView(R.id.button1) Button button1;
  @BindView(R.id.button2) Button button2;

  @Override public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
    View view = inflater.inflate(R.layout.fancy_fragment, container, false);
    ButterKnife.bind(this, view);
    // TODO Use fields...
    return view;
  }
}
```

另一种使用简化了一个list adapter 里的 view holder 样式

```java
public class MyAdapter extends BaseAdapter {
  @Override public View getView(int position, View view, ViewGroup parent) {
    ViewHolder holder;
    if (view != null) {
      holder = (ViewHolder) view.getTag();
    } else {
      view = inflater.inflate(R.layout.whatever, parent, false);
      holder = new ViewHolder(view);
      view.setTag(holder);
    }

    holder.name.setText("John Doe");
    // etc...

    return view;
  }

  static class ViewHolder {
    @BindView(R.id.title) TextView name;
    @BindView(R.id.job_title) TextView jobTitle;

    public ViewHolder(View view) {
      ButterKnife.bind(this, view);
    }
  }
}
```

你可以在提供的sample中看到这实现。

- 在哪里使用findViewById,就可以在哪里调用ButterKnife.bind。
- 使用ButterKnife.bind(this) 绑定一个view的子view。如果你使用\<merge>标签和inflate一个自定义的view 构造器，你可以马上调用这个，或者自定义view类型可以再onFinishInflate()中回调。

### View lists

你可以将多个view放在一个list或者array中。

```java
@BindViews({ R.id.first_name, R.id.middle_name, R.id.last_name })
List<EditText> nameViews;
```
apply 方法允许你执行一次就能将所有view放在list中

```java
ButterKnife.apply(nameViews, DISABLE);
ButterKnife.apply(nameViews, ENABLED, false);
```

Action 和 Setter 接口允许指定简单的行为。

```java
static final ButterKnife.Action<View> DISABLE = new ButterKnife.Action<View>() {
  @Override public void apply(View view, int index) {
    view.setEnabled(false);
  }
};
static final ButterKnife.Setter<View, Boolean> ENABLED = new ButterKnife.Setter<View, Boolean>() {
  @Override public void set(View view, Boolean value, int index) {
    view.setEnabled(value);
  }
};
```

一个android 的属性也可以通过apply方法使用：

`ButterKnife.apply(nameViews, View.ALPHA, 0.0f);`

### 监听器绑定

监听器也可以自动的在方法中配置

```java
@OnClick(R.id.submit)
public void submit(View view) {
  // TODO submit data to server...
}
//指定一个类型，就会被自动转型
@OnClick(R.id.submit)
public void sayHi(Button button) {
  button.setText("Hello!");
}
//对于常用事件处理，可以指定多个id
@OnClick({ R.id.door1, R.id.door2, R.id.door3 })
public void pickDoor(DoorView door) {
  if (door.hasPrizeBehind()) {
    Toast.makeText(this, "You win!", LENGTH_SHORT).show();
  } else {
    Toast.makeText(this, "Try again", LENGTH_SHORT).show();
  }
}

//自定义view可以不指定id，绑定成他们自己的监听器
public class FancyButton extends Button {
  @OnClick
  public void onClick() {
    // TODO do something!
  }
}

```

### 绑定重置

Fragment比Activity多一个不同的view 生命周期。在onCreateView 中绑定，在onDestroyView中设置view为null。当你调用bind的时候，ButterKnife 返回一个 Unbinder 实例，在适当的生命周期回调中调用它的unbind。

```java
public class FancyFragment extends Fragment {
  @BindView(R.id.button1) Button button1;
  @BindView(R.id.button2) Button button2;
  private Unbinder unbinder;

  @Override public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
    View view = inflater.inflate(R.layout.fancy_fragment, container, false);
    unbinder = ButterKnife.bind(this, view);
    // TODO Use fields...
    return view;
  }

  @Override public void onDestroyView() {
    super.onDestroyView();
    unbinder.unbind();
  }
}
```

### 可选绑定

默认的，@Bind 和 listener 绑定是需要的。当目标view未被发现就会抛出异常。为了镇压这种行为和创建一个可选的绑定，给方法添加@Nullable 注解或者@Optional注解。

注：任何叫@Nullable的注解都能被用，而且鼓励用Android的"support-annotations"库的@Nullable 注解。

```java
@Nullable @BindView(R.id.might_not_be_there) TextView mightNotBeThere;

@Optional @OnClick(R.id.maybe_missing) void onMaybeMissingClicked() {
  // TODO ...
}
```

### 多方法监听器

响应监听器的方法注解有多个回调可以被用来绑定他们中任何一个。每个注解有一个默认的回调。指定一个使用 callback的参数。

```java
@OnItemSelected(R.id.list_view)
void onItemSelected(int position) {
  // TODO ...
}

@OnItemSelected(value = R.id.maybe_missing, callback = NOTHING_SELECTED)
void onNothingSelected() {
  // TODO ...
}
```

### 彩蛋

可以使用findById来简化不得不在View，Activity，或者Dialog中找View的代码。它使用简单的转型。

```java
View view = LayoutInflater.from(context).inflate(R.layout.thing, null);
TextView firstName = ButterKnife.findById(view, R.id.first_name);
TextView lastName = ButterKnife.findById(view, R.id.last_name);
ImageView photo = ButterKnife.findById(view, R.id.photo);
```

给ButterKnife.findById 添加一个静态import，玩的开心。

### 下载

##### GRADLE

```
compile 'com.jakewharton:butterknife:8.6.0'
annotationProcessor 'com.jakewharton:butterknife-compiler:8.6.0'
```
翻译有错的请多多指教哈
