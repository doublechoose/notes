今天在写RecyclerView的demo，Genymotion打开后，一直打不开adb，然后就一直 `adb kill-server`,`adb start-server`,并没什么软用，终端显示

 >  `List of devices attached
adb server version (32) doesn't match this client (39); killing...
error: could not install *smartsocket* listener: Address already in use
ADB server didn't ACK`

于是google了一下，发现是Genymotion 的问题，如图所示，使用`Use custom Android SDK tools`，然后选用android studio的Android SDK就能解决。 
![我是图片.png](http://upload-images.jianshu.io/upload_images/3509189-57b2ffcc0b49e373.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

