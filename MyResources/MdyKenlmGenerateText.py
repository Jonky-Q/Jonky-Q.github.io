#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: qy
# @Date:   2015-11-26 15:31:03
# @Last Modified by:   qy
# @Last Modified time: 2015-12-14 09:04:48

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import kenlm
import random
import pickle
import time
import threading
import re
import getopt


lock = threading.Lock()
strFSign = "[\s+\.\!\/_,$%^*()+\"\']+|[+——！，；“”。？:《》：、~@#￥%……&*（）]+ "
listSing = ['。', ':', '，', '！','？']


def generate(word = 'the', num = 50):
    global listTotalR

    numKeyWord = random.randint(10, 18)
    numTitle = random.randint(8, 18)
    numAbstract = random.randint(300, 460)
    
    ii = int(num / 300)
    numReturn = random.randint(5, ii)

    listResult = []
    strRR = ''
    strKeyW = word
    strAbstract = ''
    listK = []
    listReturn = []

    bWriteAbstract = False
    iRandAbstract = random.randint(1, 20)

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

    iRSConNum = 0
    iRandConSing = random.randint(5, 20)
    for i in range(num):
        
        strRR = strRR + word

        if (iRSConNum == iRandConSing):
            iRandConSing = random.randint(5, 20)
            iRSConNum = 0
            strSing = listSing[random.randint(0, len(listSing)-1)]
            strRR = strRR + strSing

        bConLoop = True
        iCountConNum = 0
        listNextCon = []
        while (bConLoop):
            iCountConNum += 1
            for kc in range(4):
                iNext = random.randint(0, len(listTotalR)-1)
                listNextCon.append(listTotalR[iNext])
            list.sort(listNextCon, key=lambda x:x[1], reverse=True)

            senCon =  word + ' ' + listNextCon[0][0]
            for ikenlm, (prob, length) in enumerate(model.full_scores_n(senCon)):
                if ( 1 == ikenlm ):
                    Tuple = length
                    ScoreOfGroupW = prob
                    if ( Tuple > 1 or ScoreOfGroupW > -5.0 ):
                        word = listNextCon[0][0]
                        iCountConNum = 0
                        bConLoop = False
                        iRSConNum += 1
            if (iCountConNum > 300):
                word = listNextCon[0][0]
                iCountNum = 0
                bConLoop = False
                print('Content kenlm not Found!')
            listNextCon = []
        
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
            listNext = []
            strPre = word
            bLoop = True
            iRandSing = random.randint(5, 20)
            iRSNum = 0
            while (numAbstract > 0):
                bLoop = True
                iCountNum = 0 
                while (bLoop):
                    iCountNum += 1
                    for k in range(3):
                        iNext = random.randint(0, len(listTotalR)-1)
                        listNext.append(listTotalR[iNext])
                    list.sort(listNext, key=lambda x:x[1], reverse=True)

                    sentence =  strPre + ' ' + listNext[0][0]
                    for i, (prob, length) in enumerate(model.full_scores_n(sentence)):
                        if ( 1 == i ):
                            Tuple = length
                            ScoreOfGroupW = prob
                            if ( Tuple > 1 or ScoreOfGroupW > -5.0 ):
                                strAbstract = strAbstract + strPre
                                strPre = listNext[0][0]
                                iCountNum = 0
                                numAbstract -= 1
                                bLoop = False
                                iRSNum += 1
                                if (iRSNum == iRandSing):
                                    iRandSing = random.randint(5, 20)
                                    iRSNum = 0
                                    strSing = listSing[random.randint(0, len(listSing)-1)]
                                    strAbstract = strAbstract + strSing
                    if (iCountNum > 300):
                        strAbstract = strAbstract + strPre
                        strPre = listNext[0][0]
                        iCountNum = 0
                        numAbstract -= 1
                        bLoop = False
                        print('Abstract kenlm not Found!')
                    listNext = []

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
    listTotalPaper = []

    strFW = ''
    for iPaper in range(100):
        numContent = random.randint(6600, 20800)
        iFWNum = 0
        listFW = []
        while (True):
            indexW = random.randint(0, len(listTotalR)-1)
            if (False == bool(re.search(r'\d', listTotalR[indexW][0]))):
                listFW.append(listTotalR[indexW])
                iFWNum += 1
            if ( iFWNum > 5 ):
                list.sort(listFW, key=lambda x:x[1], reverse=True)
                strFW = listFW[0][0]
                listFW = []
                break

        listR = generate(strFW, numContent)
        paperDict = {'title':listR[0], 'Keyword':listR[1], 'Abstract':listR[2], 'Content':listR[3]}
        listTotalPaper.append(paperDict)

        if (iPaper % 1000 == 0):
            print(OutputF + '-' + str(iPaper) + '-' +'Paper Title:' + listR[0] + '---' + str(time.strftime('%H:%M:%S',time.localtime(time.time()))))

    pickle.dump(listTotalPaper, dumpPaper, protocol=2)
    print('Over Time: ' + str(time.strftime('%H:%M:%S',time.localtime(time.time()))))



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
        iGFNum = value



iNN = 0
listTotalR = []
strC = ''
with open(inputWFPath, 'r') as f:
    for lineC in f:
        iNN += 1
        
        listC = lineC.split('\t')
        listC[1] = int(listC[1].replace('\n', ''))
        ipos = listC[0].find('{d}')
        if ( -1 != ipos ):
            strINum = listC[0].replace('{d}', str(random.randint(1, 100)))
            strC = strINum
        else:
            strC = listC[0]
        
        listTotalR.append(tuple([strC, int(listC[1])]))

        if ( iNN % 30000 == 0 ):
            print(str(iNN) + ':Read Word line Number!! ' + str(time.strftime('%H:%M:%S',time.localtime(time.time()))))

LM = '/home/qy/Documents/kenlm/result/4-xinhua-06-09.bin'
model = kenlm.LanguageModel(LM)
print(type(model))
print(str(time.strftime('%H:%M:%S',time.localtime(time.time()))))

###################################
threads = []
for i in range(iGFNum):
    dumpPickleN = str(i+1) + '-dumpPickle.pkl'
    t = threading.Thread(target=makeText, args=(dumpPickleN,))
    threads.append(t)

for tc in threads:
    tc.setDaemon(True)
    tc.start()

for tk in threads:
    tk.join()