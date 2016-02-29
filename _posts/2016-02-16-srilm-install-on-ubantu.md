---
layout: post
title:  "Srilm install on Ubantu"
date:   2016-02-16 9:34:32
categories: Srilm
---


之前研究过kenlm语言模型，主要用来评估词与词之间可能的概率，由于工作需要，开始研究一下srilm语言模型。现记录一下安装过程，总结一下以备后用。

在32位ubantu系统上安装成功，后续准备在64位系统上也再测试一遍。

参考了网上一些文章如下：

[Ubuntu 64位系统下SRILM的配置详解](http://www.linuxidc.com/Linux/2009-06/20313.htm)

[Ubuntu 11.04 32位系统下 SRILM 的配置详解](http://blog.csdn.net/zhoubl668/article/details/7759370)

[ubuntu 编译安装 srilm](http://www.cnblogs.com/shanguanghui/p/3655808.html) : 这篇还是不错的。

[Ubuntu 12.04.5 下安装SRILM1.7.1](http://blog.csdn.net/wwjiang_ustc/article/details/50317691) : 这篇博文有好几处错误，害我耽误了不少时间，坑人呀。 路径`/home/xxx/srilm-1.7.1`这种格式的路径很可能导致无法进行编译。
`TCL_INCLUDE`和 `TCL_LIBRARY`根本无需修改。修改`GAWK = /usr/bin/awk`出现笔误。



## 安装依赖软件包

 1. c/c++ compiler：编译器gcc 3.4.3及以上版本，我的是gcc 4.8

 2. GNU make：构建和管理工程的工具，解释Makefile里的指令，描述了整个工程所有文件的编译顺序和编译规则。这里是为了控制SRILM的编译和安装。

 3. GNU gawk：GNU所做的awk程序语言。对于文字资料的修改，对比，抽取等处理，使用c或passcal等不方便且费时，awk能够以很短的程序完成。这里是处理SRILM里的一些脚本文件。`sudo apt-get install gawk`

 4. GNU gzip：使用c语言编写的一种解压缩软件。这里是为了使SRILM能够处理.Z和.GZ后缀的压缩文件。

 5. bzip2：数据压缩软件，压缩效率更高。这里是使SRILM能处理.bz2后缀的压缩文件。

 6. P7zip：数据压缩软件。这里是使SRILM能处理7-zip的压缩文件。`sudo apt-get install p7zip-rar`

 7. Tcl可嵌入式脚本语言。用于脚本编程和测试。这里是为了SRILM的测试。最好安装tcl8.x和tcl8.x-dev。
[源码安装可参考](http://blog.csdn.net/zqt520/article/details/7342171)。 或者直接用命令安装`sudo apt-get install tcl`，我选择的是后者。
如果有问题，可以尝试安装`sudo apt-get install tcl-dev tk-dev` 或者 `sudo apt-get install libc6-dev-amd64`

 8. csh：Unix shell的一种。（这个很重要，安装过程中有个问题困扰了很久，最后发现是csh没有安装的原因）。
[csh配置可参考](http://blog.sina.com.cn/s/blog_78699cbf010169vi.html)
我用命令安装的`sudo apt-get install csh`


## 安装过程

### 一 下载SRILM.tgz压缩包

[安装包服务器路径](http://www.speech.sri.com/projects/srilm/download.html)，把压缩包解压。我这里使用的是1.7.0版，安装目录是：/home/qy/srilm

### 二 修改Makefile文件（srilm目录下）

 1. 找到此行： # SRILM = /home/speech/stolcke/project/srilm/devel，另起一行输入srilm的安装路径，SRILM = /home/qy/srilm

 2. 找到此行：MACHINE_TYPE := $(shell $(SRILM)/sbin/machine-type)，在其前加＃注释掉，并另起一行输入：MACHINE_TYPE := i686-gcc4。此行告诉Makefile之后要看的设置在/home/qy/srilm/common/Makefile.machine.i686-gcc4中。

通过 uname -m 命令可以查询机器架构是i686，如果系统是 64 位的，请改为 i686-m64(此时对应的文件应该是`/home/qy/srilm/common/Makefile.machine.i686-m64`)，同时也可能需要修改相应的 sbin/machine-type。

### 三 把Ubuntu系统的相关设定告诉Makefile

#### 1. 修改GCC配置项

32位系统下

修改如下位置文件 `/home/qy/srilm/common/Makefile.machine.i686-gcc4`

```
#GCC_FLAGS = -mtune=pentium3 -Wall -Wno-unused-variable -Wno-uninitialized
GCC_FLAGS = -mtune=generic -Wall -Wno-unused-variable -Wno-uninitialized
CC = $(GCC_PATH)gcc $(GCC_FLAGS) -Wimplicit-int
CXX = $(GCC_PATH)g++ $(GCC_FLAGS) -DINSTANTIATE_TEMPLATES
```

这里是为了告诉SRILM系统使用的compiler(c和c++)，符合安装情况，不需要修改。

如果为64位系统，参考以下：

```
#GCC_FLAGS = -mtune=pentium3 -Wall -Wno-unused-variable -Wno-uninitialized
GCC_FLAGS = -march=athlon64 -m64 -Wreturn-type -Wimplicit
CC = $(GCC_PATH)gcc $(GCC_FLAGS) -Wimplicit-int
CXX = $(GCC_PATH)g++ $(GCC_FLAGS) -DINSTANTIATE_TEMPLATES
```

#### 2. 修改TCL相关项

```
# Tcl support (standard in Linux)
TCL_INCLUDE =
TCL_LIBRARY =
NO_TCL = 1 (增加此项目)
```
这里是为了告诉SRILM函数库（TCL）在系统中的安装位置，符合安装情况，不需要修改。

#### 3. 修改GAWK相关项

GAWK = /usr/bin/awk
修改为：GAWK = /usr/bin/gawk


### 四 修改环境变量

**环境变量我没进行修改**

输入命令：sudo gedit /etc/profile

找到：

```
if [ "$PS1" ]; then
　if [ "$BASH" ]; then
　　PS1=’u@h:w$ ‘
　　if [ -f /etc/bash.bashrc ]; then
　　　. /etc/bash.bashrc
　　fi
　else
　　if [ "`id -u`" -eq 0 ]; then
　　　PS1=’# ‘
　　else
　　　PS1=’$ ‘
　　fi
　fi
fi
```

在其后另起一行输入：export PATH=”$PATH:/home/qy/srilm/bin/i686-m64:/home/qy/srilm/bin” (注意32位系统和64位系统写法会有区别)


### 五 编译srilm

切换到源码路径`/home/qy/srilm`

`make World`

### 六 测试srilm

编译成功后，直接运行 `make test`

```
*** Running test ngram-server ***

0.21user 0.72system 0:06.56elapsed 14%CPU (0avgtext+0avgdata 0maxresident)k

0inputs+8outputs (0major+2559minor)pagefaults 0swaps

ngram-server: stdout output IDENTICAL.

ngram-server: stderr output IDENTICAL.

 

*** Running test ppl-counts ***

0.10user 0.24system 0:00.32elapsed 104%CPU (0avgtext+0avgdata 0maxresident)k

0inputs+16outputs (0major+4724minor)pagefaults 0swaps

ppl-counts: stdout output IDENTICAL.

ppl-counts: stderr output IDENTICAL.
```

需要等待一段时间，如果出现多是IDENTICAL,很少的DIFFERS，就证明srilm编译成功了！