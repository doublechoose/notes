# 在ubuntu 安装swift for tensorflow



## 下载swift for tensorflow压缩包

安装详情：https://github.com/tensorflow/swift/blob/master/Installation.md

下载链接：https://storage.googleapis.com/swift-tensorflow/ubuntu16.04/swift-tensorflow-DEVELOPMENT-2018-10-17-a-ubuntu16.04.tar.gz  10月17,2018版本



```bash
# 安装必要的依赖
sudo apt-get install clang libcurl3 libicu-dev libpython-dev libncurses5-dev

# 下载最新的swift-tensorflow-<VERSION>-<PLATFORM>.tar.gz 即上面的下载链接，最新的按照安装详情页面的链接获取。
wget https://storage.googleapis.com/swift-tensorflow/ubuntu16.04/swift-tensorflow-DEVELOPMENT-2018-10-17-a-ubuntu16.04.tar.gz

# 解压
tar xzf swift-tensorflow-<VERSION>-<PLATFORM>.tar.gz

# 设置path
export PATH=$(pwd)/usr/bin:"${PATH}"


```

打开 `.bashrc` 文件：

```
$ nano ~/.bashrc1
```

在文件末尾添加：

```
$ export PATH=你解压的地方/usr/bin:"${PATH}"
```