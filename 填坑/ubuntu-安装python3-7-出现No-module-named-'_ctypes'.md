问题：[Python3: ImportError: No module named '_ctypes' when using Value from module multiprocessing](https://stackoverflow.com/questions/27022373/python3-importerror-no-module-named-ctypes-when-using-value-from-module-mul)

环境ubuntu 16.04

安装python3.7出现问题

步骤：

- 下载python源码

- 执行命令

  - ```
    ./configure
    make
    make install
    ```

解决：

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install libffi-dev
```

libffi用于高级语言之间的相互调用。
