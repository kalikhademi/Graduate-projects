#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 19:22:59 2018

@author: kianamac
"""

import numpy as np
import matplotlib.pyplot as plt

dataList =[]

labels = [1,2,3,4,5,6,7,8]
final_labels=[]

for item in labels:
    for i in range(10):
        final_labels.append(item)

print(final_labels)
#repeat =[]
#for item in labels:
#    x= labels.count(item)
#    repeat.append(x)
    
#print(len(labels))

for i in range(1,81):
    x = np.load('results/'+str(i) +'_results.npy')
    dataList.append(x)

np.save('data.npy',dataList)   
np.save('labels.npy',final_labels)