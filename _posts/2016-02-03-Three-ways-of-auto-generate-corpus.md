---
layout: post
title:  "Three ways of auto generate corpus"
date:   2016-02-03 16:28:32
categories: 自然语言处理
---


在做一些自然语言处理的工作时，如果想要进行一些大数据的训练及测试工作，常常因为没有足够多的数据而烦恼。以下整理了三种自动生成文章数据的方案，已备后用。


## 前期准备工作

生词文章首先我们需要一系列的词表。

可以参考生词词表脚本文件[GenerateWordList.py](https://github.com/JonkyQ/JonkyQ.github.io/blob/master/MyResources/GenerateWordList.py)，去掉了重复词，但没有统计词频，数字没有统一用符号替换（如果不做这一步，随机生成的文章中，带数字的词会比较多）。

也可参考之前完成的词表文件[201511030.mallet.summary](https://github.com/JonkyQ/JonkyQ.github.io/blob/master/MyResources/201511030.mallet.summary)


## 第一种方法

利用nltk条件频率算法自动生成随机文章可以参考[GenerateText.py](https://github.com/JonkyQ/JonkyQ.github.io/blob/master/MyResources/GenerateText.py)脚本文件。生成效果看起来不错，但速度很慢，不适合词表较大的情况。
此方法参考文章：使用马尔可夫模型自动生成文章


## 第二种方法

利用kenlm语言模型，从词表中随机抽取两个词，用互信息进行评分，取阀值以上的词。
可以利用[MdyKenlmGenerateText.py](https://github.com/JonkyQ/JonkyQ.github.io/blob/master/MyResources/MdyKenlmGenerateText.py)脚本，生成速度稍慢，但比第一种还是快很多的。

```
python MdyKenlmGenerateText.py --inputWordsFile 201511030.mallet.summary --GenFileN 10
```

## 第三种方法

完全随机法，利用随机函数从词表中取词，完全随机生成文章。包括一些段落和标点符号的随机添加。可以最快速度生成大量的数据文章。参考文件[MdyGenerateText.py](https://github.com/JonkyQ/JonkyQ.github.io/blob/master/MyResources/MdyGenerateText.py)

```
python MdyGenerateText.py --inputWordsFile 201511030.mallet.summary --GenFileN 10
```

## 备注

[testPKD.py](https://github.com/JonkyQ/JonkyQ.github.io/blob/master/MyResources/testPKD.py) , 验证随机生成文章数据正确性。