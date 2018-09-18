# 关于pyc



关于PyCodeObject和pyc文件：在硬盘上看到的pyc文件，其实PyCodeObject才是Python编译器真正编译成的结果。当python程序运行时，编译的结果是保存在位于内存中的PyCodeObject中，当Python程序运行结束时，Python解释器则将PyCodeObject写回到pyc文件中。当python程序第二次运行时，首先程序会在硬盘中寻找pyc文件，如果找到，则直接载入，否则就重复上面的过程。所以，我们可以说pyc文件其实是PyCodeObject的一种持久化保存方式。



python 守护线程

如果设置一个线程为守护线程，就表示这个线程是不重要的，在进程退出的时候，不用等待这个线程退出。







```
# 打开浏览器
fname = "C:/Users/Administrator/AppData/Local/Temp/tmpema2wquk.html"

webbrowser.open("file://%s" % fname)
```

