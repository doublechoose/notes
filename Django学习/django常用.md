django 

新建Django项目

django-admin startproject  project_name

manage.py: A command-line utility to interact with your project. It is a thin
wrapper around the django-admin.py tool. You don't need to edit this file.
• mysite/: Your project directory consist of the following files:
° __init__.py: An empty file that tells Python to treat the mysite
directory as a Python module.
° settings.py: Settings and configuration for your project. Contains
initial default settings.
° urls.py: The place where your URL patterns live. Each URL defined
here is mapped to a view.
° wsgi.py: Configuration to run your project as a WSGI application. 

Web服务器网关接口

网关：又称网间连接器，协议转换器。在网络层上实现网络互连，是最复杂的网络互连设备。

从一个房间走到另一个房间必定要经过一扇门。从一个网络向另一个网络发送信息，也必须经过一个门，这个门就是网关（gateway）。



初始化数据库

 cd mysite

python manage.py migrate

运行服务器

python manage.py runserver

创建一个应用

python manage.py startapp blog

创建迁移脚本

python manage.py makemigrations blog 



使用pyinstaller

pyinstaller -F -w -p F:\python35-32\Lib\site-packages;F:\python35-32\Lib;F:\python35-32\Lib\site-packages\PyQt5\Qt\bin;F:\python35-32\Lib\site-packa ges\matplotlib;F:\python35-32\Lib\site-packages\matplotlib\backends -i E:\0E207\soft\Cell_Similarity\images\icon.ico E:\0E207\soft\Cell_Similarity\CellSim.pyw  --hidden- import matplotlib.backends.backend_tkagg --hidden-import tkinter --hidden-import tkinter.filedialog



pyinstaller -F -w -p 

