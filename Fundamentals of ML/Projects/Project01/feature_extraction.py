# -*- coding: utf-8 -*-
"""
File:   feature_extraction.py
Author: ml-is-fun 
Date:   13 Dec 2018
Desc:   extracts n=100 features for each image using diagonal
        feature extraction method   
    
"""

import numpy as np
from PIL import Image

"""
Code Reference: https://stackoverflow.com/questions/5953373/how-to-split-image-into-multiple-pieces-in-python   

"""
def createZones(imageFile):
  picture = []
  image = imageFile 
  height = image.shape[0]
  width = image.shape[1]

  for x in range(0, height, 10):
      for n in range(0, width, 10):
          a = image[x:x+10, n:n+10]
          picture.append(a)
  return picture

def diagonalization(zone):
    num_of_diags = 19
    
    zone_height = zone.shape[0]
    zone_width = zone.shape[1]
    
    sum_of_pixels = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
    sum_along_diags = np.zeros((num_of_diags))

    for sum_diag in range(num_of_diags):
        for i in range(zone_height):
            for j in range(zone_width):
                if((i + j) == sum_of_pixels[sum_diag]):
                    sum_along_diags[sum_diag] += zone[i][j]
    feature_value = np.sum(sum_along_diags,axis=0)/num_of_diags;

    return feature_value

def featureExtraction(Drawing_list):
    list_of_zones = list()
    features = [[] for x in range(len(Drawing_list))]
    
    for j in range(len(Drawing_list)):
        list_of_zones.append(createZones(Drawing_list[j][:,:,0]))
        
        for i in range(len(list_of_zones[0])):
            features[j].append(diagonalization(list_of_zones[0][i]))
        list_of_zones = []
        
    features = np.asarray(features)
    
    return features