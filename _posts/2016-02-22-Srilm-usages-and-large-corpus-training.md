---
layout: post
title:  "Srilm usages and large corpus training"
date:   2016-02-22 17:08:14
categories: Srilm
---

在完成Srilm的安装工作后，接下来介绍一下Srilm的基本使用方法以及在训练大数据模型时所遇到的一些问题，记录在此，少走弯路！！
本次只记录基本的用法和大数据语料训练过程中所遇到的问题。

参考连接 

[语言模型训练工具Srilm的使用](http://www.jeepshoe.org/518919296.htm)

[语言模型训练工具SRILM详解](http://www.52nlp.cn/language-model-training-tools-srilm-details)

[A Toolkit For Langugae Modeling——SRILM使用记录](http://blog.csdn.net/a635661820/article/details/43939773)

[斯坦福大学自然语言处理第四课-语言模型（Language Modeling）](http://blog.csdn.net/xiaokang06/article/details/17965965)

## Srilm基本命令

 1.词频统计

`ngram-count -text trainfile.txt -order 3 -write trainfile.count`

其中-order 3为3-gram，trainfile.count为统计词频的文本

 2.模型训练

`ngram-count -read trainfile.count -order 3 -lm trainfile.lm  -interpolate -kndiscount`

其中trainfile.lm为生成的语言模型，-interpolate和-kndiscount为插值与折回参数

也可以合并上面二步，简单的生成arpa语言模型  

`ngram-count -text trainfile.txt -lm trainfile.lm`

这里没写-order，默认是3,没指定打折算法，默认使用Good-Turing打折和Katz退避算法

 3.测试（困惑度计算）

`ngram -ppl testfile.txt -order 3 -lm trainfile.lm -debug 2 > file.ppl`

其中testfile.txt为测试文本，-debug 2为对每一行进行困惑度计算，类似还有-debug 0 , -debug 1, -debug 3等，最后将困惑度的结果输出到file.ppl。

## 大数据模型训练

对于大量数据的语言模型训练不能使用上面的方法，有可能内存溢出失败，也有可能训练要很长时间。主要思想是将文本切分，分别计算，然后合并。步骤如下：

 1.切分数据
 
`split -l 10000 trainfile.txt filedir/`

即每10000行数据为一个新文本存到filedir目录下。

 2.对每个文本统计词频

`sh make-bath-counts filepath.txt 1 cat ./counts -order 3`

其中filepath.txt为切分文件的全路径，可以用命令实现：ls $(echo $PWD)/* > filepath.txt，**filepath.txt不要与分割后的语料放在同一个目录中**，运行成功会将统计的词频结果存放在counts目录下。

**注意**

很有可能在执行上述命令上遇到这样的错误 `merge-batch-counts: command not found` 由于在`merge-batch-counts`文件中存在目录不正确的问题，需要把`ngram-count -text $test_in -write $test_out`，修改为`i686-m64/ngram-count -text $test_in -write $test_out`。如果仍有错误，尝试修改路径就可以了，一定是路径不正确造成的。如果是32位系统应该修改为`i686-gcc4/ngram-count`

`merge-batch-counts`和`make-big-lm`同样要修改相关的内容，这里不详细列出了。

 3.合并counts文本并压缩

`merge-batch-counts ./counts`

 4.训练语言模型

`make-big-lm -read ../counts/*.ngrams.gz -lm ../split.lm -order 3` 

用法同ngram-counts

 5.测评（计算困惑度）

ngram -ppl filepath.txt -order 3 -lm split.lm -debug 2 > file.ppl

**测评数据举例**

可通过以上命令计算困惑度， -debug命令可以指定0-4，指定不同参数可以获得不同等级信息。

例如 `../bin/i686-gcc4/ngram -ppl testF.txt -lm split.lm -debug 2 > file.ppl`  testF.txt文件中包含要测试分词后的句子。file.ppl为结果文件。

输出如下：

```
reading 131709 1-grams
reading 2098031 2-grams
reading 1110011 3-grams
qy@IAT-QYVPN:~/srilm/myresult$ cat file.ppl 
新郑市 龙湖 镇
    p( 新郑市 | <s> )  = [1gram] 1.03163e-06 [ -5.98647 ]
    p( 龙湖 | 新郑市 ...)    = [2gram] 0.109008 [ -0.962542 ]
    p( 镇 | 龙湖 ...)  = [3gram] 0.761585 [ -0.118282 ]
    p( </s> | 镇 ...)    = [1gram] 0.000502077 [ -3.29923 ]
1 sentences, 3 words, 0 OOVs
0 zeroprobs, logprob= -10.3665 ppl= 390.51 ppl1= 2854.36

九 龙湾 首期
    p( 九 | <s> )    = [2gram] 7.13105e-05 [ -4.14685 ]
    p( 龙湾 | 九 ...)  = [2gram] 0.00259663 [ -2.58559 ]
    p( 首期 | 龙湾 ...)     = [3gram] 0.389889 [ -0.409059 ]
    p( </s> | 首期 ...)   = [1gram] 0.000374721 [ -3.42629 ]
1 sentences, 3 words, 0 OOVs
0 zeroprobs, logprob= -10.5678 ppl= 438.477 ppl1= 3331.16

我 爱 北京 天安门
    p( 我 | <s> )    = [2gram] 0.000142666 [ -3.84568 ]
    p( 爱 | 我 ...)   = [2gram] 0.00823891 [ -2.08413 ]
    p( 北京 | 爱 ...)  = [3gram] 0.0164494 [ -1.78385 ]
    p( 天安门 | 北京 ...)    = [2gram] 0.000178553 [ -3.74823 ]
    p( </s> | 天安门 ...)  = [1gram] 0.000264057 [ -3.5783 ]
1 sentences, 4 words, 0 OOVs
0 zeroprobs, logprob= -15.0402 ppl= 1018.68 ppl1= 5755.04

file testF.txt: 3 sentences, 10 words, 0 OOVs
0 zeroprobs, logprob= -35.9745 ppl= 585.154 ppl1= 3957.77
```