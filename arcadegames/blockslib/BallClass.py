#--------------------------------------------------------------------------------
# @file   : BallClass.py
# @package: See __init__.py
# @author : See __init__.py
# @license: See __init__.py
#--------------------------------------------------------------------------------

import sys, os, math, random
import pygame

from pygame.locals import *

# Define some global colors
global black, white, blue, red, yellow
red    = (255,   0,   0)
yellow = (255, 255,   0)
blue   = (  0,   0, 255)
white  = (255, 255, 255)
black  = (  0,   0,   0)

class Ball(pygame.sprite.Sprite):
    """A ball sprite. Subclasses the pygame sprite class."""
 
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images','pong_ball.gif'))
        self.rect = self.image.get_rect()
        
        self.xy = xy
        
        self.rect.centerx, self.rect.centery = self.xy
        self.maxspeed = 10
        self.servespeed = 5
        self.velx = 0
        self.vely = 0
        
        self.lives = 3
        self.canserve = True
 
    def reset(self):
        """Put the ball back in the middle and stop it from moving"""
        self.rect.centerx, self.rect.centery = self.xy
        self.velx = 0
        self.vely = 0
 
    def serve(self):
        if self.canserve == True:
            angle = random.randint(40, 140)
     
            # if close to zero, adjust again
            if abs(angle) < 5 or abs(angle-180) < 5:
                angle = random.randint(10,20)
     
            # do the trig to get the x and y components
            x = math.cos(math.radians(angle))
            y = math.sin(math.radians(angle))
     
            self.velx = self.servespeed * x
            self.vely = self.servespeed * y
    
    def setLives(self,lfs):
        self.lives = lfs
        if self.lives > 0:
            self.canserve = True
        else:
            self.canserve = False
    
    def addLife(self):
        self.lives += 1
        self.canserve = True
    
    def takeLife(self):
        self.lives -= 1
        if self.lives > 0:
            self.canserve = True
        else:
            self.canserve = False
    
    def hasLife(self):
        if self.lives > 0:
            return True