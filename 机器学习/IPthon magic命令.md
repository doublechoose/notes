#  IPthon magic命令 

# Jupyter Notebook 的快捷键



## **IPthon magic命令**

%作用于一行代码，%%作用于cell
%%capture 屏蔽当前cell打印
与系统命令交互，前面加!：! ping [www.baidu.com](http://www.baidu.com/)
tap 补全
shift + tap 查看文档，多按几次效果不同
_表示使用上一个cell的结果
sum? sum?? 查看文档
%pdoc objctname 查看对象的文档
%psource objctname 查看源码
%pdef funcname 查看函数定义
%pfile objctname 查看所有源码文件
%quickref 显示IPython的快速参考
%magic 显示所有魔术命令的详细文档
%lsmagic 显示所有魔术命令
%debug 从最新的异常跟踪的底部进入交互式调试器
%hist 打印命令的输入（可选输出）历史
%pdb 在异常发生后自动进入调试器
%paste 执行剪贴板中的Python代码
%cpaste 打开一个特殊提示符以便手工粘贴待执行的Python代码
%reset 删除interactive命名空间中的全部变量/名称
%page OBJECT 通过分页器打印输出OBJECT
%run [script.py](http://script.py/) 在IPython中执行一个Python脚本文件
%prun statement 通过cProfile执行statement，并打印分析器的输出结果。
%prun 可显示运行时间
%time statement 报告statement的执行时间
%timeit statement 多次执行statement以计算系综平均执行时间。
%who、%who_ls、%whos 显示interactive命名空间中定义的变量，信息级别/冗余度可变
%xdel variable 删除variable，并尝试清除其在IPython中的对象上的一切引用
%pwd 目前工作文件夹
%reset_f 重置变量空间
%mkdir %cd %ls %rmdir 类似于dos的文件夹相关命令**

## **Jupyter快捷方式**

命令模式 (按键 Esc 开启)
Enter : 转入编辑模式
Shift-Enter : 运行本单元，选中下个单元
Ctrl-Enter : 运行本单元
Alt-Enter : 运行本单元，在其下插入新单元
Y : 单元转入代码状态
M :单元转入markdown状态
R : 单元转入raw状态
1 : 设定 1 级标题
2 : 设定 2 级标题
3 : 设定 3 级标题
4 : 设定 4 级标题
5 : 设定 5 级标题
6 : 设定 6 级标题
Up : 选中上方单元
K : 选中上方单元
Down : 选中下方单元
J : 选中下方单元
Shift-K : 扩大选中上方单元
Shift-J : 扩大选中下方单元
A : 在上方插入新单元
B : 在下方插入新单元
X : 剪切选中的单元
C : 复制选中的单元
Shift-V : 粘贴到上方单元
V : 粘贴到下方单元
Z : 恢复删除的最后一个单元
D,D : 删除选中的单元
Shift-M : 合并选中的单元
Ctrl-S : 文件存盘
S : 文件存盘
L : 转换行号
O : 转换输出
Shift-O : 转换输出滚动
Esc : 关闭页面
Q : 关闭页面
H : 显示快捷键帮助
I,I : 中断Notebook内核
0,0 : 重启Notebook内核
Shift : 忽略
Shift-Space : 向上滚动
Space : 向下滚动
编辑模式 ( Enter 键启动)
Tab : 代码补全或缩进
Shift-Tab : 提示
Ctrl-] : 缩进
Ctrl-[ : 解除缩进
Ctrl-A : 全选
Ctrl-Z : 复原
Ctrl-Shift-Z : 再做
Ctrl-Y : 再做
Ctrl-Home : 跳到单元开头
Ctrl-Up : 跳到单元开头
Ctrl-End : 跳到单元末尾
Ctrl-Down : 跳到单元末尾
Ctrl-Left : 跳到左边一个字首
Ctrl-Right : 跳到右边一个字首
Ctrl-Backspace : 删除前面一个字
Ctrl-Delete : 删除后面一个字
Esc : 进入命令模式
Ctrl-M : 进入命令模式
Shift-Enter : 运行本单元，选中下一单元
Ctrl-Enter : 运行本单元
Alt-Enter : 运行本单元，在下面插入一单元
Ctrl-Shift-- : 分割单元
Ctrl-Shift-Subtract : 分割单元
Ctrl-S : 文件存盘
Shift : 忽略
Up : 光标上移或转入上一单元
Down :光标下移或转入下一单元