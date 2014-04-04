import argparse
import sys
from PIL import Image
import pygame
import random
from collections import defaultdict

parser = argparse.ArgumentParser(description='Turns images into ASCII text.')
parser.add_argument('infile', help = 'Input image')
parser.add_argument('outfile', nargs = '?', default = sys.stdout, type = argparse.FileType('w'), help = 'Text file for output. Default: console')
parser.add_argument('-image', nargs = '?', help = 'Image filename for image output', metavar = 'FILENAME')
parser.add_argument('-font', default = 12, type = int, help = 'Font size used. Default: %(default)s', metavar = 'FONTSIZE')
parser.add_argument('-size', nargs = 2, type = int, help ='Width and height of output, in pixels', metavar = ('WIDTH', 'HEIGHT'))
parser.add_argument('-c', action = 'store_true', help = 'Colorizes output image')
args = parser.parse_args()

pygame.init()

infile = Image.open(args.infile)

# Load font and get size of 1 character
font = pygame.font.SysFont('monospace', args.font)
chwidth, chheight = font.size(' ')

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
oldwidth, oldheight = infile.size
if(args.size):
    im = infile.resize((args.size[0]/chwidth, args.size[1]/chheight), Image.ANTIALIAS)
else:
    im = infile.resize((oldwidth/chwidth, oldheight/chheight), Image.ANTIALIAS)

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

if(args.outfile):
# create and fill image with text
    outsurface = pygame.Surface((im.size[0]*chwidth,im.size[1]*chheight))
    outsurface.fill((255,255,255))

    for i, line in enumerate(outstrings):
        for j, char in enumerate(line):
            if(args.c):
                text = font.render(char,0,im.getpixel((j,i)))
            else:
                text = font.render(char,0,(0,0,0))
            outsurface.blit(text,(chwidth*j,chheight*i))

    pygame.image.save(outsurface,args.image)

#save text
for line in outstrings:
    args.outfile.write("%s\n" % line)
args.outfile.close()