android源码中的RadioButton:

```xml
<style name="Widget.CompoundButton.RadioButton">  
        <item name="android:background">@android:drawable/btn_radio_label_background</item>  
        <item name="android:button">@android:drawable/btn_radio</item>  
</style> 
```

其中的btn_radio_label_background是.9图

btn_radio是xml的drawable：

```xml
<selector xmlns:android="http://schemas.android.com/apk/res/android">      
    <item android:state_checked="true" android:state_window_focused="false"  
          android:drawable="@drawable/btn_radio_on" />  
    <item android:state_checked="false" android:state_window_focused="false"  
          android:drawable="@drawable/btn_radio_off" />  
  
    <item android:state_checked="true" android:state_pressed="true"  
          android:drawable="@drawable/btn_radio_on_pressed" />  
    <item android:state_checked="false" android:state_pressed="true"  
          android:drawable="@drawable/btn_radio_off_pressed" />  
  
    <item android:state_checked="true" android:state_focused="true"  
          android:drawable="@drawable/btn_radio_on_selected" />  
    <item android:state_checked="false" android:state_focused="true"  
          android:drawable="@drawable/btn_radio_off_selected" />  
  
    <item android:state_checked="false" android:drawable="@drawable/btn_radio_off" />  
    <item android:state_checked="true" android:drawable="@drawable/btn_radio_on" />  
</selector>  
```

drawable的item中可以有以下属性： 
android:drawable="@[package:]drawable/drawable_resource" 
android:state_pressed=["true" | "false"] 
android:state_focused=["true" | "false"] 
android:state_selected=["true" | "false"] 
android:state_active=["true" | "false"] 
android:state_checkable=["true" | "false"] 
android:state_checked=["true" | "false"] 
android:state_enabled=["true" | "false"] 
android:state_window_focused=["true" | "false"] 

制作button的样式

```xml
<selector xmlns:android="http://schemas.android.com/apk/res/android">

    <!--当不可用时-->
    <item android:drawable="@drawable/btn_click_unable" android:state_enabled="false"/>
    <!--按下时-->
    <item android:drawable="@drawable/btn_click_press" android:state_pressed="true"/>

    <item android:drawable="@drawable/btn_click_press" android:state_focused="true"/>

    <item android:drawable="@drawable/btn_click_press" android:state_selected="true"/>

    <item android:drawable="@drawable/btn_click_normal"/>
</selector>
```
radiobutton的样式
```
<?xml version="1.0" encoding="utf-8"?>
<selector xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@drawable/selecticon" android:state_checked="true" android:state_enabled="true"
          android:state_pressed="true"/>

    <item android:drawable="@drawable/unselecticon" android:state_checked="false" android:state_enabled="true"
          android:state_pressed="true"/>

    <item android:drawable="@drawable/selecticon" android:state_checked="true"
          android:state_enabled="true"/>

    <item android:drawable="@drawable/unselecticon" android:state_checked="false"
          android:state_enabled="true"/>

    <item android:drawable="@drawable/selecticon" android:state_checked="true"
          android:state_enabled="false"/>

    <item android:drawable="@drawable/unselecticon" android:state_checked="false"
          android:state_enabled="false"/>

</selector>
```
