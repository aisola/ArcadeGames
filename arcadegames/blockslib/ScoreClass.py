#--------------------------------------------------------------------------------
# @file   : ScoreClass.py
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

class Score(pygame.sprite.Sprite):
    """A sprite for the score."""
 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
 
        self.xy = [50,15]  # save xy -- will center our rect on it when we change the score
 
        self.font = pygame.font.Font(None, 30)  # load the default font, size 50
        
        self.balls = 3
        self.reRender()
 
    def update(self):
        pass
    
    def up(self):
        self.balls += 1
        self.reRender()
    
    def down(self):
        self.balls -= 1
        self.reRender()
 
    def reset(self):
        self.balls = 3
        self.reRender()
 
    def reRender(self):
        """Updates the score. Renders a new image and re-centers at the initial coordinates."""
        self.image = self.font.render("Lives: %d"%(self.balls), True, white)
        self.rect = self.image.get_rect()
        self.rect.center = self.xy