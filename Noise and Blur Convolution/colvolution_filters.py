

import cv2
import random
import numpy as np
import matplotlib.pyplot as ply

doggy = cv2.imread("dog.jpeg")

rowCount, colCount = doggy.shape[:2]
constant = colCount * rowCount


#0 is for copying, 1 10 50 for each noise level
grey0 = (doggy[:,:,0]//3 + doggy[:,:,1]//3 + doggy[:,:,2]//3)
grey1 = grey0.copy()
grey10 = grey0.copy()
grey50 = grey0.copy()


#1% as salt or pepper
for x in range(rowCount):
    for y in range(colCount):
        diceRoll = random.randint(1,200)
        if (diceRoll == 1): 
            grey1[x][y] = 0
        elif (diceRoll == 200): 
            grey1[x][y] = 255

#10% as salt or pepper
for x in range(rowCount):
    for y in range(colCount):
        diceRoll = random.randint(1,200)
        if (diceRoll <= 10): 
            grey10[x][y] = 0
        elif (diceRoll >= 190): 
            grey10[x][y] = 255

#50% as salt or pepper
for x in range(rowCount):
    for y in range(colCount):
        diceRoll = random.randint(1,200)
        if (diceRoll <= 50): 
            grey50[x][y] = 0
        elif (diceRoll >= 151): 
            grey50[x][y] = 255


#padding arrays
#five for later
#combine the padding an fill builds in to 1- functions
#copy greyDog/ img imnto larger array, +1 offst for padding
#functionize this

def padMe3 (array):
    padded = []
    for x in range(rowCount + 2):
        padded.append([0] * (colCount +2))

    for x in range(rowCount):
        for y in range(colCount):
            padded[x+1][y+1] = array[x][y]
    return padded


def padMe5(array):
    fiveX = []
    for x in range(rowCount + 4):
        fiveX.append([0] * ( colCount +4))
    for x in range(rowCount):
            for y in range(colCount):
                fiveX[x+2][y+2] = array[x][y]
    return fiveX

#intermittend organize step, get all the duckies in a row for testing
padded1_3 = padMe3(grey1)
padded10_3 = padMe3(grey10)
padded50_3 = padMe3(grey50)
padded1_5 = padMe5(grey1)
padded10_5 = padMe5(grey10)
padded50_5 = padMe5(grey50)

#ok convulotion window math
def windowTech3 (array, x, y):
    total = 0
    for xWindow in range(-1, 2):
        for yWindow in range(-1, 2):
            total += int(array[x+xWindow][y+yWindow])
    return total //9

#smae but bigger now
def windowTech5(array, x, y):
    total = 0
    for xWindow in range(-2,3):
        for yWindow in range(-2,3):
            total += int(array[x+xWindow][y+yWindow])
    return total // 25

#praxticing list completinng format
#[list of [0] in y columns] for x amount of rows. orginal image is fine
rinsed1_3 = grey0.copy()
rinsed10_3 = grey0.copy()
rinsed50_3 = grey0.copy()
rinsed1_5 = grey0.copy()
rinsed10_5 = grey0.copy()
rinsed50_5 = grey0.copy()


#3x3 , use function call, aadjust parameters for the padding
for x in range(rowCount):
    for y in range(colCount):
        rinsed1_3[x][y] = windowTech3(padded1_3, x+1, y+1)
        rinsed10_3[x][y] = windowTech3(padded10_3, x +1, y+1)
        rinsed50_3[x][y] = windowTech3(padded50_3, x +1, y+1)

for x in range(rowCount):
    for y in range(colCount):
        rinsed1_5[x][y] = windowTech5(padded1_5, x+1, y+1)
        rinsed10_5[x][y] = windowTech5(padded10_5, x+1, y+1)
        rinsed50_5[x][y] = windowTech5(padded50_5, x+1, y+1)

#loop a dictionary since theres a plot with titles etc
final9={"1% Noise": grey1, "10% Noise": grey10, "50% Noise": grey50, "3x3 Filter 1%": rinsed1_3,
        "3x3 Filter on 10% Noise": rinsed10_3, "3x3 Filter on 50% Noise": rinsed50_3, 
        "5x5 Filter on 1%": rinsed1_5,  "5x5 Filter on 10%": rinsed10_5, "5x5 Filter on 50%": rinsed50_5}

i = 0
for title, img in final9.items():
    ply.subplots(3, 3, i+1
    ply.imshow(img, cmap='gray')
    ply.title(title)
    i +=1

ply.show)

'''
references
https://www.youtube.com/watch?v=5zznDnZ4IJI
Simple Convolution and Image Filters, Part 1 -- Latent Topics in Data Science


https://www.youtube.com/watch?v=6SNBUWTX3MA
Python#16 How to Manually Add a Salt-and-pepper Noise to an Image in Python

https://www.youtube.com/watch?v=C_zFhWdM4ic&t=33s
How Blurs & Filters Work - Computerphile

https://www.youtube.com/watch?v=D4VlmL3G4_o
Learn Data Visualization with Matplotlib in Python: A Beginner’s Guid
'''
