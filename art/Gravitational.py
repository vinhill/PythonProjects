#F = ((m1*m2) / d^2) * gravitational_strength
#distance is the distance between the center of both elements
#distance and force are vectors!
#maybe give the objects some trail
    #have them draw to the background, make the background greyer each tick
#maybe let all objects attract each other

import pygame
import numpy as np
from itertools import chain
import math
import random

GRAV_CONST = 10**-3
WIDTH = 1000
HEIGHT = 600

def attraction(b1, b2):
    dir = b2[0] - b1[0]
    d = math.sqrt( dir[0]**2 + dir[1]**2 )
    if(d < 10**-2):
        return [0,0]
    dir /= d
    return dir * GRAV_CONST * ((b1[2]*b2[2]) / d)

#init graphics
pygame.init()
img = pygame.display.set_mode((WIDTH,HEIGHT))
img.fill((255,255,255))
running = True;
pygame.display.flip()#actualizes display image (makes changes visible)

#init bodies
#a body is a tuple (pos,velocity,mass) all given as float
bodies = list()
for i in range(1, 20):
    bodies.append( [np.array([random.random()*WIDTH,random.random()*HEIGHT]), np.array([0.0,0.0]), random.random()*8+1] )
#bodies that will stay fixed in place
stationary = list()
#stationary.append( [np.array([float(WIDTH/3),float(HEIGHT/2)]), np.array([0.0,0.0]), 80] )

while(running):#without infinite loop, pygame will stop
    #check for closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #simulation step
    #calculate change in velocity
    for b in bodies:
        for to in chain(bodies, stationary):
            b[1] += attraction(b,to)
    #move bodies
    for b in bodies:
        b[0] += b[1]
    
    #actualize graphics
    pygame.draw.rect(img, (255,255,255,10), (0,0,WIDTH,HEIGHT), 0)
    for b in bodies:
        pygame.draw.circle(img, (255,0,0), (int(round(b[0][0])),int(round(b[0][1]))), int(math.log(b[2]))*5, 0)
    for b in stationary:
        pygame.draw.circle(img, (0,0,255), (int(round(b[0][0])),int(round(b[0][1]))), int(math.log(b[2]))*5, 0)
    pygame.display.flip()