import numpy as np
import cv2
from numpy import array
import matplotlib.pyplot as plt
#https://stackoverflow.com/questions/5953373/how-to-split-image-into-multiple-pieces-in-python   
def divideImage(imageFile):
  picture = []
  image = imageFile #Image.fromarray(np.uint8(imageFile*255))
  height = image.shape[0]
  #print('height', height)
  width = image.shape[1]
  #print('width', width)
  for x in range(0, height, 10):
      for n in range(0, width, 10):
          #box = (n, x, n + 10, x + 10)
          print('x', x)
          a = image[x:x+10, n:n+10] #.crop(box)
          picture.append(a)
  return picture
  
  #######THIS IS WHAT YOU RUN#############
cropped = []
file = np.load('file_drawing.npy')
plt.figure()
plt.imshow(file)
fig = plt.figure(figsize=(10,10))

cropped.append(divideImage(file[:,:,0]))
for i in range(len(cropped[0])):
    fig.add_subplot(10,10,i+1)
    plt.imshow(cropped[0][i])
#ccropped = array(cropped)
#print(cropped.shape)
