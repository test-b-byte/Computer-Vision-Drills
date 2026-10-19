#Sabastian Mandell
#Oct 12 2026
#CS 5330 HW-2
# edge detection

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('dog.jpeg', 0)
#plt.plot(img)
#plt.imshow(img, cmap=plt.cm.gray)
#plt.show()
height, weight = img.shape
x = np.linspace(0, weight,weight, dtype=int)
y = np.linspace(0, height,height, dtype=int)
X, Y = np.meshgrid(x, y)
#https://docs.opencv.org/4.13.0/d4/d13/tutorial_py_filtering.html
'''
plt figure is the primary display
add/subplot creates sectionals wihtin the primary window
n-n-n, is arrangement, x,y, and sequecne
plot sruface is the detail of each sectional
'''


img5 = cv2.GaussianBlur(img,(5,5),0)
img11 = cv2.GaussianBlur(img,(11,11),0)
fig = plt.figure()
axNorm = fig.add_subplot(131, projection = '3d')
ax5 = fig.add_subplot(132, projection = '3d')
ax11 = fig.add_subplot(133, projection = '3d')

dog= axNorm.plot_surface(X,Y,img,cmap = plt.cm.gray)
dog2= ax5.plot_surface(X,Y,img5,cmap = plt.cm.gray)
dog3= ax11.plot_surface(X,Y,img11,cmap = plt.cm.gray)
plt.show()

#I honestly cant see a significant difference.

