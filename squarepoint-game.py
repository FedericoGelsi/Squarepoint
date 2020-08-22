# Just a simple game made with pygame

# Imports

import sys
import pygame
import random
import math
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
        self.game_over = GameOver()
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
                
            # PROGRESS TO DO        
            if self.bar.player.get_level() > 1:
                partition = (self.width / (50* (2**(self.bar.player.get_level()-1))))*10
            else: 
                partition = (self.width / (50* (2**self.bar.player.get_level())))*10
            self.header.set_progress(partition, self.bar.player.get_sq())

        elif self.playing == 3:
            self.game_over.draw(self.window, self.bar.player.get_name(), self.bar.player.get_score())
            
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
            self.bar.player.reset()
            self.squares.clear()

        if self.playing == 1:
            self.header.name_font.set_text(self.bar.player.get_name())

    def update(self):
        """
        Updates the game's objects into the screen
        """ 
        i = 0
        if self.playing == 2:
            if len(self.squares) < 2:
                self.new_square(self.bar.player.get_level())
            while i < len(self.squares)-1:
                if len(self.squares) < 5 and self.squares[i].py > 400:
                    self.new_square(self.bar.player.get_level())
                    self.flag = True
                if self.squares[i].py >= self.bar.py + 100:
                    if self.squares[i].color == PLAYER_COLOR:
                        self.bar.player.subtract_live()
                    del self.squares[i]
                    break
                elif self.squares[i].shape.colliderect(self.bar.player.shape):
                    if self.squares[i].color == WHITE:
                        self.bar.player.subtract_live()
                    elif self.squares[i].color == PLAYER_COLOR:
                        self.bar.player.add_point()
                    del self.squares[i]
                    break
                else:
                    self.squares[i].move_square(self.fps)
                i += 1
            if self.bar.player.get_score() == (50* (2**(self.bar.player.get_level()))):
                self.bar.player.q_sq = 0
                self.bar.player.add_level()
            if self.bar.player.get_lives() == 0:
                self.playing = 3
        pygame.display.flip()       

    def new_square(self, speed: int):
        self.squares.append(Square(self.bar.player.radius*2, speed))

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
        self.progress = 0
        

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
    
    def set_progress(self, partition, progress):
        self.progress = partition* progress

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
            pygame.draw.line(self.block, LEVEL_COLOR, (0,self.height), (self.progress,self.height), 10)
        window.blit(self.block, (0,0))

class Square:
    def __init__(self, size: int, speed:int):
        self.color = self.set_random_color()
        self.px = self.set_init_position()
        self.py = 0
        self.limit = 900
        self.size = size
        self.speed = math.log2(speed*10)*70
        self.shape = pygame.Rect(self.px, self.py, self.size, self.size)

    def set_random_color(self):
        if random.randint(0, 100) >= 60:
            return PLAYER_COLOR
        else:
            return WHITE

    def set_init_position(self) -> int:
        return random.randint(50, 400)

    def move_square(self, fps: int):
        self.py += self.speed/ fps

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
        self.game_over = Font(24, LEVEL_COLOR)
        self.score = Font(20, PLAYER_COLOR)
        self.play = Font(20, PLAYER_COLOR)
        self.exit = Font(15, PLAYER_COLOR)

    def draw(self, window: object, playername: str, score: int):
        # GAME OVER
        self.game_over.set_text("Game over !!")
        window.blit(self.game_over.render(), (window.get_width()//2-self.game_over.render().get_width()//2,222))
       
        # SCORE 1
        self.score.set_text(playername + " your")
        pos = window.get_width()//2-self.score.render().get_width()//2
        self.score.set_text(playername)
        window.blit(self.score.render(), (pos,350))
        pos +=self.score.render().get_width()
        self.score.set_color(WHITE)
        self.score.set_text(" your")
        window.blit(self.score.render(), (pos,350))

        # SCORE 2
        self.score.set_text("score is " + str(score))
        pos = window.get_width()//2-self.score.render().get_width()//2
        self.score.set_text("score is ")
        window.blit(self.score.render(), (pos,380))
        pos +=self.score.render().get_width()
        self.score.set_text(str(score))
        self.score.set_color(SCORE_COLOR)
        window.blit(self.score.render(), (pos,380))

        # PRESS ENTER TO PLAY
        self.play.set_text("Press enter to")
        pos = window.get_width()//2-self.play.render().get_width()//2
        self.play.set_text("Press ")
        window.blit(self.play.render(), (pos,530))
        pos +=self.play.render().get_width()
        self.play.set_color(SCORE_COLOR)
        self.play.set_text("enter ")
        window.blit(self.play.render(), (pos,530))
        pos +=self.play.render().get_width()
        self.play.set_color(PLAYER_COLOR)
        self.play.set_text("to")
        window.blit(self.play.render(), (pos,530))
        self.play.set_text("play again")
        window.blit(self.play.render(), (window.get_width()//2-self.play.render().get_width()//2,560))

        # PRESS ESCAPE TO EXIT
        self.exit.set_text("Press escape to exit")
        pos = window.get_width()//2-self.exit.render().get_width()//2
        self.exit.set_text("Press ")
        window.blit(self.exit.render(), (pos,645))
        pos +=self.exit.render().get_width()
        self.exit.set_color(LEVEL_COLOR)
        self.exit.set_text("escape ")
        window.blit(self.exit.render(), (pos,645))
        pos +=self.exit.render().get_width()
        self.exit.set_color(PLAYER_COLOR)
        self.exit.set_text("to exit")
        window.blit(self.exit.render(), (pos,645))

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
        self.q_sq = 0

    def set_color(self, color: tuple):      
        self.color = color

    def move_player(self, px: int, leftlimit: int, rightlimit: int):
        if leftlimit + self.radius <= self.px + px <= rightlimit + self.radius:
            self.px += px


    def add_point(self):
        self.score += 10
        self.q_sq += 1
        
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
        self.add_live()

    def get_level(self) -> int:
        return self.level
    
    def get_sq( self) -> int:
            return self.q_sq
    
    def draw(self, window: object):
        self.shape = pygame.draw.circle(window, self.color , (self.px, self.py), self.radius)
    
    def reset(self):
        self.score = 0
        self.lives = 5
        self.level = 1

def main():
    win = Screen(500,900)
    while True:
        win.game.handle_event()
        win.update()
        win.game.clock.tick(win.game.get_fps()) 

if __name__ == '__main__':
    main()

