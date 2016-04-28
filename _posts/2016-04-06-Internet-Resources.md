---
layout: post
title:  "各类互联网技术资源汇总"
date:   2016-04-06 15:23:32
categories: Resources
---

以下内容均来自互联网，在工作或学习中使用的技术或方法，汇总于此，以备后用。

[如何在Ubuntu Linux上升级Oracle Java](http://zh.wikihow.com/%E5%9C%A8Ubuntu-Linux%E4%B8%8A%E5%8D%87%E7%BA%A7Oracle-Java)

[Linux命令之大文件切分与合并](http://www.2cto.com/os/201408/326881.html)

[Python调用C/C++的种种方法](http://blog.csdn.net/fxjtoday/article/details/6059874)

[引用外部jar包生成jar文件](http://blog.csdn.net/luoweifu/article/details/7791712)

[打包jar时Class-Path的配置方式](http://blog.csdn.net/zhouyong0/article/details/7517055)

***

```
##Jena环境变量设置

Jena3.0版本要求JDK必须要8.0以上版本，需要官网下载Jena及JDK对应的版本，并配置环境变量。

/etc/profile
#set 1.7.0_79 jdk environment
#export JAVA_HOME=/opt/jdk1.7.0_79
#export JRE_HOME=/opt/jdk1.7.0_79/jre
#export CLASSPATH=.:$CLASSPATH:$JAVA_HOME/lib:$JRE_HOME/lib
#export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin

#set 1.8 jdk environment
export JAVA_HOME=/opt/jdk1.8.0_73
export JRE_HOME=/opt/jre1.8.0_73
export CLASSPATH=.:$CLASSPATH:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin

#set jena
export JENAROOT=/opt/jena-3.0.1
export CLASSPATH=.:$CLASSPATH:$JENAROOT/lib
export PATH=$PATH:$JENAROOT/bin
```
