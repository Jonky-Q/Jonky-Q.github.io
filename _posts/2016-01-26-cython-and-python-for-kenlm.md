---
layout: post
title:  "cython and python for kenlm"
date:   2016-01-26 11:23:55
categories: python cython kenlm
---

# Kenlm相关知识
[Kenlm下载地址](http://www.kheafield.com/code/kenlm/)
[kenlm中文版本训练语言模型](http://www.smallqiao.com/124790.html)
[如何使用kenlm训练出来的模型C++版本](http://www.smallqiao.com/124791.html)

## 关于Kenlm模块的使用及C++源码说明

###加载Kenlm模块命令
>qy@IAT-QYVPN:~/Documents/kenlm/lm$ ../bin/query -n test.arpa
***
###Kenlm模块C++源码说明
query的主入口文件:query_main.cc
query的执行函数文件:ngram_query.hh
`注意:`
默认执行的是query_main.cc文件96行的
```c
Query<ProbingModel>(file, config, sentence_context, show_words);
```
而不是lm/wrappers/nplm.hh,这个封装文件是需要NPLM模块的,参考以下代码,当时疏忽了在这个地方耽误了一些时间
```c
#ifdef WITH_NPLM
    } else if (lm::np::Model::Recognize(file)) {
      lm::np::Model model(file);
      if (show_words) {
        Query<lm::np::Model, lm::ngram::FullPrint>(model, sentence_context);
      } else {
        Query<lm::np::Model, lm::ngram::BasicPrint>(model, sentence_context);
      }
#endif
```
**关于Model类的继承关系**
> * 最基类`virtual_interface.hh` lm::base::Model
> * 次基类`facade.hh` lm::base::ModelFacade : public Model
> * 子类`model.hh` lm::ngram::GenericModel : public base::ModelFacade<GenericModel<Search, VocabularyT>, State, VocabularyT>

# 关于cython的简单说明
[cython官网](http://cython.org/)
可以从官网下载最新版本,参考Documentation分类中的Cython Wiki和Cython FAQ了解一些知识。
[cython-cpp-test-sample](https://github.com/sturlamolden/cython-cpp-test)
[Wrapping C++ Classes in Cython](https://github.com/cython/cython/wiki/WrappingCPlusPlus)
[cython wrapping of base and derived class](http://stackoverflow.com/questions/18344391/cython-wrapping-of-base-and-derived-class)
[std::string arguments in cython](http://comments.gmane.org/gmane.comp.python.cython.user/266)
[Cython and constructors of classes](http://stackoverflow.com/questions/13201886/cython-and-constructors-of-classes)
[Cython基础--Cython入门](http://blog.csdn.net/i2cbus/article/details/18181637)

# kenlm的python模块封装
接下来，让我们进入正题，在kenlm的源码中实际上已经提供了python的应用。在`kenlm/python文件夹`中，那么为什么还要再封装python模块呢，因为kenlm中所带的python模块仅仅实现了包含`<s>和</s>`这种情况下的计算分数的方法，而没有提供不包含这种情况的计算分数的算法，这就是为什么要重新封装python模块的原因。
## 简单介绍一下python模块使用的必要步骤
> * 安装kenlm.so模块到python的目录下，默认直接运行`kenlm目录下`的setup.py文件即可安装成功`sudo python setup.py install --record log`。
> * 安装成功后，即可运行`python example.py`文件，查看运行结果。

## 如何扩展kenlm的python模块
接下来，正式进入python扩展模块的介绍。`kenlm.pxd`是cython针对所用到C++类及对象的声明文件，`kenlm.pyx`是真正要编写的cython功能代码，也是未来python所要调用的类及方法。使用cython的编译命令，可以把`kenlm.pxd`和`kenlm.pyx`编译出`kenlm.cpp`文件。`setup.py`文件会用到编译出来的`kenlm.cpp`文件。
> * cython编译命令`cython --cplus kenlm.pyx`

### 扩展后的kenlm.pxd文件
```c
from libcpp.string cimport string

cdef extern from "lm/word_index.hh":
    ctypedef unsigned WordIndex

cdef extern from "lm/return.hh" namespace "lm":
    cdef struct FullScoreReturn:
        float prob
        unsigned char ngram_length

cdef extern from "lm/state.hh" namespace "lm::ngram":
    cdef struct State:
        pass

    ctypedef State const_State "const lm::ngram::State"

cdef extern from "lm/virtual_interface.hh" namespace "lm::base":
    cdef cppclass Vocabulary:
        WordIndex Index(char*)
        WordIndex BeginSentence() 
        WordIndex EndSentence()
        WordIndex NotFound()

    ctypedef Vocabulary const_Vocabulary "const lm::base::Vocabulary"


cdef extern from "lm/model.hh" namespace "lm::ngram":
    cdef cppclass Model:
        const_Vocabulary& GetVocabulary()
        const_State& NullContextState()
        void Model(char* file)
        FullScoreReturn FullScore(const_State& in_state, WordIndex new_word, const_State& out_state)

        void BeginSentenceWrite(void *)
        void NullContextWrite(void *)
        unsigned int Order()
        const_Vocabulary& BaseVocabulary()
        float BaseScore(void *in_state, WordIndex new_word, void *out_state)
        FullScoreReturn BaseFullScore(void *in_state, WordIndex new_word, void *out_state)
        void * NullContextMemory()

```

### 扩展后的kenlm.pyx文件
```c
import os

cdef bytes as_str(data):
    if isinstance(data, bytes):
        return data
    elif isinstance(data, unicode):
        return data.encode('utf8')
    raise TypeError('Cannot convert %s to string' % type(data))

cdef int as_in(int &Num):
    (&Num)[0] = 1

cdef class LanguageModel:
    cdef Model* model
    cdef public bytes path
    cdef const_Vocabulary* vocab

    def __init__(self, path):
        self.path = os.path.abspath(as_str(path))
        try:
            self.model = new Model(self.path)
        except RuntimeError as exception:
            exception_message = str(exception).replace('\n', ' ')
            raise IOError('Cannot read model \'{}\' ({})'.format(path, exception_message))\
                    from exception
        self.vocab = &self.model.GetVocabulary()

    def __dealloc__(self):
        del self.model

    property order:
        def __get__(self):
            return self.model.Order()
    
    def score(self, sentence):
        cdef list words = as_str(sentence).split()
        cdef State state
        self.model.BeginSentenceWrite(&state)
        cdef State out_state
        cdef float total = 0
        for word in words:
            total += self.model.BaseScore(&state, self.vocab.Index(word), &out_state)
            state = out_state
        total += self.model.BaseScore(&state, self.vocab.EndSentence(), &out_state)
        return total

    def full_scores(self, sentence):
        cdef list words = as_str(sentence).split()
        cdef State state
        self.model.BeginSentenceWrite(&state)
        cdef State out_state
        cdef FullScoreReturn ret
        cdef float total = 0
        for word in words:
            ret = self.model.BaseFullScore(&state,
                self.vocab.Index(word), &out_state)
            yield (ret.prob, ret.ngram_length)
            state = out_state
        ret = self.model.BaseFullScore(&state,
            self.vocab.EndSentence(), &out_state)
        yield (ret.prob, ret.ngram_length)
    
    def full_scores_n(self, sentence):
        cdef list words = as_str(sentence).split()
        cdef State state
        state = self.model.NullContextState()
        cdef State out_state
        cdef FullScoreReturn ret
        cdef int ovv = 0
        for word in words:
            ret = self.model.FullScore(state,
                self.vocab.Index(word), out_state)
            yield (ret.prob, ret.ngram_length)
            state = out_state

    """""""""""
    """count scores when not included <s> and </s>"""
    """""""""""
    def score_n(self, sentence):
        cdef list words = as_str(sentence).split()
        cdef State state
        state = self.model.NullContextState()
        cdef State out_state
        cdef float total = 0
        for word in words:
            ret = self.model.FullScore(state,
                self.vocab.Index(word), out_state)
            total += ret.prob
            """print(total)"""
            state = out_state
        return total


    def __contains__(self, word):
        cdef bytes w = as_str(word)
        return (self.vocab.Index(w) != 0)

    def __repr__(self):
        return '<LanguageModel from {0}>'.format(os.path.basename(self.path))

    def __reduce__(self):
        return (LanguageModel, (self.path,))
```

