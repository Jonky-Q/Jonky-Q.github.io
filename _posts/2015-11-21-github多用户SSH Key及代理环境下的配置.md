---
layout: post
title:  "github多用户SSH Key及代理环境下的配置"
date:   2015-11-21 10:23:32
categories: github proxy multiuser
---

在我们使用github ssh key模式的时候可以充分享受其带来的便捷性，但也许在配置的过程中会遇到那么一点点恼人的小问题。
下面把我在配置过程遇到的问题及解决方案记录一下。

[原文链接](http://blog.csdn.net/itmyhome1990/article/details/42643233)

***

##多个Github账号共存的问题

一台电脑上有一个ssh key，在github上提交代码，由于其他原因，你可能会在一台电脑上提交到不同的github上，怎么办呢...

### 1. 生成并添加第一个ssh key

> $ ssh-keygen -t rsa -C "youremail@xxx.com"

在Git Bash中执行命令一路回车，会在~/.ssh/目录下生成id_rsa和id_rsa.pub两个文件,用文本编辑器打开id_rsa.pub里的内容，在Github中添加SSH Keys。

### 2. 生成并添加第二个ssh key

> $ ssh-keygen -t rsa -C "youremail@xxx.com"

这次不要一路回车了，给这个文件起一个名字 不然默认的话就覆盖了之前生成的第一个。

![Pic1](http://img0.tuicool.com/fyE7ve.png!web)

假如起名叫my,目录结构如下：

![Pic2](http://img2.tuicool.com/eAJRja.png!web)

如果生成的第二个ssh key不在.ssh/下，可移动到此目录

### 3.如果生成的第二个ssh key不在.ssh/下，可移动到此目录


```
Host github.com
  HostName github.com
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_rsa
Host my.github.com
  HostName github.com
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/my
```

Host名字随意，接下来会用到。

### 4.测试配置是否正确

![Pic3](http://img0.tuicool.com/faa2Ef.png!web)

如果出现Hi xxx!You've successfully authenticated 就说明连接成功了

***

关于git服务器两种不同的做法：

#### 1.本地已经创建或已经clone到本地： 

打开.git/config文件

```
#更改[remote "origin"]项中的url中的
#my.github.com 对应上面配置的host
[remote "origin"]
  url = git@my.github.com:itmyline/blog.git
```

或者在Git Bash中提交的时候修改remote

```
$ git remote rm origin
$ git remote add origin git@my.github.com:itmyline/blog.git
```

#### 2.clone仓库时对应配置host对应的账户

```
#my.github.com对应一个账号
git clone git@my.github.com:username/repo.git
```


### 5.git ssh使用代理

[git ssh使用代理](http://ju.outofmemory.cn/entry/109979)

[在Mac OSX上通过SSH代理实现github访问](http://ju.outofmemory.cn/entry/129361)

[利用 HTTPS 代理访问 GitHub](http://blog.yxwang.me/2010/05/git-through-https-proxy/)

### 6.我在Ubuntu上的配置文件

```
Host *.workdomain.com
User qiy
IdentityFile ~/.ssh/id_rsa

Host github.com
User 17630287@qq.com
Hostname ssh.github.com
PreferredAuthentications publickey
ProxyCommand corkscrew 172.30.1.35 8081 %h %p
IdentityFile ~/.ssh/id_rsa_github
Port 443
```

[How to use SSH Via HTTP Proxy using Corkscrew in Ubuntu](http://www.ubuntugeek.com/how-to-use-ssh-via-http-proxy-using-corkscrew-in-ubuntu.html)