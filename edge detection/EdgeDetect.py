#Sabastian Mandell
#Oct 13 2026
#CS 5330
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math

'''
https://www.youtube.com/watch?v=uihBwtPIBxM
Finding the Edges (Sobel Operator) - Computerphile

https://www.youtube.com/watch?v=9YpP1uGJcmM
Python#13 Edge Detection using Sobel Operator in Python
Made Python

https://www.youtube.com/watch?v=Ie2Tj_3Ug2A
Sobel Edge Detector | Code-Implementation-Python | Feature point
'''
#build sobel filter kernels
Gofx = np.array([[1,0,-1],
                [2,0,-2],
                [1,0,-1]])

Gofy = np.array([[1,2,1],
                [0,0,0],
                [-1,-2,-1]])

#pull img, make grey
img = cv2.imread('dog.jpeg')
greyD = (img[:,:,0]//3 + img[:,:,1]//3 + img[:,:,1]//3)

#here for me to call whenever Im workin to see if its coming along
def test(img):
    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows

#test(greyD) check
#create a padded version, sobel is 3x3
#greyscale or 2D
def padded(image):
    new = []
    for x in range(image.shape[0] + 2):
        new.append([0] *( image.shape[1]+2))

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            new[x+1][y+1] = image[x][y]
    return new



#convolllvee, because we're trying the serperate kernal technqieu this time
#we can pass it as a parameter
def convolve(padded, s_kern, x, y): #padded image, G of x or y sobel, and (x,y)
    newval = 0
    for j in range(-1,2):
        for k in range(-1,2):
            newval += int(padded[x+j][y+k] * s_kern[j+1][k+1])
    return newval

#prepare to populate the new image
dog_padded = padded(greyD)
Hi = greyD.shape[0]
We = greyD.shape[1]
edged = greyD.copy()

#populate new array withnalues. errors out wiht overflow. needs a clamp
for x in range(Hi):
    for y in range(We):
        gx = convolve(dog_padded, Gofx, x+1, y+1)
        gy = convolve(dog_padded, Gofy, x+1, y+1)
        big_G = math.sqrt(gx**2 + gy**2)
        clamp_fix = int(min(255, big_G))
        edged[x][y] = clamp_fix

#test(edged) #success

cutoff50 = edged.copy()
cutoff150 = edged.copy()

#cutoffs to spec and cleans noise
for x in range(Hi):
    for y in range(We):
        if cutoff50[x][y] > 50:
            cutoff50[x][y] = 255
        else:
            cutoff50[x][y] = 0

for x in range(Hi):
    for y in range(We):
        if cutoff150[x][y] > 150:
            cutoff150[x][y] = 255
        else:
            cutoff150[x][y] = 0

uncanny = cv2.Canny(greyD,100, 100)
'''tests, successful
test(cutoff50)
test(cutoff150)
test(uncanny)
'''

#guassian runs.

gausianGrey = cv2.GaussianBlur(greyD, (5,5), 0)
gassianPad = padded(gausianGrey)
gausianEdge = gausianGrey.copy()
cannyGause = cv2.Canny(gausianGrey, 100, 100)

for x in range(Hi):
    for y in range(We):
        gx = convolve(gassianPad, Gofx, x+1, y+1)
        gy = convolve(gassianPad, Gofy, x+1, y+1)
        big_G = math.sqrt(gx**2 + gy**2)
        clamp_fix = int(min(255, big_G))
        gausianEdge[x][y] = clamp_fix

gausian50 = gausianEdge.copy()
gausian150 = gausian50.copy()

for x in range(Hi):
    for y in range(We):
        if gausian50[x][y] > 50:
            gausian50[x][y] = 255
        else:
            gausian50[x][y] = 0

for x in range(Hi):
    for y in range(We):
        if gausian150[x][y] > 150:
            gausian150[x][y] = 255
        else:
            gausian150[x][y] = 0
'''
test(gausianGrey)
test(gausian50)
test(gausian150)
test(cannyGause)
'''
#greyD, 
fig = plt.figure()
greyDog= fig.add_subplot(141)
greyDog.imshow(greyD,cmap = plt.cm.gray)
greyDog.set_title("GreyScale")


Cut_off_50 = fig.add_subplot(142)
Cut_off_50.imshow(cutoff50,cmap = plt.cm.gray)
Cut_off_50.set_title("50 cut off")

Cut_off_150 = fig.add_subplot(143)
Cut_off_150.imshow(cutoff150,cmap = plt.cm.gray)
Cut_off_150.set_title("150 cut off")


Canny = fig.add_subplot(144)
Canny.imshow(uncanny,cmap = plt.cm.gray)
Canny.set_title("Canny")


BlurredGrey = fig.add_subplot(241)
BlurredGrey.imshow(gausianGrey,cmap = plt.cm.gray)
BlurredGrey.set_title("Blurred Original")


Blurred_c50 = fig.add_subplot(242)
Blurred_c50.imshow(gausian50,cmap = plt.cm.gray)
Blurred_c50.set_title("Blurred 50cut")


Blurred_C150 = fig.add_subplot(243)
Blurred_C150.imshow(gausian150,cmap = plt.cm.gray)
Blurred_C150.set_title("Blurred 150cut")


Blurred_Canny = fig.add_subplot(244)
Blurred_Canny.imshow(cannyGause,cmap = plt.cm.gray)
Blurred_Canny.set_title("Blurred Canny")


plt.tight_layout()
plt.show()