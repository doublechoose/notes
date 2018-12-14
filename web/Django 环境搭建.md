# Django 环境搭建

安装pip

```
cd /data;
mkdir tmp;
cd tmp;
wget https://bootstrap.pypa.io/get-pip.py;
python ./get-pip.py;
```

安装Django

```
pip install Django
```

安装mysql

因为 CentOS 7 之后的版本都不在提供 Mysql 安装源，这里我们使用 mariadb 代替 mysql，依次执行下列命令

```
yum install mariadb mariadb-server -y
```

```
yum install MySQL-python -y
```

```
systemctl start mariadb
```