---
layout: post
title:  "语义网相关知识整理"
date:   2016-03-16 09:23:32
categories: OWL Jena Protege RDF RDFS
---

以下内容为调查语义网过程中一些知识的积累及问题的总结，以备后用！


***

##相关资料整理

[Apache Jena](http://jena.apache.org/index.html)

Apache Jena的安装，需要注意一点就是 `apache-jena-3.0.1.tar.gz` 3.0版本需要 `Jena requires Java8 (from Jena version 3.0.0 onwards).` 如果是java7环境，可以安装2.X版本进行学习验证。

下载包解压后，只要配置好环境变量，Jena API就可以正常工作了，可通过 `sparql -version`命令进行验证是否配置正确。配置全局的环境变量，修改/etc/profile, 在文件末尾添加以下内容

```
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

如果用JAVA开发环境，只要把Jena包中的`lib`文件夹中的所有Jar包引入工程即可。

[Jena API Manual](https://jena.apache.org/documentation/javadoc/jena/index.html?overview-summary.html)

***

一些相关Jena的中文资料

[Jena API详解（关注本体持久化到MySQL后的操作）](http://echo.vars.me/Jena-API/)

[jena学习思路](http://akunamotata.iteye.com/blog/451084)

[RDF API – Jena 手册](http://www.flykun.com/rdf-api-jena-%E6%89%8B%E5%86%8C/)

[RDF 教程](http://www.it535.com/Index-show-375-2083-374.html)

[建立语义网搜索](http://www.cnblogs.com/tingzi/archive/2012/04/16/2452597.html)

***

一些相关Jena的外文资料

[owl实体库下载](http://smi-protege.stanford.edu/svn/owl/trunk/etc/?diff_format=u&sortdir=down&pathrev=17511&logsort=rev&sortby=rev)

[示例代码](http://www.programcreek.com/java-api-examples/index.php?ClassName=org.semanticweb.owlapi&submit=Search)

[owlapi官网](http://owlapi.sourceforge.net/documentation.html)

[Jena的Java示例代码库](http://www.programcreek.com/java-api-examples/index.php?api=com.hp.hpl.jena.ontology.OntModel)

[OWL 2 Web Ontology Language Primer (Second Edition)](https://www.w3.org/TR/2012/REC-owl2-primer-20121211/)

***

国内外常用流行本体库

[SUMO](http://www.ontologyportal.org/)

[WordNet](http://wordnet.princeton.edu/)

[OpenCyc](http://www.opencyc.org/doc/)

[DBPedia](http://dbpedia.org/About)

[HowNet](http://www.keenage.com/html/e_index.html)

***

关于语义网本体的一些资料

[知乎上关于语义网“本体”的讨论](http://www.zhihu.com/question/19558514?__nids__=151116)

[Protege工具官网](http://protege.stanford.edu/products.php#desktop-protege)

[Graphviz - Graph Visualization Software](http://www.graphviz.org/Download_linux_ubuntu.php)

Protege工具是管理语义实体的工具，目前有多个版本，如果基于Java7环境可以安装3.x或4.x等版本。如果安装5.x以上的版本需要Java8的环境。

Graphviz是Protege工具的可视化插件，需要另行安装，注意x86版本或x64版本。

在我的64位Ubantu系统中，安装了Protege-5.0.0-beta-24-linux.tar.gz，解压此文件夹，运行`run.sh`即可。
需要图形化支持，需要安装这三个依赖包graphviz_2.38.0-1-saucy_amd64.deb，libgraphviz4_2.38.0-1-saucy_amd64.deb，libgraphviz-dev_2.38.0-1-saucy_amd64.deb。安装成功后，打开Protege，在File->Preferences->OWLViz属性页中，`Dot Application Path`的选项中填写如下内容`/usr/bin/dot`

[http://bbs.w3china.org/index.asp]中文语义网论坛

***

##基本概念介绍

###RDF

RDF(Resource Description Framework)定义了一个简单的模型,用于描述资源,属性和值之间的关系。资源是可以用 URI 标识的所
有事物,属性是资源的一个特定的方面或特征,值可以是另一个资源,也可以是字符串。总的来说,一个 RDF 描述就是一个三元组: 

**对象――属性――值**

**主体――谓词――客体**

RDF是一个机制,用于描述数据。它不是一个语言，而是一个模型用于描述Web上数据。RDF是忽略语法的它仅仅提供一个模型用于表达元数据。这种可能的表达可以是有向图、列表或其他,当然XML也是一种可选的表达。

```
<rdf:RDF
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
xmlns:uni="http://www.mydomain.org/uni-ns">
<rdf:Description rdf:about="949318">
<uni:name>David Billington</uni:name>
<uni:title>Associate Professor</uni:title>
<uni:age rdf:datatype="&xsd:integer">27<uni:age>
</rdf:Description>
<rdf:Description rdf:about="CIT1111">
<uni:courseName>Discrete Maths</uni:courseName>
<uni:isTaughtBy>David Billington</uni:isTaughtBy>
</rdf:Description>
<rdf:Description rdf:about="CIT2112">
<uni:courseName>Programming III</uni:courseName>
<uni:isTaughtBy>Michael Maher</uni:isTaughtBy>
</rdf:Description>
</rdf:RDF>
```

###RDF Schema 概述

RDF Schema,使用了一些预先定义的词汇集,比如class、subpropertyof、subclassof,来指定特定的schema。RDF Schema是一个有效的RDF表达,就像XMLSchema是一个有效的XML表达。

subclassof允许开发者去定义每一个类的继承机制, subpropertyof对属性是一样的。属性的限制可以用domain和range结构来实现,
这个结构可以用来扩展词汇表RDF和RDF Schema可以用谓词逻辑刻画(为其子集),可以进行高效的自动推理。


```
<rdfs:Class rdf:ID="lecturer">
<rdfs:comment>
The class of lecturers. All lecturers are academic staff members.
</rdfs:comment>
<rdfs:subClassOf rdf:resource="#academicStaffMember"/>
</rdfs:Class>
<rdfs:Class rdf:ID="course">
<rdfs:comment>The class of courses</rdfs:comment>
</rdfs:Class>
<rdf:Property rdf:ID="isTaughtBy">
<rdfs:comment>
Inherits its domain ("course") and range ("lecturer")
from its superproperty "involves"
</rdfs:comment>
<rdfs:subPropertyOf rdf:resource="#involves"/>
</rdf:Property>
<rdf:Property rdf:ID="phone">
<rdfs:comment>
It is a property of staff members
and takes literals as values.
</rdfs:comment>
<rdfs:domain rdf:resource="#staffMember"/>
<rdfs:range rdf:resource="http://www.w3.org/2000/01/rdf-schema#Literal"/>
</rdf:Property>
```

###RDF 与 RDF Schema

*RDF 描述的 statement 为三元组:资源――属性――值,主体――谓词――客体
*RDF 有一个基于 XML 的语言
*RDF 是领域无关的,RDF Schema 提供了一种描述具体领域知识的机制
*RDF Schema 是最原始本体语言,提供了一套具有固定语义的建模原语
*RDF Schema 的核心概念是类、子类关系,属性、子属性关系
*RDF 和 RDF Schema 可以用谓词逻辑形式化刻画,存在高效的自动推理机

##实体

*Ontology为人类和应用程序系统提供了一个对于主题的共同理解
*Ontology为了不同来源的信息的合成,提供了一个共同的相关领域的理解
*Ontology为了在不同的应用程序之间共享信息和知识(用于互操作),描述应用程序的领域,定义术语及其关系
*Ontology 刻画领域的公共知识:基本概念和关系,以及基于它们的规则

###OWL 的三个子语言

OWL Lite
    *OWL DL 的一个子集,良好的可计算性
    *提供给那些只需要一个分类层次和简单约束的用户
OWL DL
    *基于描述逻辑,与一部分 RDF 不兼容,旨在支持已有的描述逻辑商业处理(business segment)和具有良好计算性质的推理系统
    *包括了 OWL 语言的所有成分,但有一定的限制,如类型的分离
    *保证计算的完全性,可判定性,计算复杂度较高,暂时没有完全的推理机实现
OWL Full
    *最强的表达能力,不可判定
    *支持那些需要尽管没有可计算性保证,但有最强的表达能力的用户

在表达能力和推理能力上,每个子语言都是前面的语言的扩展

```
<?xml version="1.0"?>
<rdf:RDF
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
xmlns:owl="http://www.w3.org/2002/07/owl#"
xmlns:dc="http://purl.org/dc/elements/1.1/"
xml:base="http://wasp.cs.vu.nl/sekt/ontology/animal">
<owl:Ontology rdf:about=“animal"/><owl:Class rdf:ID="Eagle">
<rdfs:subClassOf><owl:Class rdf:about="#Bird"/>
</rdfs:subClassOf></owl:Class><owl:Class rdf:ID="Animal"/>
<owl:Class rdf:ID="Fly"><owl:disjointWith>
<owl:Class rdf:about="#Penguin"/></owl:disjointWith>
<rdfs:subClassOf rdf:resource="#Animal"/>
</owl:Class><owl:Class rdf:ID="Bird">
<rdfs:subClassOf rdf:resource="#Fly"/>
</owl:Class>
<owl:Class rdf:ID="Penguin">
<rdfs:subClassOf rdf:resource="#Bird"/>
<owl:disjointWith rdf:resource="#Fly"/>
</owl:Class>
</rdf:RDF>
```


##Jena

###what is Jena
    *Jena is a Java framework for the creation of applications for the Semantic Web
    *Provides interfaces and classes for the creation and manipulation of RDF repositories
    *Also provides classes/interfaces for the management of OWL-based ontologies

###Capabilities of Jena
    *RDF API
    *Reading and writing in RDF/XML, N-Triples
    *OWL API
    *In-memory and persistent storage
    *SPARQL query engine

###RDF Concepts
    *Resources, Properties, Literals, Statements (Triples: <subj pred obj>)
    *A set of (related) statements constitute an RDF graph
    *The Jena RDF API contains classes and interfaces for every important aspect of the RDF specification
    *They can be used in order to construct RDF graphs from scratch, or edit existent graphs
    *These classes/interfaces reside in the com.hp.hpl.jena.rdf.model package
    *In Jena, the Model interface is used to represent RDF graphs
    *Through Model, statements can be obtained/ created/ removed etc