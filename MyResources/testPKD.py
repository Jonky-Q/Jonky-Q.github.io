#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: qy
# @Date:   2015-12-03 14:46:27
# @Last Modified by:   qy
# @Last Modified time: 2015-12-16 10:32:29


import pickle
import re
import random

ll = [1,2,3,3,2,5,6]
ll2 = ['g','k']

lT = []

lT.extend(ll)
lT.extend(ll2)
print(lT)

# setdata = ([1,2])
ss = set([3,4])
setdata = set(ll)


# ppp = ss | setdata
print(list(setdata))

strC = 'ppp'
iRR = 124

listTT = []

listTT.append(tuple(['aaa', 999]))
listTT.append(tuple([strC, iRR]))
listTT.append(tuple(['kkk', 789]))

list.sort(listTT, key=lambda x:x[1])

print(listTT)

# ii = 0
# llout = []
# fileWLName = 'WordList.txt'
# with open(fileWLName, 'r') as fRead:
#     for line in fRead:
#         if (ii < 30):
#             llout.append(line.replace('\n', ''))
#         ii += 1

# print(llout)


# fWL = open(fileWLName, 'r+')
# sss = fWL.read()
# lC = sss.split('\n')
# for i in range(len(lC)):
#     if (i > 10000 and i < 11100):
#         print(lC[i])


ff = open('1-dumpPickle.pkl', 'rb')
# fdata = pickle.load(ff, fix_imports=True, encoding='utf-8')
fdata = pickle.load(ff)
fp = open('33.txt', 'w+')
strTT = ''
for i in range(1):
    listR = fdata[i]
    fp.write('title:' + listR['title'] + '\n')
    fp.write('Keyword:' + listR['Keyword'] + '\n')
    fp.write('Abstract:' + listR['Abstract'] + '\n')
    fp.write('Content:' + listR['Content'] + '\n')
    fp.write('------------------------------------------------------------------------------------' + '\n')

    strTT = listR['title'] + listR['Keyword'] + listR['Abstract'] + listR['Content'] + 'end!!'

print(strTT)

# fileName='201511030.mallet.summary'
# stringArr = []
# iNN = 0
# with open(fileName, 'r') as f:
#     for lineC in f:
#         iNN += 1
#         listC = lineC.split('\t')
#         listC[1] = int(listC[1].replace('\n', ''))
#         stringArr.append(listC[0])
#         ipos = listC[0].find('{d}')
#         if ( -1 != ipos ):
#             strINum = listC[0].replace('{d}', str(random.randint(1, 100)))
#             print(strINum)
#         else:
#             print('&&' + listC[0])
#         if ( iNN % 500 == 0 ):
#             break