#Sabastian Mandell
# CS5330 Oct 10
# Lab3

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import math
#/opt/miniconda3/envs/CS5330/bin/python
# https://www.youtube.com/watch?v=GHO7289OiGY
# OpenCV Python Image Resize, Kevin Wood, Robotic and AI
# And resizing by hand in case we're not allowd to use cv2 functions.
puppy = cv2.imread("rune_little.jpeg")
doggy = cv2.imread("rune_grown.jpeg")

'''
print(puppy.shape) #1400, 855, 3
print()
print(doggy.shape) #778, 856, 3
'''

#because I found the FFT which requires power of 2 sizing, os the FTT requires 512, 1024 etc
adjHeight = 1000
adjWeight = 880 

#resize by hand since idk of we're supposed to use cv2 tools
newPup = []
newDog = []
for i in range(adjHeight):
    newPup.append([0]*adjWeight)
    newDog.append([0]*adjWeight)

heigtScaleP = 1400 / adjHeight
weightScaleP = 855 /adjWeight
heigtScaleD = doggy.shape[0] / adjHeight
weightScaleD = doggy.shape[1] / adjWeight

for x in range(adjHeight):
    for y in range(adjWeight):
        puppyX = int(x* heigtScaleP)
        doggyX = int(x * heigtScaleD)
        puppyY = int(y * weightScaleP)
        doggyY = int(y* weightScaleD)
        newPup[x][y] = puppy[puppyX][puppyY]
        newDog[x][y] = doggy[doggyX][doggyY]

newDog = np.array(newDog).astype(np.uint8)
newPup = np.array(newPup).astype(np.uint8)

#greyscale / brightness
greyPup = (newPup[:,:,0]//3 + newPup[:,:,1]//3 + newPup[:,:,2]//3)
greyDog = (newDog[:,:,0]//3 + newDog[:,:,1]//3 + newDog[:,:,2]//3)

'''
cv2.imshow("grown", newDog)
cv2.imshow("baby", newPup)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

'''
#Foureier Transform
##https://www.youtube.com/watch?v=arYKpiVACvY, Plotting the Fourier Transform in Python (DFT/FFT) Signals with Paul
https://www.youtube.com/watch?v=o5EawXpa9AQ, Fourier Transform in Image Processing: Simple Guide for Beginners
https://stackoverflow.com/questions/38476359/fft-on-image-with-python

Apparently FTT is a merge sort adjacent related alogrythm, so I decied to use a tutor-mode LLM to work 
through it with me, I know its not for a grade but I wanted to understand it a bit and see its componenets
NO I did not write this or even fully undertand the trig myself
'''
'''
def fft1D(image):
    #wave frequency identificaiton!!! Merge sort typ recusive log function.
    N = len(image)
    if N == 1:
        return image
    evens = fft1D(image[0::2])
    odds = fft1D(image[1::2])

    combined = [0] * N
    for freq in range(N//2):
        angle = -2 * math.pi * freq / N
        twiddle = complex(math.cos(angle), math.sin(angle)) * odds[freq]

        combined[freq] = evens[freq] + twiddle
        combined[freq + N//2] = evens[freq] - twiddle
    return combined

def fft2D(image):
    #transform row by row
    FTRows = []
    for row in image:
        FTRows.append(fft1D(row))

    #transform coloumn, use transpose zip function because it needs to group col as rows to process and then revert them back
    transmigration = list(zip(*FTRows))
    FTCols = []
    for col in transmigration:
        FTCols.append(fft1D(list(col)))
    #convert cols back to cols, (they get orocessed as a row)
    done = list(zip(*FTCols))
    return done

#The filter part, so how these things work is by identifying which waves are waves in teh Fourier Transform are
#in the that high-freq range, which our eyes tend to ignore, so we can cut those out by basically removing them 
# and keeping only the parts that the eye would register. this means lighter load while retaining good viusal appeal

def ftt_lowMask(N, cutoff):
    mask = []
    for x in range(N):
        row = []
        for y in range (N):
            distance_from_Center = math.sqrt((x - N/2)**2 + (y -N/2)**2)
            if distance_from_Center < cutoff:
                row.append(1)
            else:
                row.append(0)
        mask.append(row)
    return mask

def fft_highMask(N, cutoff):
    mask = []
    for x in range(N):
        row =[]
        for y in range(N):
            DFC = math.sqrt((x- N/2)**2 + (y- N/2)**2)
            if DFC >= cutoff:
                row.append(1)
            else:
                row.append(0)
        mask.append(row)
    return mask  
'''

    
#padding and blurring, back to normal assignment
def pad11(img_array):
    padded = []
    for x in range(adjHeight +10):
        padded.append([0] * (adjWeight+10))

    for x in range(adjHeight):
        for y in range(adjWeight):
            padded[x+5][y+5] = img_array[x][y]
    return padded

#11x11 filter, same as last lab, function smooths pixel, 
def window11(array, x, y):
    total = 0
    for xWindow in range(-5, 6):
        for yWindow in range(-5,6):
            total += int(array[x+xWindow][y+yWindow])
    return total // 121

#prepare to popuuulate ze lowpass Images
paddedPup = pad11(greyPup)
paddedDog = pad11(greyDog)

LowDog = greyDog.copy()
LowPup = greyPup.copy()
HighDog = greyDog.copy()
HighPup = greyPup.copy()

#similarly to last lab, use the 11x11 smoother to popiulate a new array
for x in range(adjHeight):
    for y in range(adjWeight):
        LowDog[x][y] = window11(paddedDog, x+5, y+5)
        LowPup[x][y] = window11(paddedPup, x+5, y+5) 


for x in range(adjHeight):
    for y in range(adjWeight):
        clamp = (int(HighPup[x][y]) - int(LowPup[x][y]) + 127)//2
        #if (clamp > 255):
        #   clamp = 255
        if clamp < 0:
            clamp = 0
        HighPup[x][y] = clamp

for x in range(adjHeight):
    for y in range(adjWeight):
        clamp = (int(HighDog[x][y]) - int(LowDog[x][y]) + 127)//2
        #if (clamp > 255):
         #   clamp = 255
        if clamp < 0:
            clamp = 0
        HighDog[x][y] = clamp

'''
sanity check, test to see if we made it this far.
cv2.imshow("High", HighDog)
cv2.imshow("Lolo", LowPup)
cv2.waitKey(0)
cv2.destroyAllWindows
Yaaay we did it.

https://www.youtube.com/watch?v=5jONfLRz4uk
OPENCV Python Image Blending, Kevin Wood, Robotics and AI
https://www.youtube.com/watch?v=8UTJFgSBra0
Combine two images into a single image with OpenCV
these all use cv2
'''


combinedPooches = LowPup.copy()
for x in range(adjHeight):
    for y in range(adjWeight):
        clamp = (int(HighPup[x][y]) + int(LowDog[x][y]))//2
        #if (clamp > 255):
        #    clamp = 255
        if clamp < 0:
            clamp = 0
        combinedPooches[x][y] = clamp

combinedPooches2 = LowDog.copy()
for x in range(adjHeight):
    for y in range(adjWeight):
        clamp = (int(HighDog[x][y]) + int(LowPup[x][y]))//2
        #if (clamp > 255):
        #    clamp = 255
        if clamp < 0:
           clamp = 0
        combinedPooches2[x][y] = clamp


cv2.imshow("baby to big", combinedPooches)
cv2.imshow("big to baby", combinedPooches2)
cv2.waitKey(0)
cv2.destroyAllWindows

#https://matplotlib.org/stable/tutorials/images.html tutorials

plt.subplot(1,3, 1)
plt.imshow(LowDog, cmap='gray')

plt.subplot(1, 3, 2)
plt.imshow(HighPup, cmap='gray')

plt.subplot(1, 3, 3)
plt.imshow(combinedPooches, cmap='gray')
plt.tight_layout()
plt.show()

