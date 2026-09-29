import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('dog.jpeg', 0)

height, width = img.shape
x= np.linspace(0, width, width, dtype = int)
y = np.linspace(0, height, height, dtype = int)

X, Y = np.meshgrid(x, y)

#print(X)
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
surf = ax.plot_surface(X, Y, img, cmap = 'plasma_r')

plt.show()
