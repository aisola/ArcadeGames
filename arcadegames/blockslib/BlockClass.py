#--------------------------------------------------------------------------------
# @file   : BlockClass.py
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

class Block(pygame.sprite.Sprite):
    "The breakout Block Class"
    
    def __init__(self,color,x,y):
        """
            @param color: block color
            @param x: block horizontal position
            @param y: block vertical position
        """
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        # Size of break-out blocks
        self.width=23
        self.height=15
        
        # Create the image of the block of appropriate size & Fill it
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(color)
        
        if color == red:
            self.color = "red"
        elif color == blue:
            self.color = "blue"
        elif color == yellow:
            self.color = "yellow"
        
        # Fetch the rectangle object that has the dimensions of the image & set position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y