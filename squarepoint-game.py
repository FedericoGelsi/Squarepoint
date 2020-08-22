# Just a simple game made with pygame

# Imports

import sys
import pygame
import random
from pygame.locals import *

# TAGS

PLAYER_COLOR = (4,191,191)
BG_COLOR = (29,51,83)
BAR_COLOR = (41,65,99)
BLACK = (0,0,0)
WHITE = (255,255,255)
SCORE_COLOR = (233,120,5)
LEVEL_COLOR = (191,4,98)

# Funtions
class Screen:
    """
    Represents the screen of the game
    """
    def __init__(self, width: int, height: int):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))
        self.game = Map(self.width, self.height, self.window)        
        self.caption = "SquarePoint"
        self.icon = pygame.image.load("icon.png")
        pygame.display.set_caption(self.caption)
        pygame.display.set_icon(self.icon)

    def draw(self):
        """
        Draws all the objects contained in the game into the screen
        """
        self.game.draw()
        self.window.blit(self.game.window, (0,0))



    def update(self):
        self.game.update()
        self.draw()
    
class Map:
    """
    Represents the background of the game
    """
    def __init__(self, width: int, height: int, window: object):
        self.width = width
        self.height = height
        self.color = BG_COLOR

        self.window = pygame.Surface(window.get_size()).convert()
        self.header = Header(self.width, 70, self.color)
        self.bar = Bar()
        self.playing = 1
        self.menu = Menu()
        self.squares = []
        self.map_limit = self.height
        self.clock = pygame.time.Clock()
        self.fps = 72
    
    def get_fps(self) -> int:
        return self.fps

    def set_width(self, width: int):
        """
        Sets the window width
        """
        self.width = width
    
    def get_width(self) -> int:
        """
        Gets the window width
        """
        return self.width

    def set_height(self, height: int):
        """
        Sets the window height
        """
        self.height = height

    def get_height(self) -> int:
        """
        Gets the window height
        """
        return self.height

    def set_color(self, color: tuple=BLACK):
        """
        Sets the window color
        """
        self.color = color
        
    def draw(self):
        """
        Draws the header and the bar with all of his objects into the game.
        """
        self.window.fill(self.color)
        
        if self.playing == 1:
            self.menu.draw(self.window)
            self.bar.draw(self.window)
        elif self.playing == 2:
            playerscore = self.bar.player.get_score()
            playerlives = self.bar.player.get_lives()
            playerlevel = self.bar.player.get_level()
            self.header.lives_font.set_text(str(playerlives))
            self.header.score_font.set_text(str(playerscore))
            self.header.level_font.set_text(str(playerlevel))
            self.bar.draw(self.window)
            for square in self.squares:
                square.draw(self.window)
            
        elif self.playing == 3:
            pass # Implement
            
        self.header.draw(self.window, self.playing)
        self.window.blit(self.header.block, (0,0))
            
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN and self.playing == 1:
                if event.key == pygame.K_BACKSPACE and len(self.bar.player.get_name()) != 0:
                    self.bar.player.set_name(self.bar.player.get_name()[:len(self.bar.player.get_name())-1])
                elif len(self.bar.player.get_name()) <= 12 and event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN:
                    self.bar.player.set_name(self.bar.player.get_name() + event.unicode)
                self.menu.input_text.set_text(self.bar.player.get_name())

        pygame.event.pump()  # Allow pygame to handle internal actions.
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.bar.player.move_player(-self.bar.player.speed, self.bar.px, self.bar.width)
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.bar.player.move_player(self.bar.player.speed, self.bar.px, self.bar.width)
        if key[pygame.K_RETURN]:
            self.playing = 2
            self.bar.player.set_name(self.bar.player.get_name())

        if self.playing == 1:
            self.header.name_font.set_text(self.bar.player.get_name())

    def update(self):
        """
        Updates the game's objects into the screen
        """ 
        count = 0
        if self.playing == 2:
            self.new_square()
            for i in range(len(self.squares)-1):
                
                if self.squares[i].py >= 800:
                    if self.squares[i].color == PLAYER_COLOR:
                        self.bar.player.subtract_live()
                    self.squares.pop(i)
                elif self.bar.player.shape.colliderect(self.squares[i].shape):
                    if self.squares[i].color == WHITE:
                        self.bar.player.subtract_live()
                    elif self.squares[i].color == PLAYER_COLOR:
                        self.bar.player.add_point()
                        count += 1
                    self.squares.pop(i)
                else:
                    self.squares[i].move_square(self.fps)
            #if self.bar.player.get_lives() == 0:
             #d   self.playing = 2
        pygame.display.flip()       

    def new_square(self):
        self.squares.append(Square(self.bar.player.radius*2))

class Header:
    """
    Represents the header of the game
    """
    def __init__(self, width: int, height: int, color: tuple=BLACK):
        self.playername = ""
        self.width = width
        self.height = height
        self.color = color
        self.block = pygame.Surface((self.width, self.height)).convert()
        self.icon = pygame.transform.scale(pygame.image.load("icon.png"), (50,50)).convert()
        self.name_font = Font(15, PLAYER_COLOR)
        self.lives_font = Font(15, PLAYER_COLOR)
        self.score_font = Font(15, SCORE_COLOR)
        self.level_font = Font(15, LEVEL_COLOR)
        self.data_font = Font(15)

        

    def set_playername(self, name: str):
        """
        Sets the player's name
        """
        self.playername = name

    def set_lives(self, lives: int):
        """
        Set the lives of the player
        """
        self.lives = lives

    def set_level(self, level: int):
        self.level = level

    def get_height(self) -> int:
        return self.height

    def set_color(self, color: tuple=BLACK):
        # Sets the header color
        self.color = color

    def draw(self, window: object, playing: int):
        self.block.fill(self.color)
        pos = ( self.width//2 - self.icon.get_width()//2 , self.height//2 - self.icon.get_height()//2)
        self.block.blit(self.icon, pos)
        pygame.draw.line(self.block, PLAYER_COLOR, (0,self.height), (self.width,self.height), 10)
        
        if playing == 2:
            self.block.blit(self.name_font.render(), (15,15))
            self.data_font.set_text("Lives:")
            self.block.blit(self.data_font.render(), (15,46))
            self.block.blit(self.lives_font.render(), (15+self.data_font.render().get_width(),46))
            self.data_font.set_text("Score:")
            self.block.blit(self.data_font.render(), (288,15))
            self.block.blit(self.score_font.render(), (288+self.data_font.render().get_width(),15))
            self.data_font.set_text("Level:")
            self.block.blit(self.data_font.render(), (288,46))
            self.block.blit(self.level_font.render(), (288+self.data_font.render().get_width(),46))

            # PROGRESS TO DO

        window.blit(self.block, (0,0))

class Square:
    def __init__(self, size):
        self.color = self.set_random_color()
        self.px = self.set_init_position()
        self.py = 0
        self.size = size
        self.endx = self.set_endpoint()
        self.endy = 900
        self.m = (self.endy - self.py) / (self.endx - self.px)
        self.speed = 50
        self.shape = pygame.Rect(self.px, self.py, self.size, self.size)
    
    def set_random_color(self):
        if random.randint(0, 100) >= 60:
            return PLAYER_COLOR
        else:
            return WHITE

    def set_init_position(self) -> int:
        return random.randint(100, 500)

    def move_square(self, fps: int):
        self.px += self.speed / fps
        self.py = self.m * self.px

    
    def set_endpoint(self) -> int:
        return random.randint(50,450)

    def draw(self, window: object):
        self.shape = pygame.Rect(self.px, self.py, self.size, self.size)
        pygame.draw.rect(window, self.color, self.shape)

class Menu:
    def __init__(self):
        self.p_bar = Font(10,SCORE_COLOR)
        self.up_arrow = pygame.transform.scale(pygame.image.load("up_arrow.png"), (25,25)).convert()
        self.left_arrow = pygame.transform.scale(pygame.image.load("left_arrow.png"), (25,25)).convert()
        self.right_arrow = pygame.transform.scale(pygame.image.load("right_arrow.png"), (25,25)).convert()
        self.welcome = Font(24, LEVEL_COLOR)
        self.play = Font(20, PLAYER_COLOR)
        self.exit = Font(15, PLAYER_COLOR)
        self.lw = 2
        self.input_text = Font(22, PLAYER_COLOR)
    
    def draw(self, window: object):
        # DRAW PROGRESS BAR HELP
        self.p_bar.set_text("Here your can see the")
        window.blit(self.p_bar.render(), (65,100))
        self.p_bar.set_text("progress on the level")
        window.blit(self.p_bar.render(), (65,110+self.p_bar.render().get_height()))
        window.blit(self.up_arrow, (40,75))

        # WELCOME TO SQUAREPOINT
        self.welcome.set_text("Welcome to")
        window.blit(self.welcome.render(), (window.get_width()//2-self.welcome.render().get_width()//2,160))
        self.welcome.set_text("SquarePoint!!")
        window.blit(self.welcome.render(), (window.get_width()//2-self.welcome.render().get_width()//2,170+self.welcome.render().get_height()))

        # PRESS ENTER TO PLAY
        self.play.set_text("Press ")
        pos = 60
        window.blit(self.play.render(), (pos,315))
        pos +=self.play.render().get_width()
        self.play.set_color(SCORE_COLOR)
        self.play.set_text("enter ")
        window.blit(self.play.render(), (pos,315))
        pos +=self.play.render().get_width()
        self.play.set_color(PLAYER_COLOR)
        self.play.set_text("to play")
        window.blit(self.play.render(), (pos,315))

        # PRESS ESCAPE TO EXIT
        self.exit.set_text("Press ")
        pos = 95
        window.blit(self.exit.render(), (pos,846))
        pos +=self.exit.render().get_width()
        self.exit.set_color(LEVEL_COLOR)
        self.exit.set_text("escape ")
        window.blit(self.exit.render(), (pos,846))
        pos +=self.exit.render().get_width()
        self.exit.set_color(PLAYER_COLOR)
        self.exit.set_text("to exit")
        window.blit(self.exit.render(), (pos,846))

        # ENTER YOUR NAME
        self.exit.set_text("Enter your name:")
        window.blit(self.exit.render(), (window.get_width()//2-self.exit.render().get_width()//2,450))
        textbox = pygame.Rect((100,491),(300,40))
        pygame.draw.rect(window, PLAYER_COLOR, textbox, 2 )
        window.blit(self.input_text.render(), (110, 499))
        if self.lw == 2:
            pygame.draw.line(window, PLAYER_COLOR, (110 + self.input_text.render().get_width(), 499), (110 + self.input_text.render().get_width(),499+25), self.lw )
            self.lw = 0
        elif self.lw == 0:
            pygame.draw.line(window, PLAYER_COLOR, (110 + self.input_text.render().get_width(), 499), (110 + self.input_text.render().get_width(),499+25), self.lw )
            self.lw = 2

        # HELP
        self.p_bar.set_text("Avoid the white squares and")
        window.blit(self.p_bar.render(), (window.get_width()//2-self.p_bar.render().get_width()//2,640))
        self.p_bar.set_text("progress on the level")
        window.blit(self.p_bar.render(), (window.get_width()//2-self.p_bar.render().get_width()//2,650+self.p_bar.render().get_height()))

        # HELP ARROW
        self.p_bar.set_text("Move left")
        window.blit(self.p_bar.render(), (65,810))
        window.blit(self.left_arrow, (100,770))
        self.p_bar.set_text("Move right")
        window.blit(self.p_bar.render(), (331,810))
        window.blit(self.right_arrow, (370,770))

class GameOver:
    def __init__(self):
        self.x = 0

        # IMPLEMENTAR

class Font:
    """
    Used to create an define a font.
    """
    def __init__(self, size: int , color: tuple=WHITE):
        self.type = pygame.font.Font("Pixel_font.ttf", size)
        self.fontcolor = color
        self.text = ""

    def set_text(self, text: str):
        self.text = text

    def set_color(self, color: tuple):
        self.fontcolor = color

    def render(self):
        return self.type.render(self.text, False, self.fontcolor)

class Bar:
    """
    Represents the screen of the game
    """
    def __init__(self):
        self.px = 50
        self.py = 700
        self.width = 400
        self.height = 40
        self.color = BAR_COLOR
        self.player = Player(self.px+self.width//2, self.py+self.height//2, self.height//2)

    def set_position(self, px: int, py: int):
        self.px = px
        self.py = py

    def set_color(self, color: tuple):
        self.color = color

    def draw(self, window: object):
        SP_R = pygame.Rect(self.px+self.height//2, self.py, self.width-self.height, self.height)
        pygame.draw.rect(window, self.color, SP_R)
        SP_C = (self.px+self.height//2, self.py+self.height//2)
        pygame.draw.circle(window, self.color , SP_C  , self.height//2)
        SP_C = (self.width+ self.height//2, self.py+self.height//2)
        pygame.draw.circle(window, self.color , SP_C  , self.height//2)
        self.player.draw(window)

class Player:
    def __init__(self, px: int, py: int, radius: int):
        self.px = px
        self.py = py
        self.radius = radius
        self.color = PLAYER_COLOR
        self.score = 0
        self.lives = 5
        self.level = 1
        self.name = ""
        self.speed = 10
        self.shape = None

    def set_color(self, color: tuple):      
        self.color = color

    def move_player(self, px: int, leftlimit: int, rightlimit: int):
        if leftlimit + self.radius <= self.px + px <= rightlimit + self.radius:
            self.px += px


    def add_point(self):
        self.score += 10
        if self.score%100 == 0:
            self.add_live()
        
    def get_score(self) -> int:
        return self.score

    def add_live(self):
        self.lives+=1
    
    def subtract_live(self):
        if self.lives > 0:
            self.lives-=1

    def get_lives(self) -> int:
        return self.lives
    
    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def add_level(self):
        self.level += 1

    def get_level(self) -> int:
        return self.level
    
    def draw(self, window: object):
        self.shape = pygame.draw.circle(window, self.color , (self.px, self.py), self.radius)
    

def main():
    win = Screen(500,900)
    while True:
        win.game.handle_event()
        win.update()
        win.game.clock.tick(win.game.get_fps()) 

if __name__ == '__main__':
    main()

