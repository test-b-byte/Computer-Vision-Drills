#Sabastian Mandell
#Sep 24, 2026

import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plp


tooDark = cv2.imread("dark_image.jpg")

#find sizes
rowcount = tooDark.shape[0]
colcount = tooDark.shape[1]
constant = (rowcount * colcount)
#make container
histList = [0]*256
#print(histList)

#convert triplet to greyscale
greyD = ((tooDark[:,:,0]*.114)//1 + (tooDark[:,:,1]*.587)//1 + (tooDark[:,:,2]*.299)//1).astype(np.uint8)


#get vlaues for histogram
for x in range(rowcount):
    for y in range (colcount):
        histList[greyD[x][y]] += 1;
        
cdfD = [0]*256
cdfD[0] = histList[0]
print(len(histList))

#CDF build the new list
for x in range(1, len(histList)):
    cdfD[x] = cdfD[x-1] + histList[x]
    #print(cdfD[x]) #wuick lil test

#normalization minimum
cdf_min = 0
for i in range(len(cdfD)):
    if cdfD[i] > 0:
        cdf_min = cdfD[i]
        break


# mapping phase by realtive positon / total count and * 255
mapped = [0]*256
for x in range(len(mapped)):
    mapped[x] = round((cdfD[x] - cdf_min) / (constant - cdf_min) * 255)



#rebuild the equalized image
newIm = []
for x in range(rowcount):
    newIm.append([0]*colcount)

for x in range(rowcount):
    for y in range(colcount):
        newIm[x][y] = (mapped[greyD[x][y]])

#apparently it wont work if its not numpy array
newIm = np.array(newIm).astype(np.uint8)

#compare/ test
Compared = cv2.equalizeHist(greyD)

#these didn't look close to mean, i think it needs normalization so I'm going to look up and add that step.

cv2.imshow("test", newIm) #NOTE these appear on top of each other so you need to move the windows
cv2.imshow('compare', Compared)
cv2.waitKey(0)
cv2.destroyAllWindows()



# funcitonize it for practice with a second image
def theGreatEqualizer(img):
    rowCount = img.shape[0]
    colCount = img.shape[1]
    constant = rowCount*colCount
    
    
    histList = [0] * 256
    greyScale = ((img[:,:,0]*.114)//1 + (img[:,:,1]*.587//1) + (img[:,:,2]*.299//1)).astype(np.uint8)
               
    for x in range(rowCount):
        for y in range(colCount):
            histList[greyScale[x][y]] += 1

    cDisFun = [0]*256
    cDisFun[0] = histList[0]
    for i in range(1, len(histList)):
        cDisFun[i] = cDisFun[i-1] + histList[i]

    cDisMin = 0
    for i in range(len(cDisFun)):
        if cDisFun[i] > 0:
            cDisMin = cDisFun[i]
            break

    mapped = [0]*256
    for n in range(len(mapped)):
        mapped[n] = round((cDisFun[n] - cDisMin) / (constant - cDisMin) * 255)

    equalIm = []
    for x in range(rowCount):
        equalIm.append([0]*colCount)
        
    for x in range(rowCount):
        for y in range(colCount):
            equalIm[x][y] = (mapped[greyScale[x][y]])

    equalIm = np.array(equalIm).astype(np.uint8)

    cv2.imshow("final", equalIm)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    img = cv2.imread("too_bright.png")
    theGreatEqualizer(img)




    
    
    




    
