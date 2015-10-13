# Name     : mcimage.py 
# Author   : Yasin Gamieldien (yasingamieldien.io)
# Date     : 11 October 2015
# Requires : Python 3.x or 2.7, numpy, PIL, mcpi, mcblocks.py, Minecraft
# Purpose  : Imports images into Minecraft, builds them pixelwise
# You are free to distribute and/or modify this code.

import numpy as np
import PIL.Image as Image
import mcpi.minecraft as minecraft
from mcblocks import blocks #mcblocks.py contains block index and colours

im = np.array(Image.open("image.jpg")) #insert target image filename

#image matrix reshaping for easier handling in loop
imshape = np.shape(im)
im2 = np.reshape(im, (imshape[0]*imshape[1], imshape[2])) 

# builds a matrix of block ids and states at correct indices
blockids = [blocks[np.argmin(((blocks[:,2] - x[0])*0.3)**2 +
                                ((blocks[:,3] - x[1])*0.59)**2 +
                                ((blocks[:,4] - x[2])*0.11)**2)][:2]
                                for x in im2]

#reversal of matrix - allows easy block placement from ground up
blockids = blockids[::-1]
blockids = np.array(blockids)

#configurable initial positions
ypos = 0
zpos = 0
xcorrect = (imshape[1])*ypos

mc = minecraft.Minecraft.create() #creates Minecraft session

for x in range(0, len(blockids)):

    if (x - xcorrect == imshape[1]): #correction of block sequence
        ypos += 1
        xcorrect = (imshape[1])*ypos

    blockID = int(blockids[x][0]) #not converting to int produces error
    blockState = int(blockids[x][1])
    mc.setBlock(x - xcorrect, ypos, zpos, blockID, blockState) #placement
