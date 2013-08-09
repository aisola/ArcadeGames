#!/usr/bin/python -O
#--------------------------------------------------------------------------------
# @file        : arcade-blocks-beta
# @author      : Abram C. Isola
# @license     : Unlicensed; Closed Source
# @version     : 2.0 BETA
# @precondition: Library pygame
# @precondition: Library blockslib
# @summary     : This is an attempt to optimize and improve the code readability
#                and performance of the v1 of "arcade-blocks". It will also add
#                several features such as Menus, High Scores, etc.
#--------------------------------------------------------------------------------

# import modules
try:
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
    
    # import Game Attributes
    from blockslib import *

except ImportError, err:
    print "%s Failed to Load Module: %s" % (__file__, err)
    sys.exit(1)
            

class Game(object):
    
    def __init__(self):
        """Called when the the Game object is initialized. Initializes
        pygame and sets up our pygame window and other pygame tools
        that we will need for more complicated tutorials."""
        
        # load and set up pygame
        pygame.init()
        
        # create our window & set title
        self.window = pygame.display.set_mode([800, 600])
        pygame.display.set_caption('Arcade BLOCKS')
        pygame.display.set_icon(pygame.image.load(os.path.join("images","pong_ball_large.gif")))
        
        # clock for ticking & set font (size 36)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.canserve = True
        
        # tell pygame to only pay attention to certain events
        # we want to know if the user hits the X on the window, and we
        # want keys so we can close the window with the esc key, and/or
        # control the on-screen paddle.
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        
        # a sprite rendering group for our blocks, ball, and paddle
        self.blocks=pygame.sprite.RenderPlain()
        self.lifeBlocks=pygame.sprite.RenderPlain()
        self.sprites = pygame.sprite.RenderUpdates()
        
        # make background -- all white, with black line down the middle
        self.background = pygame.Surface((800,600))
        self.background.fill(black)
        
        self.background_height = self.background.get_height()
        
        # flip the display so the background is on there
        pygame.display.flip()
        
        # Create player and add it to the sprites
        self.player = Player()
        self.sprites.add(self.player)
        
        # Create ball and add it to the sprites
        self.ball = Ball([400,self.background_height-25])
        self.sprites.add(self.ball)
        
        # Create score and add it to the sprites
        self.score = Score()
        self.sprites.add(self.score)
        
        # Create 5 rows of blocks using the below
        # defined createBlocks procedure
        self.createBlocks(5)
        self.writeText("Press the Spacebar to Serve!",canserve=True)
    
    def createBlocks(self,ROWS):
        """Creates an algorithm that creates ROWS number of rows."""
        # Set individual Block width & height constants
        BLOCK_WIDTH  = 23
        BLOCK_HEIGHT = 15
        
        # set the pixels from the top of the row.
        PIXELS_FROM_TOP = 80
        
        # Set the "random" distribution of Life Blocks
        LIFE_BLOCK_DISTRIBUTON = random.randint(30, 58)
        
        # Initialize the count of blocks. :0
        NUMBER_OF_BLOCKS = 0
        
        # For row in a range of row 1 to ROWS:
        for row in range(ROWS):
            
            # For each (32) columns in the row.
            for column in range(0,32):
                
                # Set the block size constant.
                BLOCK_SIZE = column * (BLOCK_WIDTH + 2) +1
                
                
                # if there are no blocks yet: create one;
                # else if it is supposed to be a life block: create a life block;
                # -> if the life block should yield two lives: color the block yellow;
                # -> otherwise: make it yield one life and color the block red.
                # -> THEN: add the life block to the lifeblocks rendering group.
                # otherwise: create a normal block.
                if NUMBER_OF_BLOCKS == 0:
                    block = Block(blue, BLOCK_SIZE, PIXELS_FROM_TOP)
                elif NUMBER_OF_BLOCKS % LIFE_BLOCK_DISTRIBUTON == 0:
                    if random.randint(1, 5) == 1:
                        block = Block(yellow, BLOCK_SIZE, PIXELS_FROM_TOP)
                    else:
                        block = Block(red, BLOCK_SIZE, PIXELS_FROM_TOP)
                    self.lifeBlocks.add(block)
                else:
                    block = Block(blue, BLOCK_SIZE, PIXELS_FROM_TOP)
                
                # Add the block to the proper rendering groups.
                self.blocks.add(block)
                self.sprites.add(block)
                
                # update the block count
                NUMBER_OF_BLOCKS += 1
            
            # redefine how many pixels from the top the next row will be. 
            PIXELS_FROM_TOP += BLOCK_HEIGHT + 2
        return True
    
    # (MAY BE REPLACED MY MENU-IZATION)
    def writeText(self,display_text,canserve=True):
        """Helper function for creating text on screen."""
        self.text=self.font.render(display_text, True, white)
        textpos = self.text.get_rect(centerx=self.background.get_width()/2)
        textpos.top = 300
        self.window.blit(self.text, textpos)
        pygame.display.flip()
        self.ball.canserve = canserve
        return True
    
    # (MAY BE REPLACED MY MENU-IZATION)
    def killText(self):
        """Helper function for killing text on screen."""
        self.text.fill(black)
        textpos = self.text.get_rect(centerx=self.background.get_width()/2)
        textpos.top = 300
        self.window.blit(self.text, textpos)
        pygame.display.flip()
    
    
    def run(self):
        """Runs the game. Contains the game loop that computes and renders
        each frame."""
        
        print 'Starting Event Loop'
        
        running = True
        # run until something tells us to stop
        while running:
            
            # tick pygame clock (Limit: 60 Frames/Second [FPS])
            self.clock.tick(60)
            
            # handle pygame events -- if user closes game, stop running
            running = self.handleEvents()
            
            # handle ball
            self.manageBall()
            
            # update the title bar with our frames per second
            pygame.display.set_caption('Arcade BLOCKS ||  %d fps' % self.clock.get_fps())
            
            # update all of the sprites in the main rendering group.
            for sprite in self.sprites:
                sprite.update()
            
            # render our sprites
            self.sprites.clear(self.window, self.background)    # clears the window where the sprites currently are, using the background
            dirty = self.sprites.draw(self.window)              # calculates the 'dirty' rectangles that need to be redrawn
            
            # blit the dirty areas of the screen
            pygame.display.update(dirty)                        # updates just the 'dirty' areas
        
        print 'Quitting. Thanks for playing'
    
    def handleEvents(self):
        # Process the events in the game
        for event in pygame.event.get():
            
            # if the event is clicking the window X
            if event.type == pygame.QUIT:
                return False
            
            # handle user input
            elif event.type == KEYDOWN:
                # if the user presses escape, quit the event loop.
                if event.key == K_ESCAPE:
                    return False
                
                # player control (LEFT ARROW and RIGHT ARROW)
                if event.key == K_LEFT:
                    if self.ball.vely != 0 and self.ball.velx != 0:
                        self.player.up()
                if event.key == K_RIGHT:
                    if self.ball.vely != 0 and self.ball.velx != 0:
                        self.player.down()
                
                # (MAY BE REPLACED MY MENU-IZATION)
                # player control (n Key)
                if event.key == K_n:
                    # if the ball is still:
                    if self.ball.vely == 0 and self.ball.velx == 0:
                        # reset the player, the ball,
                        # re-create the blocks, reset the lives & score
                        self.player.reset()
                        self.ball.reset()
                        self.createBlocks(5)
                        self.killText()
                        self.ball.setLives(3)
                        self.score.reset()
                        self.writeText("Press the Spacebar to Serve!",canserve=True)
                
                # THE LIFE ADDER CHEAT
                # if event.key == K_l:
                #     self.ball.addLife()
                #     self.score.up()
                
                # player control (SPACE BAR)
                if event.key == K_SPACE:
                    # if the ball is still and you can serve:
                    if self.ball.vely == 0 and self.ball.velx == 0:
                        if self.ball.canserve == True:
                            # take a life and kill text
                            self.score.down()
                            self.killText()
                        # serve ball
                        self.ball.serve()
            
            elif event.type == KEYUP:
                # player control
                if event.key == K_LEFT:
                    if self.ball.vely != 0 and self.ball.velx != 0:
                        self.player.down()
                if event.key == K_RIGHT:
                    if self.ball.vely != 0 and self.ball.velx != 0:
                        self.player.up()
        
        return True
    
    def manageBall(self):
        """This basically runs the game. Moves the ball and handles
        wall and paddle collisions."""
 
        # move the ball according to its velocity
        self.ball.rect.x += self.ball.velx
        self.ball.rect.y += self.ball.vely
 
        # check if ball is off the top
        if self.ball.rect.top < 0:
            self.ball.rect.top = 1
            self.ball.vely *= -1
 
        # check if ball is off the bottom
        elif self.ball.rect.bottom > 600:
            self.ball.reset()
            self.player.reset()
            self.ball.takeLife()
            if self.ball.hasLife():
                self.writeText("Press the Spacebar to Serve!",canserve=True)
            else:
                self.writeText("Game Over. Press 'n' to start a new game!",canserve=False)
        
        # check if ball is off the left side
        if self.ball.rect.left < 0:
            self.ball.rect.left = 1
            self.ball.velx *= -1
 
        # check if ball is off the right side
        elif self.ball.rect.right > 800:
            self.ball.right = 599
            self.ball.velx *= -1
        
        # check for collisions with the paddles using pygames collision functions
        collided = pygame.sprite.spritecollide(self.ball, [self.player], dokill=False)
 
        # if the ball hit a paddle, it will be in the collided list
        if len(collided) > 0:
            hitpaddle = collided[0]
 
            # reverse the x velocity on the ball
            self.ball.vely *= -1
 
            # need to make sure the ball is no longer in the paddle -- going to move it again manually
            self.ball.rect.y += self.ball.vely
            
            # give a little of the paddle's velocity to the ball
            self.ball.velx += hitpaddle.velocity/10.0
        
        # Check for collisions between the ball and the blocks
        self.deadblocks = pygame.sprite.spritecollide(self.ball, self.blocks, True)
        
        # If we actually hit a block, bounce the ball
        if len(self.deadblocks) > 0:
            for blks in self.deadblocks:
                if blks.color == "red":
                    self.ball.addLife()
                    self.score.up()
                elif blks.color == "yellow":
                    self.ball.addLife()
                    self.ball.addLife()
                    self.score.up()
                    self.score.up()
            self.ball.vely *= -1
        
        if len(self.blocks) <= 0:
            self.ball.vely = 0
            self.ball.velx = 0
            self.writeText("You Win!!! Press 'n' to start a new game!",canserve=False)

if __name__ == "__main__":
    game = Game()
    game.run()
