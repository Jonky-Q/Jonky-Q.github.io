#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: qy
# @Date:   2015-11-26 15:31:03
# @Last Modified by:   qy
# @Last Modified time: 2015-12-14 12:55:18

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import nltk
import random
import pickle
import time
import threading
import re
import getopt
# from string import punctuation 


lock = threading.Lock()
strFSign = "[\s+\.\!\/_,$%^*()+\"\']+|[+——！，；“”。？:《》：、~@#￥%……&*（）]+ "
listSing = ['。', ':', '，', '！','？']

def makePairs(arr):
    pairs = []
    for i in range(len(arr)):
        if i < len(arr)-1: 
            temp = (arr[i], arr[i+1])
            pairs.append(temp)
    return pairs

def generate(word = 'the', num = 50):
    numKeyWord = random.randint(10, 18)
    numTitle = random.randint(8, 18)
    numAbstract = random.randint(300, 460)
    numReturn = random.randint(10, int(num / 300))


    listResult = []
    strRR = ''
    strKeyW = word
    strAbstract = ''
    listK = []
    listReturn = []

    bWriteAbstract = False
    iRandAbstract = random.randint(1, 100)

    bWriteTitle = False
    strTitle = ''
    iRandT = random.randint(1, num-100)
    for ik in range(numKeyWord):
        ikey = random.randint(1, num-1)
        listK.append(ikey)

    iBeg = 1
    averageN = int((num-1) / numReturn)
    iEnd = averageN
    for iRet in range(numReturn):
        iRR = random.randint(iBeg, iEnd)
        listReturn.append(iRR)
        iBeg = iRR + 50
        iEnd = iEnd + averageN
        if (iEnd > num - 200 or iBeg > iEnd):
            # print('Return Num: ' + str(len(listReturn)))
            # print('Return Break!!!!!')
            break

    iConSing = random.randint(5, 20)
    iConNum = 0
    for i in range(num):
        # arr = []                                      
        # for j in cfd[word]:
        #     for k in range(cfd[word][j]):
        #         arr.append(j)
        
        global stringArr

        strRR = strRR + word
        iConNum += 1
        if (iConSing == iConNum):
            strRR += listSing[random.randint(0, len(listSing)-1)]
            iConNum = 0
            iConSing = random.randint(5, 20)

        # word = arr[int((len(arr))*random.random())]            
        word = stringArr[random.randint(0, len(stringArr)-1)]
        
        for iRn in range(len(listReturn)):
            if (i == listReturn[iRn]):
                strRR = strRR + listSing[0] + '\n'
                del listReturn[iRn]
                break

        for ikk in range(len(listK)-1):
            if ( i == listK[ikk] ):
                if ( len(word) > 3):
                    if (False == bool(re.search(r'\d', word))):
                        strKeyW = strKeyW + ' ' + word
                        del listK[ikk]
                        break

        if ( i == iRandT ):
            bWriteTitle = True
        if (bWriteTitle and numTitle > 0):
            if ( -1 == strFSign.find(word) ):
                if (False == bool(re.search(r'\d', word))):
                    strTitle = strTitle + word
                    numTitle -= 1

        if ( i == iRandAbstract ):
            strAbstract += word
            strAb = ''
            iAbSing = random.randint(5, 20)
            iAbNum = 0
            while(numAbstract > 0):
                strAb = stringArr[random.randint(0, len(stringArr)-1)]
                strAbstract += strAb
                numAbstract -= 1
                iAbNum += 1
                if (iAbSing == iAbNum):
                    strAbstract += listSing[random.randint(0, len(listSing)-1)]
                    iAbSing = random.randint(5, 20)
                    iAbNum = 0

    # strTitle = strTitle.translate(None, punctuation)

    listResult.append(strTitle)
    listResult.append(strKeyW)
    listResult.append(strAbstract)
    listResult.append(strRR)
    return listResult

# I'm gonna make a method so I can do it a bunch of times really easily.
# 一篇字数1520, 代码中以词为单位
def makeText(OutputF = 'the'):

    # global model

    dumpPaper = open(OutputF, 'wb')
    listTotalR = []
    for iPaper in range(5001):
        numContent = random.randint(6600, 20800)
        indexW = 0
        while (True):
            indexW = random.randint(0, len(stringArr)-1)
            if (False == bool(re.search(r'\d', stringArr[indexW]))):
                break
        listR = generate(stringArr[indexW], numContent)
        paperDict = {'title':listR[0], 'Keyword':listR[1], 'Abstract':listR[2], 'Content':listR[3]}
        listTotalR.append(paperDict)

        if (iPaper % 1000 == 0):
            print(OutputF + '-' + str(iPaper) + '-' +'Paper Title:' + listR[0] + '---' + str(time.strftime('%H:%M:%S',time.localtime(time.time()))))

    pickle.dump(listTotalR, dumpPaper, protocol=2)
    listTotalR = []


inputWFPath = '201511030.mallet.summary'
iGFNum = 3

try:  
  opts, args = getopt.getopt(sys.argv[1:], "", ["inputWordsFile=", "GenFileN="])  
except getopt.GetoptError:  
   print ('OCRCheckErr Getopt Error!')
   sys.exit(1)

for name, value in opts:
    if name in ("--inputWordsFile"):
        inputWFPath = value
    elif name in ("--GenFileN"):
        iGFNum = int(value)

stringArr = []
iNN = 0
with open(inputWFPath, 'r') as f:
    for lineC in f:
        iNN += 1
        
        listC = lineC.split('\t')
        listC[1] = int(listC[1].replace('\n', ''))
        ipos = listC[0].find('{d}')
        if ( -1 != ipos ):
            strINum = listC[0].replace('{d}', str(random.randint(1, 100)))
            stringArr.append(strINum)
        else:
            stringArr.append(listC[0])
        
        if ( iNN % 5000 == 0 ):
            print(str(iNN) + ':Read Word line Number!! ' + str(time.strftime('%H:%M:%S',time.localtime(time.time()))))


# threads = []
# for i in range(iGFNum):
#     dumpPickleN = str(i+1) + '-dumpPickle.pkl'
#     t = threading.Thread(target=makeText, args=(dumpPickleN,))
#     threads.append(t)

# for tc in threads:
#     tc.setDaemon(True)
#     tc.start()

# for tk in threads:
#     tk.join()

for i in range(iGFNum):
    dumpPickleN = str(i+1) + '-dumpPickle.pkl'
    makeText(dumpPickleN)