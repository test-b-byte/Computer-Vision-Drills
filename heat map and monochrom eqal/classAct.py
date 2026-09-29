#Ryan Bockmon
#5/13/2024
import cv2
import numpy as np
import matplotlib.pyplot as plt




#mono chroming
#histogram equalization

img = cv2.imread('flowers.jpg')#Opens the image in color
cv2.imshow("test", img) #NOTE these appear on top of each other so you need to move the windows
cv2.waitKey(0)
cv2.destroyAllWindows()

rowCount = img.shape[0]
colCount = img.shape[1]
constant = rowCount * colCount

histRed = [0] * 256
histBlue = [0] * 256
histGreen = [0] * 256
redScale = img.copy()
blueScale = img.copy()
greenScale = img.copy()

for x in range(rowCount):
    for y in range(colCount):
        redScale[x][y][0] = 0
        redScale[x][y][1] = 0
        blueScale[x][y][2] = 0
        blueScale[x][y][1] = 0
        greenScale[x][y][2] = 0
        greenScale[x][y][0] = 0
        

#red     
for x in range(rowCount):
    for y in range(colCount):
        histRed[redScale[x][y][2]] += 1

CDF = [0] * 256
CDF[0] = histRed[0]
for i in range(1, len(histRed)):
             CDF[i] = CDF[i-1] + histRed[i]

CDFMIN = 0
for i in range(len(CDF)):
    if CDF[i] > 0:
        CDFMin = CDF[i]
        break

mapped = [0]*256
for n in range(len(mapped)):
    mapped[n] = ((CDF[n] - CDFMin) / (constant - CDFMin)) * 255

redEqual = redScale.copy()
for x in range(rowCount):
    for y in range(colCount):
        redEqual[x][y][2] = mapped[int(redScale[x][y][2])]


#blue
for x in range(rowCount):
    for y in range(colCount):
        histBlue[blueScale[x][y][0]] += 1

CDFb = [0] * 256
CDFb[0] = histBlue[0]
for i in range(1, len(histBlue)):
             CDFb[i] = CDFb[i-1] + histBlue[i]

CDFMINb = 0
for i in range(len(CDFb)):
    if CDFb[i] > 0:
        CDFMinb = CDFb[i]
        break

mappedb = [0]*256
for n in range(len(mapped)):
    mappedb[n] = ((CDFb[n] - CDFMinb) / (constant - CDFMinb)) * 255

blueEqual = blueScale.copy()
for x in range(rowCount):
    for y in range(colCount):
        blueEqual[x][y][0] = mappedb[int(blueScale[x][y][0])]

# green

for x in range(rowCount):
    for y in range(colCount):
        histGreen[greenScale[x][y][1]] += 1

CDFg = [0] * 256
CDFg[0] = histGreen[0]
for i in range(1, len(histGreen)):
             CDFg[i] = CDFg[i-1] + histGreen[i]

CDFMINg = 0
for i in range(len(CDFg)):
    if CDFg[i] > 0:
        CDFMing = CDFg[i]
        break

mappedg = [0]*256
for n in range(len(mappedg)):
    mappedg[n] = ((CDFg[n] - CDFMing) / (constant - CDFMing)) * 255

greenEqual = greenScale.copy()
for x in range(rowCount):
    for y in range(colCount):
        greenEqual[x][y][1] = mappedg[int(greenScale[x][y][1])]

cv2.imshow('red', redScale)
cv2.imshow('blue', blueScale)
cv2.imshow('green', greenScale)
cv2.imshow('red 2', redEqual)
cv2.imshow('blue 2', blueEqual)
cv2.imshow('green 2', greenEqual)
cv2.waitKey(0)
cv2.destroyAllWindows()
            
             


'''
#plt.hist(img4.ravel(),256,[0,256],histtype=u'step')
#plt.show()
equ = cv2.equalizeHist(img4)
cv2.imshow('image1',img4)
cv2.imshow('image2',equ)
plt.hist(img4.ravel(),256,[0,256],histtype=u'step')
plt.hist(equ.ravel(),256,[0,256],histtype=u'step')
plt.show()
'''
