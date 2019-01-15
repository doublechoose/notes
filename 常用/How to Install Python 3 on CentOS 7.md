# How to Install Python 3 on CentOS 7

This tutorial will guide you through installing Python 3 on a CentOS 7 system using the Software Collections (SCL) along side the distribution default Python version 2.7. We will also show you how to create a Python virtual environment.

Python is one of the most popular programming languages in the world. With its simple and easy to learn syntax Python is a great choice for beginners and experienced developers. Python is quite versatile programming language, you can use it to do almost anything you want, write small scripts, build games, develop websites, create machine learning algorithms, analyze data and more.

Many popular applications and websites including YouTube, DropBox, Reddit, Quora, Instagram, Pinterest have been developed using Python.

While Python 2 is well-supported and active, Python 3 is considered to be the present and future of the language.

## [Enable Software Collections (SCL)](https://linuxize.com/post/how-to-install-python-3-on-centos-7/#enable-software-collections-scl)

[Software Collections](https://www.softwarecollections.org/en/), also known as SCL is a community project that allows you to build, install, and use multiple versions of software on the same system, without affecting system default packages. By enabling Software Collections you will gain access to the newer versions of programming languages and services which are not available in the core repositories.

CentOS 7 ships with Python 2.7.5 which is a critical part of the CentOS base system. SCL will allow you to install newer versions of python 3.x alongside the default python v2.7.5 so that system tools such as `yum` will continue to work properly.

In order to enable SCL we need to install the CentOS SCL release file. It is part of the CentOS extras repository and can be installed by running the following command:

```console-bash
sudo yum install centos-release-scl
```

Copy

## [Installing Python 3 on CentOS 7](https://linuxize.com/post/how-to-install-python-3-on-centos-7/#installing-python-3-on-centos-7)

Now that we have access to the SCL repository we can install any Python 3.x version we need. Currently the following Python 3 collections are available:

- Python 3.3
- Python 3.4
- Python 3.5
- Python 3.6

In this tutorial we will install Python 3.6 which is the latest version available at the time of writing. To do so type the following command on your CentOS 7 terminal:

```console-bash
sudo yum install rh-python36
```

Copy

## [Using Python 3](https://linuxize.com/post/how-to-install-python-3-on-centos-7/#using-python-3)

After the package `rh-python36` is installed, check the Python version by typing:

```console-bash
python --version
```

Copy

```output
Python 2.7.5
```

Copy

You will notice that Python 2.7 is the default Python version in your current shell.

To access Python 3.6 you need to launch a new shell instance using the Software Collection `scl` tool:

```console-bash
scl enable rh-python36 bash
```

Copy

What the command above does is calling the script `/opt/rh/rh-python36/enable` which changes the shell environment variables.

If you check the Python version again, you’ll notice that Python 3.6 is the default version in your current shell now.

```console-bash
python --version
```

Copy

```output
Python 3.6.3
```

Copy

It is important to point out that Python 3.6 is set as the default Python version only in this shell session. If you exit the session or open a new session from another terminal Python 2.7 will be the default Python version.

## [Installing Development Tools](https://linuxize.com/post/how-to-install-python-3-on-centos-7/#installing-development-tools)

Development tools are required for building Python modules, you can install the necessary tools and libraries by typing:

```console-bash
sudo yum groupinstall 'Development Tools'
```

Copy



## [Creating Virtual Environment](https://linuxize.com/post/how-to-install-python-3-on-centos-7/#creating-virtual-environment)

Python `Virtual Environments` allows you to install Python modules in an isolated location for a specific project, rather than being installed globally. This way you do not have to worry of affecting other Python projects.

The preferred way to create a new virtual environment in Python 3 is by executing the `venv` command.

Let’s say we want to create a new Python 3 project called `my_new_project` inside our user home directory and matching virtual environment.

First create the project directory and switch to it:

```console-bash
mkdir ~/my_new_projectcd ~/my_new_project
```

Copy

Activate Python 3.6 using the `scl` tool:

```console-bash
scl enable rh-python36 bash
```

Copy

From inside the project root run the following command to create a virtual environment named `my_project_venv`:

```console-bash
python -m venv my_project_venv
```

Copy

To use the virtual environment first we need to activate it by typing:

```console-bash
source my_project_venv/bin/activate
```

Copy

After activating the environment, the shell prompt will be prefixed with the name of the environment:

```sh
(my_project_venv) user@host:~/my_new_project$
```

Copy

Starting with Python 3.4, when creating virtual environments [pip, the package manager](https://linuxize.com/post/how-to-install-pip-on-centos-7/) for Python is installed by default.

## [Conclusion](https://linuxize.com/post/how-to-install-python-3-on-centos-7/#conclusion)

You should now have Python 3 programming environment setup on your CentOS 7 machine and you can start developing your Python 3 project.