# -*- coding: utf-8 -*-
"""
File:   findcontours.py
Author: ml-is-fun 
Date:   13 Dec 2018
Desc:   Finds and draws contours for each image   
    
"""

"""
Code Reference: Python version of this tutorial - http://opencv.itseez.com/doc/tutorials/imgproc/shapedescriptors/find_contours/find_contours.html#find-contours
Level : Beginner
Benefits : Learn to use 1) cv2.findContours() and 2)cv2.drawContours()
Written by : Abid K. (abidrahman2@gmail.com) , Visit opencvpython.blogspot.com for more tutorials
Group ml-is-fun changed the function arguments to match with our problem needs.
"""

import cv2
import numpy as np

def thresh_callback(thresh,blur,img):
    edges = cv2.Canny(blur,thresh,thresh*2)
    drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
    image,contours,hierarchy = cv2.findContours(edges.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        color = np.random.randint(0,255,(3)).tolist()  # Select a random color
        cv2.drawContours(drawing,[cnt],0,color,2)
        cv2.imshow('output',drawing)
    cv2.imshow('input',img)
    return drawing


thresh = 200
max_thresh = 255

def createContours(data_size, image_path):
    Drawing_list =[]

    for i in range(data_size):
        img = cv2.imread(image_path + '/filename_' + str(i) + '.bmp')
        #cv2.imshow('image',img)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        #cv2.createTrackbar('canny thresh:','input',thresh,max_thresh,thresh_callback)
        drawing = thresh_callback(200,blur,img)
        Drawing_list.append(drawing)
    
    return Drawing_list