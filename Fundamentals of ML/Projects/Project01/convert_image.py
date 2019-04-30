# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 21:27:56 2018

@author: Diandra
"""

import csv
from PIL import Image
import numpy as np
import string
import os
import pdb

csv_File_Path = 'handwritten_data/A_Z_Handwritten_Data.csv'#Your downloded csv file path

count = 1
last_digit_Name =  None

labels = []

image_Folder_Path = 'handwritten_data/png_images' #your path to target folder to save images. Note: Path should have 26 empty folder with name as alphabets

Alphabet_Mapping_List = list(string.ascii_uppercase)

for alphabet in Alphabet_Mapping_List:
    path = image_Folder_Path + '\\' + alphabet
    if not os.path.exists(path):
        os.makedirs(path)

with open(csv_File_Path, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    count = 0
    for row in reader:
        digit_Name = row.pop(0)
        image_array = np.asarray(row)
        image_array = image_array.reshape(28, 28)
        new_image = Image.fromarray(image_array.astype('uint8'))

        if last_digit_Name != str(Alphabet_Mapping_List[(int)(digit_Name)]):
            last_digit_Name = str(Alphabet_Mapping_List[(int)(digit_Name)])
            count = 0
            print ("")
            print ("Prcessing Alphabet - " + str (last_digit_Name))
        
        labels.append(last_digit_Name)
        image_Path = image_Folder_Path + '\\' + last_digit_Name + '\\' + str(last_digit_Name) + '-' + str(count) + '.png'
        new_image.save(image_Path)
        count = count + 1

        if count % 1000 == 0:
            print ("Images processed: " + str(count))

pdb.set_trace()
labels = [1 if x=='A' else x for x in labels]
labels = [2 if x=='B' else x for x in labels]
labels = [3 if x=='C' else x for x in labels]
labels = [4 if x=='D' else x for x in labels]
labels = [-1 if x=='E' else x for x in labels]
labels = [-1 if x=='F' else x for x in labels]
labels = [-1 if x=='G' else x for x in labels]
labels = [5 if x=='H' else x for x in labels]
labels = [6 if x=='I' else x for x in labels]
labels = [7 if x=='J' else x for x in labels]
labels = [8 if x=='K' else x for x in labels]
labels = [-1 if x=='L' else x for x in labels]
labels = [-1 if x=='M' else x for x in labels]
labels = [-1 if x=='N' else x for x in labels]
labels = [-1 if x=='O' else x for x in labels]
labels = [-1 if x=='P' else x for x in labels]
labels = [-1 if x=='Q' else x for x in labels]
labels = [-1 if x=='R' else x for x in labels]
labels = [-1 if x=='S' else x for x in labels]
labels = [-1 if x=='T' else x for x in labels]
labels = [-1 if x=='U' else x for x in labels]
labels = [-1 if x=='V' else x for x in labels]
labels = [-1 if x=='W' else x for x in labels]
labels = [-1 if x=='X' else x for x in labels]
labels = [-1 if x=='Y' else x for x in labels]
labels = [-1 if x=='Z' else x for x in labels]

labels = np.asarray(labels)
np.save('labels.npy',labels)