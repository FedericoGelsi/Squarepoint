# Just a simple game made with pygame

# Imports

import sys
import pygame
import random
from pygame.locals import *
# Funtions
class Map:
    def __init__(self, width, height):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        self.color = None
        self.caption = "SquarePoint"
        self.icon = pygame.image.load("icon.png")
        self.window = self.create_window((29,51,83))
        self.header = None
       

    def set_width(self, width):
        """Sets the window width"""
        self.width = width
    
    def get_width(self):
        """Gets the window width"""
        return self.width

    def set_height(self, height):
        """Sets the window height"""
        self.height = height

    def get_height(self):
        """Gets the window height"""
        return self.height

    def set_color(self, color):
        """Sets the window color"""
        self.color = color
    
    def create_window(self, color=(0,0,0)):
        self.set_color(color)
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)
        pygame.display.set_icon(self.icon)
        self.draw()
        self.header = Header(self.width, 50)
        self.header.create_header(self.window)#, self.color)    SEt color later

    def draw(self):
        self.window.fill(self.color)

    def update(self):
        pygame.display.update()
        

class Header:
    def __init__(self, width, height):
        self.icon = pygame.image.load("icon.png")
        self.playername = ""
        self.width = width
        self.height = height
        self.color = None

    def set_playername(self, name):
        self.playername = name

    def set_lives(self, lives):
        self.lives = lives

    def set_level(self, level):
        self.level = level

    def get_height(self):
        return self.height

    def set_color(self, color):
        """Sets the header color"""
        self.color = color

    def create_header(self, window, color=(0,0,0)):
        """Create the header"""
        self.set_color(color)
        block = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(window, self.color, block)


class Bar:
    def __init__(self):
        self.px = px
        self.py = py
        self.width = width
        self.height = height
        self.color = None

    def set_position(self, px, py):
        self.px = px
        self.py = py

    def set_color(self, color):
        self.color = color

    def draw(self):
        


class Player:
    def __init__(self, px, py, radius):
        self.px = px
        self.py = py
        self.radius = radius
        self.color = None

    def draw(self):

    

def main():
    game = Map(500,900)
    while True:
        game.update()


if __name__ == '__main__':
    main()

