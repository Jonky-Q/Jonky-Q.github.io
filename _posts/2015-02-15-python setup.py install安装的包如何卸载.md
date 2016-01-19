---
layout: post
title:  "python setup.py install安装的包如何卸载"
date:   2015-02-15 12:23:32
categories: python
---
python很好用，尤其是用过easy_install的朋友更是觉得它的便捷，
卸载命令也很简单 
```
easy_install -m package-name
```

但是面对源码安装的怎么办呢？
`setup.py` 帮助你纪录安装细节方便你卸载
```
python setup.py install —record log
```
这时所有的安装细节都写到 `log` 里了。
想要卸载的时候
```
cat log ｜ xagrs rm －rf
```
就可以干净卸载了