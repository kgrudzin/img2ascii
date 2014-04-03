import sys
from PIL import Image
import pygame
import random
from collections import defaultdict

pygame.init()

# Open files for input and output

fname = sys.argv[1]
    
image = Image.open(fname)

# Load font and get size of 1 character
font = pygame.font.SysFont('monospace', 12)
width, height = font.size(' ')

mapping = defaultdict(list)

# Find how many black pixels there are in each character
# Use ASCII values from 32 to 126
for i in xrange(32,127):
    text = font.render(chr(i),0,(255,255,255))
    covered = 0
    for x in xrange(text.get_width()):
        for y in xrange(text.get_height()):
            covered += text.get_at((x,y)).r
    covered /= 255
    mapping[covered].append(chr(i))

#downsize the image so each pixel is the size of a character
oldwidth, oldheight = image.size
im = image.resize((oldwidth/width, oldheight/height), Image.ANTIALIAS)

# Go through each pixel, and generate the text representation
# A random character is chosen from the group that has the same
# amount of black
outstrings = []
for i in xrange(im.size[1]):
    outstring = ''
    for j in xrange(im.size[0]):
        color = im.getpixel((j,i))
        gray = 0.2126*color[0]+0.7152*color[1]+0.0722*color[2]
        
        #scale the luminance values to the mapping
        coverage = int((255-gray)*max(mapping.keys())/(255))
        #not all coverage values are in the mapping, go down until we find one
        while not mapping.get(coverage):
            coverage -= 1
        char = random.choice(mapping[coverage])

        outstring+=(char)
    outstrings.append(outstring)


# create and fill image with text
outsurface = pygame.Surface((im.size[0]*width,im.size[1]*height))
outsurface.fill((255,255,255))

for i, line in enumerate(outstrings):
    for j, char in enumerate(line):
        text = font.render(char,0,im.getpixel((j,i)))
        outsurface.blit(text,(width*j,height*i))

pygame.image.save(outsurface,fname+'.png')

#save text
outfile = open(fname+'.txt','w')
for line in outstrings:
    outfile.write("%s\n" % line)
outfile.close()