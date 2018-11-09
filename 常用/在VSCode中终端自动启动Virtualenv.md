# vscode 打开终端自动加载virtualenv 环境

### 第一步：在VSCode中配置Virtualenv

使用快捷键`CTRL` + `SHIFT` + `P`打开命令面板，输入`设置`，选择`首选项: 打开设置`，在`工作区设置`中添加`python.pythonPath`的配置项，如下（**C:\Virtualenv\py3env\Scripts\python.exe为Virtualenv的虚拟环境python绝对路径**）：

```
{
    "python.pythonPath": "C:\\Virtualenv\\py3env\\Scripts\\python.exe"
}123
```



使用快捷键`CTRL` + `SHIFT` + `P`打开命令面板，输入`python select`，选择`python: 选择解析器`,这时候能看到配置的python解析器 


此时，使用快捷键`CTRL` + ```打开终端（VSCode默认是cmd打开），如下（**在命令行前面没有指明虚拟环境**）：

```
Microsoft Windows [版本 6.1.7601]
版权所有 (c) 2009 Microsoft Corporation。保留所有权利。

(这个位置)C:\Users\XXX\iCloudDrive\PycharmProjects\bilibili\myblog>
```

### 第二步：在VSCode中配置Terminal

使用快捷键`CTRL` + `SHIFT` + `P`打开命令面板，输入`设置`，选择`首选项: 打开设置`，在`工作区设置`中添加`terminal.integrated.shellArgs.windows`的配置项

```
{
    "python.pythonPath": "C:\\Virtualenv\\py3env\\Scripts\\python.exe",
    //或者这么设置
    "python.venvPath": "D:\\QQPCmgr\\anaconda\\envs\\tensorflow\\python.exe",
    "python.terminal.activateEnvironment": true

    "terminal.integrated.shellArgs.windows": ["/k", "C:\\Virtualenv\\py3env\\Scripts\\activate"]
}
```

此时，使用快捷键`CTRL` + ```打开终端（VSCode默认是cmd打开），如下：

```
(py3env) C:\Users\XXX\iCloudDrive\PycharmProjects\bilibili\myblog>
```

### 题外话（linux、mac平台有其他参数配置）

`linux`: terminal.integrated.shellArgs.linux[“-c”, “source ./env/bin/activate”] 
`mac`: terminal.integrated.shellArgs.osx[“-c”, “source ./env/bin/activate”]

