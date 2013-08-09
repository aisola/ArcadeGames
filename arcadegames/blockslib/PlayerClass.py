#--------------------------------------------------------------------------------
# @file   : PlayerClass.py
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

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.width = 82
        self.height = 8
        self.image = pygame.image.load(os.path.join('images','paddle_horizontal.gif'))
         
        # Make our top-left corner the passed-in location.
        surface = pygame.display.get_surface()
        self.screenheight = surface.get_height()
        self.screenwidth = surface.get_width()
        
        
        self.rect = self.image.get_rect()
        
        # set position
        self.rect.x = 359
        self.rect.y = self.screenheight - (self.height*2.5)
 
        # the movement speed of our paddle
        self.movementspeed = 15
 
        # the current velocity of the player -- can only move in X direction
        self.velocity = 0
    
    def reset(self):
        self.rect.x = 359
        self.velocity = 0
 
    def up(self):
        """Increases the horizontal velocity"""
        self.velocity -= self.movementspeed
 
    def down(self):
        """Decreases the horizontal velocity"""
        self.velocity += self.movementspeed
 
    def move(self, dx):
        """Move the paddle in the X direction. Don't go out the top or bottom"""
        if self.rect.right + dx > 800:
            self.rect.right = 800
        elif self.rect.left + dx < 0:
            self.rect.left = 0
        else:
            self.rect.x += dx
 
    def update(self):
        """Called to update the sprite. Do this every frame. Handles
        moving the sprite by its velocity"""
        self.move(self.velocity)
