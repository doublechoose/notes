打开VS code命令面板，mac下快捷键：shift+command+P 或者 F1
在打开的命令面板里输入或者在 quick pick 内找到 Python: Select Workspace Interpreter 这条命令
执行后会列出自动扫描出的解释器路径，选择你想要的就可以了
它其实是在你的项目根目录下新建了一个 ./.vscode/settings.json 配置文件，将解释器路径选项写在里面了，该文件称为工作区设置，可以针对每个项目单独设置配置项。当然了你自己手动设置也是没有问题的。
