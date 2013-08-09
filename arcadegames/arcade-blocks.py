#!/usr/bin/python
# 
# Arcade BLOCKS
# @license: IOAL-1.0.txt
# 

# import modules
try:
    import sys, os, math, random
    import pygame
    
    from pygame.locals import *
    
    # Define some global colors
    global black, white, blue, red
    red    = (255,   0,   0)
    yellow = (255, 255,   0)
    blue   = (  0,   0, 255)
    white  = (255, 255, 255)
    black  = (  0,   0,   0)

except ImportError, err:
    print "%s Failed to Load Module: %s" % (__file__, err)
    sys.exit(1)

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
        # want keys so we can close the window with the esc key
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
        
        # create player & ball
        self.player = Player()
        self.sprites.add(self.player)
        
        self.ball = Ball([400,self.background_height-25])
        self.sprites.add(self.ball)
        
        self.score = Score()
        self.sprites.add(self.score)
        
        self.createBlocks()
        self.writeText("Press the Spacebar to Serve!",canserve=True)
    
    def createBlocks(self):
        # create all blocks (5 rows)
        top = 80
        block_width=23
        block_height=15
        lblockdist = random.randint(30, 58)
        is_double_life = random.randint(1,5)
        numofblocks = 0
        for row in range(5):
            # 32 columns of blocks
            for column in range(0,32):
                # Create a block (color,x,y)
                BLOCK_SIZE = column*(block_width+2)+1
                if numofblocks == 0:
                    block=Block(blue,BLOCK_SIZE,top)
                elif numofblocks % lblockdist == 0:
                    if is_double_life == 1:
                        block=Block(yellow,BLOCK_SIZE,top)
                    else:
                        block=Block(red,BLOCK_SIZE,top)
                    self.lifeBlocks.add(block)
                else:
                    block=Block(blue,BLOCK_SIZE,top)
                    
                self.blocks.add(block)
                self.sprites.add(block)
                
                numofblocks += 1
            # Move the top of the next row down
            top += block_height+2
        return True
    
    def writeText(self,display_text,canserve=True):
        self.text=self.font.render(display_text, True, white)
        textpos = self.text.get_rect(centerx=self.background.get_width()/2)
        textpos.top = 300
        self.window.blit(self.text, textpos)
        pygame.display.flip()
        self.ball.canserve = canserve
        return True
    
    def killText(self):
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
            
            # tick pygame clock
            # you can limit the fps by passing the desired frames per second to tick()
            self.clock.tick(60)
            
            # handle pygame events -- if user closes game, stop running
            running = self.handleEvents()
            
            # handle ball
            self.manageBall()
            
            # update the title bar with our frames per second
            pygame.display.set_caption('Arcade BLOCKS ||  %d fps' % self.clock.get_fps())
            
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
            if event.type == pygame.QUIT:
                return False
            
            # handle user input
            elif event.type == KEYDOWN:
                # if the user presses escape, quit the event loop.
                if event.key == K_ESCAPE:
                    return False
                
                # player control
                if event.key == K_LEFT:
                    if self.ball.vely != 0 and self.ball.velx != 0:
                        self.player.up()
                if event.key == K_RIGHT:
                    if self.ball.vely != 0 and self.ball.velx != 0:
                        self.player.down()
                
                if event.key == K_n:
                    if self.ball.vely == 0 and self.ball.velx == 0:
                        self.player.reset()
                        self.ball.reset()
                        self.createBlocks()
                        self.killText()
                        self.ball.setLives(3)
                        self.score.reset()
                        self.writeText("Press the Spacebar to Serve!",canserve=True)
                
                if event.key == K_l:
                    self.ball.addLife()
                    self.score.up()
                
                if event.key == K_SPACE:
                    if self.ball.vely == 0 and self.ball.velx == 0:
                        if self.ball.canserve == True:
                            self.score.down()
                            self.killText()
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
