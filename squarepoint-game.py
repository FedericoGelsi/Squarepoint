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

    def draw(self):
        """
        Draws all the objects contained in the game into the screen
        """
        self.game.draw()
        self.window.blit(self.game.window, (0,0))


class Map:
    """
    Represents the background of the game
    """
    def __init__(self, width: int, height: int, window: object):
        self.width = width
        self.height = height
        self.color = BG_COLOR
        self.caption = "SquarePoint"
        self.icon = pygame.image.load("icon.png")
        self.window = pygame.Surface(window.get_size()).convert()
        self.header = Header(self.width, 70, self.icon, self.color)
        self.bar = Bar()
        self.playing = 2
        pygame.display.set_caption(self.caption)
        pygame.display.set_icon(self.icon)
       

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
        self.header.draw(self.window, self.playing)
        self.window.blit(self.header.block, (0,0))
        self.bar.draw(self.window)

    def update(self):
        """
        Updates the game's objects into the screen
        """
        pygame.display.flip()
        

class Header:
    """
    Represents the header of the game
    """
    def __init__(self, width: int, height: int, icon: object, color: tuple=BLACK):
        self.icon = pygame.image.load("icon.png")
        self.playername = ""
        self.width = width
        self.height = height
        self.color = color
        self.block = pygame.Surface((self.width, self.height)).convert()
        self.icon = pygame.transform.scale(icon, (50,50)).convert()
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
        self.height = 45
        self.color = BAR_COLOR
        self.player = Player(self.px+self.width//2, self.py+self.height//2, self.height//2)
        self.player2 = Player(self.px+self.width//4, self.py+self.height//2, self.height//2)

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
        SP_C = (self.px+self.width-self.height//2, self.py+self.height//2)
        pygame.draw.circle(window, self.color , SP_C  , self.height//2)
        self.player.draw(window)
        self.player2.set_color(SCORE_COLOR)
        self.player2.draw(window)


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

    def set_color(self, color: tuple):      
        self.color = color

    def move_player(self, px: int):
        self.px = px

    def add_point(self):
        self.score += 10
        if self.score%100 == 0:
            self.add_live()
        
    def get_score(self) -> int:
        return self.score

    def add_live(self):
        self.lives+=1

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

    def is_collition(self, object: object) -> bool:
        pass    # Implementar
    
    def draw(self, window: object):
        pygame.draw.circle(window, self.color , (self.px, self.py)  , self.radius)

    

def main():
    win = Screen(500,900)
    win.game.bar.player.set_name("Killerex")
    playername = win.game.bar.player.get_name()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        playerscore = win.game.bar.player.get_score()
        playerlives = win.game.bar.player.get_lives()
        playerlevel = win.game.bar.player.get_level()
        win.game.header.name_font.set_text(playername)
        win.game.header.lives_font.set_text(str(playerlives))
        win.game.header.score_font.set_text(str(playerscore))
        win.game.header.level_font.set_text(str(playerlevel))
        win.game.bar.player.add_live()
        win.game.bar.player.add_point()
        win.game.bar.player.add_level()
        win.draw()
        win.game.update()


if __name__ == '__main__':
    main()

