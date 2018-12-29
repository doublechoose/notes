# jupyterhub with kubernetes 

安装kubectl

linux：

下载最新版本：

```
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
```

使kubectl二进制可执行

````
chmod +x ./kubectl
````

将二进制文件移动到PATH中

```
 sudo mv ./kubectl /usr/local/bin/kubectl
```

## zero to jupyterHub with Kubernetes

安装Helm

Helm是Kubernetes的包管理工具，用于安装、升级和管理在一个Kubernetes集群的应用。

Helm的包叫charts。我们将使用Helm chart安装和管理JupyterHub在Kubernetes集群。

#### 安装

最简单的方式：

```
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
```

#### 初始化

安装完helm后，初始化Helm在你的Kubernetes集群上：

1. Set up a [ServiceAccount](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/) for use by `tiller`.

```
kubectl --namespace kube-system create serviceaccount tiller
```

[conjure-up](http://conjure-up.io/) 为多种云和裸机提供了在 Ubuntu 上部署 Kubernetes 的最快方式。它提供了一个用户友好的界面，提示您输入云凭证和配置选项。

```
sudo snap install conjure-up --classic
# 如果您刚刚才安装 Snap，那么可能需要重新登录
conjure-up kubernetes
```



注： 上面zero to jupyterHub with kubernetes 没跟着操作走下去，不熟kubernetes。

看到**embeddable-jhub-sample**里有一个minikube-config.yaml文件。从minikube入手

### 安装minikube

https://github.com/kubernetes/minikube/releases

```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.32.0/minikube-linux-amd64 && chmod +x minikube && sudo cp minikube /usr/local/bin/ && rm minikube
```

要先安装virtualenv



启动minikube

```
minikube start
```

报错 

```
Running pre-create checks...
Error with pre-create check: "We support Virtualbox starting with version 5. 
Your VirtualBox install is \"
WARNING: The vboxdrv kernel module is not loaded. 
Either there is no module available for the current kernel (4.8.0-56-generic) or it failed to load. 
Please recompile the kernel module and install it by sudo /sbin/vboxconfig
You will not be able to start VMs until this problem is fixed.\\n5.1.22r115126\". 
Please upgrade at https://www.virtualbox.org"
```



sudo apt-get install virtualbox-dkms



pip install -e .

pip install -e . # 安装当前目录已打包好的项目 