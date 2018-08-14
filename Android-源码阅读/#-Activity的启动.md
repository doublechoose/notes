startActivity - startActivityForResult - mInstrument.execStartActivity - ActivityManagerNative.getDefault() .startActivityAsUser - mActivityStarter.startActivityMayWait - startActivityLocked - startActivityUnchecked - mSupervisor.resumeFocusedStackTopActivityLocked - mFocusedStack.resumeTopActivityUncheckedLocked - resumeTopActivityInnerLocked - mStackSupervisor.startSpecificActivityLocked - realStartActivityLocked - app.thread.scheduleLaunchActivity -  sendMessage -  handleLaunchActivity - performLaunchActivity

### performLaunchActivity

1. 从ActivityClientRecord中获取启动activity的组件信息
2. 通过Instrumentation的newActivity方法使用类加载器创建Activity对象
3. 通过loadedApk的makeApplication方法尝试创建Application对象
4. 创建ContextImpl对象并通过Activity的attach方法完成一些重要数据的初始化
5. 调用Activity的onCreate方法
