## menu 隐藏 
在`onPrepareOptionsMenu`方法中，使用menuItem的setVisible方法

## 单行省略号

```
android:maxLines="1"
android:ellipsize="end"
```
## 在布局中使用tool:text
```xml
           <TextView
            android:id="@+id/tv_name"
            android:layout_width="wrap_content"
            android:gravity="left|start|center_vertical"
            android:layout_height="wrap_content"
            tools:text="@string/netdisk_super_long_string"/>
```
可以用于预览，并且不会被带进apk里

## 防止连续点击出现多个重复页面
`import com.jakewharton.rxbinding.view.RxView;`

```java

RxView.clicks(viewHolder.itemView)
                    .throttleFirst(1, TimeUnit.SECONDS)
                    .subscribe(new Action1<Void>() {
                        @Override
                        public void call(Void aVoid) {
                            if (mOnFooterViewClickInterface != null) {
                                mOnFooterViewClickInterface.onFootViewClickLintener();
                            }
                        }
                    });
```
## 特殊符号的编码
```java
/*编码关键字，当为单引号'的时候会出现mac错误，下为处理方案*/
        String encodeWord=keyWord;
        if (mKeyword.trim().equals("'")||mKeyword.trim().contains("'")){
            try {
                encodeWord = URLEncoder.encode(mKeyword,"utf-8");
            } catch (UnsupportedEncodingException e) {
                Log.e(TAG, "doSearch: ", e);
            }
        }else {
            encodeWord = Uri.encode(mKeyword);
        }
```
## 防止多点触控

在item的父布局中添加`android:splitMotionEvents="false"`

## 支持Android M
`RxPermission`

## DateFormat
`DD month dd` 会造成 `illegal pattern character 'o'`

## Anyproxy
当需要拦截https的时候
安装证书+下面这个
`anyproxy --intercept`

## ViewPager 获取当前fragment
对 FragmentStatePagerAdapter子类添加下面2个方法
```
 @Override  
    public void setPrimaryItem(ViewGroup container, int position, Object object) {  
        mCurrentFragment = (XXXFragment) object;  
        super.setPrimaryItem(container, position, object);  
    }  
  
  
    public XXXFragment getCurrentFragment() {  
        return mCurrentFragment;  
    } 
```
