---
layout: post
title:  "Git Common Usages"
date:   2015-09-03 15:28:32
categories: git
---


参考了以下网络资源：
廖雪峰Git官方教程，简单易懂，[点击这里](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

[Git常用命令总结](http://www.cnblogs.com/mengdd/p/4153773.html)

[git rebase 使用](http://blog.csdn.net/witsmakemen/article/details/22661605)

## git

- working tree：就是你所工作在的目录，每当你在代码中进行了修改，working tree的状态就改变了。 
- index file：是索引文件，它是连接working tree和commit的桥梁，每当我们使用git-add命令来登记后，index file的内容就改变了，此时index file就和working tree同步了。 
- commit：是最后的阶段，只有commit了，我们的代码才真正进入了git仓库。我们使用git-commit就是将index file里的内容提交到commit中。 

***

## git diff

- git diff：是查看working tree与index file的差别的。 
- git diff --cached：是查看index file 与commit的差别的。 
- git diff HEAD：是查看working tree和commit的差别的。（你一定没有忘记，HEAD代表的是最近的一次commit的信息） 
- git diff master origin/master: 是查看远程服务器上与本地的差异。

***

## git reset

- git reset —hard "commit":
    * 1.替换引用的指向.引用指向新的提交ID;
    * 2.替换暂存区.替换后,暂存区的内容和引用指向的目录树一致;
    * 3.替换工作区.替换后,工作区的内容变得和暂存区一致,也和HEAD所指向的目录树内容相同.

- git reset —soft "commit":
    * 1.替换引用的指向.引用指向新的提交ID.即只更改引用的指向,不改变暂存区和工作区.

- git reset —mixed "commit" 或 git reset "commit":
    * 1.替换引用的指向.引用指向新的提交ID;
    * 2.替换暂存区.替换后,暂存区的内容和引用指向的目录树一致;即更改引用的指向及重置暂存区,但是工作区不变.

### 实例:

- git reset : 仅用HEAD指向的目录树重置暂存区,工作区不受影响,相当于将之前用git add命令更新到暂存区的内容撤出暂存区.引用也未改变,因为引用重置到HEAD相当于没有重置.

- git reset HEAD : 同上

- git reset — filename : 仅将文件filename的改动撤出暂存区,暂存区中其他文件不该变.相当于git add filename的反向操作.

- git reset HEAD filename : 同上

- git reset —soft HEAD^ : 工作区和暂存区不改变,但是引用向前回退一次.当对最新提交的提交说明或提交不满意更改时,撤销最新的提交一遍重新提交.

- git reset HEAD^ : 工作区不变,但是暂存区会回退到上一次提交之前,引用也会回退一次.

- git reset —mixed HEAD^ : 同上

- git reset —hard HEAD^ : 彻底撤销最近的提交.引用回退到前一次,而且工作区和暂存区都会回退到上一次提交的状态.自上一次以来的提交全部丢失.

***

## git checkout 

- git checkout "commit" [—] "paths"
    * 1."commit"是可选项,如果省略则相当于从暂存区进行检出.和reset命令大不相同:重置的默认值是HEAD,而检出的默认值是暂存区.
    * 2.因此重置一般用于重置暂存区(除非使用—hard,否则不重置工作区),而检出命令主要是覆盖工作区(如果"commit"不省略,也会替换暂存区中相应的文件).
    * 3.该命令不会改变HEAD的头指针,主要用于指定版本文件覆盖工作区中对应的文件.如果省略"commit",则会用暂存区的文件覆盖工作区的文件,否则用指定提交中的文件覆盖暂存区和工作区中的对应文件。

- git checkout "branch"
    * 1.会改变HEAD头指针.之所以后面的参数写作"branch",是因为只有HEAD切换到一个分支才可以对提交进行跟踪,否则仍然会进入“分离头指针“的状态.在“分离头指针“的状态下的提交并不能被引用关联到,从而可能丢失.所以该命令主要作用是切换分支.
    * 2.如果省略"branch"则相当于对工作区进行状态检查.

***

## git log

- git log -n : 选择显示前N条log信息。
- git log --stat -n ： -n代表前n条log信息， --stat代表显示简要的增改行数统计,每次提交文件的变更统计。
- git log -p -n ：　-p代表显示比上条更全面的信息，包括修改文件的内容等。
- git log --pretty=oneline : 一行显示，只显示哈希值和提交说明。
- git log --graph : 简单图形方式表示。
- git log --pretty=format:" " : 按照预定的格式进行显示，例如：git log --pretty=format:"%h %s" --graph。

    控制显示的记录格式，常用的格式占位符写法及其代表的意义如下：　

    ```
    %H  提交对象（commit）的完整哈希字串
    %h  提交对象的简短哈希字串
    %T  树对象（tree）的完整哈希字串
    %t  树对象的简短哈希字串
    %P  父对象（parent）的完整哈希字串
    %p  父对象的简短哈希字串
    %an 作者（author）的名字
    %ae 作者的电子邮件地址
    %ad 作者修订日期（可以用 -date= 选项定制格式）
    %ar 作者修订日期，按多久以前的方式显示
    %cn 提交者(committer)的名字
    %ce 提交者的电子邮件地址
    %cd 提交日期
    %cr 提交日期，按多久以前的方式显示
    %s  提交说明
    ```

    例如如下操作：

    ```
    $ git log --pretty=format:"%h -%an,%ar : %s" -3
    d0b9a20 -BeginMan,24 hours ago : ok
    8c186cd -BeginMan,24 hours ago : mi
    b2a3100 -BeginMan,24 hours ago : what?
    ```

    显示了前3条的信息，简单的哈希值，作者，提交时间，提交说明。

- git指定路径、日期、关键字、作者等信息

    * 指定项目路径下的所有以install.md结尾的文件的提交历史:git log --pretty=oneline *install.md
    * 如两天前的提交历史：git log --since=2.days
    * 如指定作者为"BeginMan"的所有提交:$ git log --author=BeginMan
    * 如指定关键字为“init”的所有提交：$ git log --grep=init
    * 如指定提交者为"Jack"的所有提交：$ git log --committer=Jack
    (注意作者与提交者的关系：作者是程序的修改者，提交者是代码提交人。)
    * 如指定2天前，作者为“BeginMan”的提交含有关键字'init'的前2条记录：$ git log --since=2.days --author=BeginMan --grep=init -2

    注意：上面选项后面的参数可以带单双引号，如--author="BeginMan"

    使用说明如下：

    ```
    -(n) 仅显示最近的 n 条提交
    --since, --after 仅显示指定时间之后的提交。
    --until, --before 仅显示指定时间之前的提交。
    --author 仅显示指定作者相关的提交。
    --committer 仅显示指定提交者相关的提交。
    ```

    看一个实际的例子，如果要查看 Git 仓库中，2008 年 10 月期间，Junio Hamano 提交的但未合并的测试脚本（位于项目的 t/ 目录下的文件），可以用下面的查询命令：

    ```
    git log --pretty="%h - %s" --author=gitster --since="2008-10-01" --before="2008-11-01" --no-merges -- t/
    ```

- git log 命令支持的选项

    ```
    -p 按补丁格式显示每个更新之间的差异。
    --stat 显示每次更新的文件修改统计信息。
    --shortstat 只显示 --stat 中最后的行数修改添加移除统计。
    --name-only 仅在提交信息后显示已修改的文件清单。
    --name-status 显示新增、修改、删除的文件清单。
    --abbrev-commit 仅显示 SHA-1 的前几个字符，而非所有的 40 个字符。
    --relative-date 使用较短的相对时间显示（比如，“2 weeks ago”）。
    --graph 显示 ASCII 图形表示的分支合并历史。
    --pretty 使用其他格式显示历史提交信息。可用的选项包括 oneline，short，full，fuller 和 format（后跟指定格式）。
    ```


