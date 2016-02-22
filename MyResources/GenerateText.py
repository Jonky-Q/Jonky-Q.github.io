#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: qy
# @Date:   2015-11-26 15:31:03
# @Last Modified by:   qy
# @Last Modified time: 2015-12-11 15:27:15

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import nltk
import random
# import numpy
import pickle
from string import punctuation 
import time
# import matplotlib

strFSign = "[\s+\.\!\/_,$%^*(+\"\']+|[+——！，；“”。？：、~@#￥%……&*（）]+ "


# from nltk.parse.generate import generate, demo_grammar
# from nltk import CFG

# demo_grammar1 = """
#   S -> NP VP
#   NP -> Det N
#   PP -> P NP
#   VP -> 'slept' | 'saw' NP | 'walked' PP
#   Det -> 'the' | 'a'
#   N -> 'man' | 'park' | 'dog'
#   P -> 'in' | 'with'
# """
# grammar1 = CFG.fromstring(demo_grammar1)
# print(grammar1)

# for sentence in generate(grammar1, depth=6, n=10):
#     print(' '.join(sentence))

def makePairs(arr):
    pairs = []
    for i in range(len(arr)):
        if i < len(arr)-1: 
            temp = (arr[i], arr[i+1])
            pairs.append(temp)
    return pairs

def generate(cfd, word = 'the', num = 50):
    numKeyWord = random.randint(10, 18)
    numTitle = random.randint(8, 18)
    numAbstract = random.randint(300, 460)

    listResult = []
    strRR = ''
    strKeyW = word
    strAbstract = ''
    listK = []

    bWriteAbstract = False
    iRandAbstract = random.randint(1, 100)

    bWriteTitle = False
    strTitle = ''
    iRandT = random.randint(1, num-100)
    for ik in range(numKeyWord):
        ikey = random.randint(1, num-1)
        listK.append(ikey)

    for i in range(num):
        arr = []                                      # make an array with the words shown by proper count
        for j in cfd[word]:
            for k in range(cfd[word][j]):
                arr.append(j)
        
        strRR = strRR + word
        # print(len(arr))
        # print(int(len(arr)*random.random()))
        word = arr[int(len(arr)*random.random())]     # choose the word randomly from the conditional distribution
        
        for ikk in range(len(listK)-1):
            if ( i == listK[ikk] ):
                if ( len(word) > 3):
                    strKeyW = strKeyW + ' ' + word

        if ( i == iRandT ):
            bWriteTitle = True
        if (bWriteTitle and numTitle > 0):
            if ( -1 == strFSign.find(word) ):
                strTitle = strTitle + word
                numTitle -= 1

        if ( i == iRandAbstract ):
            bWriteAbstract = True
        if (bWriteAbstract and numAbstract > 0):
            strAbstract += word
            numAbstract -= 1

    # strTitle = strTitle.translate(None, punctuation)

    listResult.append(strTitle)
    listResult.append(strKeyW)
    listResult.append(strAbstract)
    listResult.append(strRR)
    return listResult

# I'm gonna make a method so I can do it a bunch of times really easily.
# 一篇字数1520, 代码中以词为单位
def makeText(fileName, word = 'the', num = 100):
    
    stringArr = []
    with open(fileName, 'r') as f:
        for lineC in f:
            stringArr.extend(lineC.split())

    print('File split success!!')
    print(time.strftime('%H:%M:%S',time.localtime(time.time())))
    
    pairs = makePairs(stringArr)
    print('File makePairs success!!')
    print(time.strftime('%H:%M:%S',time.localtime(time.time())))
    model = nltk.ConditionalFreqDist(pairs)
    print('nltk.ConditionalFreqDist success!!')
    print(time.strftime('%H:%M:%S',time.localtime(time.time())))
    # pairs = []

    dumpPaper = open('1-nltk-dumpPaper.pkl', 'wb')

    listTotalR = []
    for iPaper in range(1):
        numContent = random.randint(6600, 20800)
        indexW = random.randint(0, len(stringArr)-1)
        listR = generate(model, stringArr[indexW], numContent)
        paperDict = {'title':listR[0], 'Keyword':listR[1], 'Abstract':listR[2], 'Content':listR[3]}

        listTotalR.append(paperDict)
        print(str(iPaper+1) + '-' +'Paper Title:' + listR[0])
        # print(listR[1] + '\n')
        # print(listR[2] + '\n')
        print(time.strftime('%H:%M:%S',time.localtime(time.time())))

    pickle.dump(listTotalR, dumpPaper, protocol=2)

makeText('22.txt')                 # sweet. Now all I have to do is input a file name.李克强

