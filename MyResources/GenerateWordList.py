#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: qy
# @Date:   2015-12-07 09:05:10
# @Last Modified by:   qy
# @Last Modified time: 2015-12-09 09:48:04
import time


fileName = 'xinhua06-09_splited.txt'

fileWLName = 'xinhua06-09_WordList.txt'
fileWL = open(fileWLName, 'w+')

id = 0
iN = 0
setTotalData = set([])
lTemp = []
with open(fileName, 'r') as f:
    for line in f:
        iN += 1
        ll = line.split()
        lTemp.extend(ll)
        if ( iN % 2000 == 0 ):
            print('Read File line:' + str(iN) + ' ' + str(time.strftime('%H:%M:%S',time.localtime(time.time()))))
            sData = set(lTemp)
            setTotalData = setTotalData | sData
            lTemp = []
            sData = set([])
            print(len(lTemp))
            print(len(setTotalData))

if (len(lTemp) > 0):
    sData = set(lTemp)
    setTotalData = setTotalData | sData
    lTemp = []
    sData = set([])
    print(len(lTemp))
    print('Total Words : ' + str(len(setTotalData)))

lDate = list(setTotalData)
setTotalData = set([])
for item in lDate:
    WriteStrC = item + '\n'
    fileWL.write(WriteStrC)
    id += 1
    if (id % 50000 == 0):
        print(id)
print('End Time: ' + str(time.strftime('%H:%M:%S',time.localtime(time.time()))))
lDate = []

# strC = fileC.readline(10240)
# ll = strC.split()

# sData = set(ll)

# lDate = list(sData)


# fileC.close()
fileWL.close()