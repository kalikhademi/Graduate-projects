#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:   normalization.py
Author: ml-is-fun 
Date:   13 Dec 2018
Desc:   Resizes image to 100x100 pixels and saves images as bmp image  
    
"""

"""
Code Reference: https://docs.opencv.org/3.4/da/d6e/tutorial_py_geometric_transformations.html
                make bmp normalized image 
                https://stackoverflow.com/questions/17358722/python-3-how-to-delete-images-in-a-folder

"""
import cv2 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image 
import os


trainNormal = []
def NormalizeImage(trainData):
    	for x in range(len(trainData)):    
    		img = trainData[x]
    		rows = img.shape[0]
    		cols = img.shape[1]
    		res = cv2.resize(img,(100, 100), interpolation = cv2.INTER_CUBIC)
    		trainNormal.append(res)
    		plt.imsave('Training_Images/filename_' + str(x) + '.png', trainNormal[x], cmap=cm.gray)
    		image = Image.open('Training_Images/filename_' + str(x) + '.png')
    		image.save('Training_Images/filename_' + str(x) + '.bmp')   		
    		os.remove('Training_Images/filename_' + str(x) + '.png')

     
     
  
