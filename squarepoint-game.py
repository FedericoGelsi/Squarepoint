# Just a simple game made with pygame

# Imports

import sys
import pygame
import random
from pygame.locals import *
# Global 'variables
# CONSTANTS
FPS = 60                                # Frames per second setting
WINDOWWIDTH = 320
WINDOWHEIGHT = 640
GAMEWIDTH = WINDOWWIDTH
GAMEHEIGHT_END = WINDOWHEIGHT*2//3
SCOREWIDTH = WINDOWWIDTH
SCOREHEIGHT_START = GAMEHEIGHT_END
SCOREHEIGHT_END = WINDOWHEIGHT
OBJ_SIZE = (25, 25)
OBJ_SPEED = 200
SP_X = 240
# COLORS
BLACK = (27, 27, 27)                 # Black
DARK_BLACK = (46, 47, 66)            # Dark Black
WHITE = (255, 255, 255)              # White
GREEN = (95, 208, 159)               # Green
pygame.font.init()
FONT_NAME = "Roboto-Regular.ttf"
FONT = pygame.font.Font(FONT_NAME, 20)
SC_FONT = pygame.font.Font(FONT_NAME, 40)
#KEYS
LEFT = 'left'
RIGHT = 'right'

# OBJECTS

SQUARE_COLOR = WHITE
CIRCLE_COLOR = GREEN
WINDOW_COLOR = BLACK
SLIDE_COLOR = DARK_BLACK

# Funtions
def main():
    global FPSCLOCK, DISPLAYSURF
    SQUARES = []
    pygame.init()
    look = 0
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('SquarePoint')
    newSquare(SQUARES)
    while True:
        NP = menu()
        while not(NP[6]):
            look = play( NP , SQUARES , look)
    printBox_2(NP[7])

def menu():                             # Main menu
    flag = False
    DISPLAYSURF.fill(WINDOW_COLOR)
    printBox_1()
    printBox_3()
    while not(flag):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_e:
                    flag = True
                    NP = newPlayer()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
    return NP
def printBox_1():
    TITLE_FONT = FONT.render('SquarePoint', True , WHITE)
    TITLE = TITLE_FONT.get_rect()
    TITLE.topleft = ((WINDOWWIDTH/2)-50 , WINDOWHEIGHT/6)
    DISPLAYSURF.blit(TITLE_FONT , TITLE)
    return False

def printBox_2( SC ):
    GOV_FONT = FONT.render('GAME OVER', True , GREEN)
    GOV = GOV_FONT.get_rect()
    GOV.topleft = ((WINDOWWIDTH/2)-50 , WINDOWHEIGHT/2)
    DISPLAYSURF.blit(GOV_FONT , GOV)
    SC_FONT = FONT.render(str(SC), True , GREEN)
    SC = SC_FONT.get_rect()
    SC.topleft = ((WINDOWWIDTH/2)-50 , WINDOWHEIGHT*4/6)
    DISPLAYSURF.blit(SC_FONT , SC)
    return False

def printBox_3():
    KEY_FONT = FONT.render('Press E to start...', True , WHITE)
    KEY = KEY_FONT.get_rect()
    KEY.topleft = (WINDOWWIDTH/2-70 , WINDOWHEIGHT*5/6)
    DISPLAYSURF.blit(KEY_FONT , KEY)
    return False
def play( NP , SQUARES , look):
    Q_SQ = len(SQUARES)
    DISPLAYSURF.fill(WINDOW_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
           if (event.key == K_LEFT or event.key == K_a):
               NP[4] = LEFT
           elif (event.key == K_RIGHT or event.key == K_d):
               NP[4] = RIGHT
           elif event.key == K_ESCAPE:
               pygame.quit()
    movePlayer(NP)
    # menu()
    space_move()
    drawPlayer(NP)
    if moveSquare(Q_SQ , SQUARES , NP):
        look -= 1
    pygame.display.update()
    if SQUARES[look][1] > GAMEHEIGHT_END*1//3:
        newSquare(SQUARES)
        look += 1
    FPSCLOCK.tick(FPS)
    return look
def newSquare(sqs):
    C_GR = random.uniform(0.0, 10.0)
    newSQ = []      # [ x , y , xf , xi]
    newSQ.append(random.randint(OBJ_SIZE[0], GAMEWIDTH)) # Generate x position
    newSQ.append(0) # y axis
    if newSQ[0] < GAMEWIDTH/2:
        m = newSQ[0] - random.randint(newSQ[0]+1, GAMEWIDTH-OBJ_SIZE[0])
    elif newSQ[0] >= GAMEWIDTH/2:
        m = newSQ[0] - random.randint(1, newSQ[0]-1)
    m = -400/m
    newSQ.append(m)
    newSQ.append(newSQ[0])
    if C_GR > 3.0 and C_GR < 5.0:
        newSQ.append(GREEN)
    else:
        newSQ.append(WHITE)
    sqs.append(newSQ)
    return False
def moveSquare( Q_SQ , SQUARES , NP ):
    i = 0
    D_SQ = False
    while i < Q_SQ:
        SQ = pygame.Rect(SQUARES[i][0], SQUARES[i][1], OBJ_SIZE[0], OBJ_SIZE[1])
        pygame.draw.rect(DISPLAYSURF, SQUARES[i][4], SQ)
        if SQUARES[i][1]+OBJ_SIZE[1] > GAMEHEIGHT_END-OBJ_SIZE[1]:
            del SQUARES[i]
            Q_SQ -= 1
            D_SQ = True
        else:
            SQUARES[i][1] += OBJ_SPEED/FPS
            SQUARES[i][0] = SQUARES[i][1]/SQUARES[i][2] + SQUARES[i][3]
        colisionOP(NP, SQUARES[i])
        if SQUARES[i][4] == GREEN and NP[5]:
            # NP[6] = score( NP[6] )
            del SQUARES[i]
            Q_SQ -= 1
            D_SQ = True
            NP[5] = False
        elif SQUARES[i][4] == WHITE and NP[5]:
            # gameover()
            NP[5] = False
            NP[6] = True
        i += 1
    return D_SQ
def space_move( ):
    SP_R = pygame.Rect((GAMEWIDTH-SP_X)/2, GAMEHEIGHT_END - (GAMEHEIGHT_END-GAMEWIDTH), SP_X, OBJ_SIZE[1])
    pygame.draw.rect(DISPLAYSURF, DARK_BLACK, SP_R)
    SP_C = ((GAMEWIDTH-SP_X)//2, GAMEHEIGHT_END - (GAMEHEIGHT_END-GAMEWIDTH) + OBJ_SIZE[1]//2)
    pygame.draw.circle(DISPLAYSURF, DARK_BLACK , SP_C  , int(OBJ_SIZE[0]/2))
    SP_C = ((GAMEWIDTH+SP_X)//2, GAMEHEIGHT_END - (GAMEHEIGHT_END-GAMEWIDTH) + OBJ_SIZE[1]//2)
    pygame.draw.circle(DISPLAYSURF, DARK_BLACK , SP_C  , int(OBJ_SIZE[0]/2))
    return False
def newPlayer( ):
    NP = []
    NP.append(GAMEWIDTH//2)
    NP.append(GAMEHEIGHT_END - (GAMEHEIGHT_END-GAMEWIDTH) + OBJ_SIZE[1]//2)
    NP.append(int(OBJ_SIZE[0]/2))
    NP.append(GREEN)                # Color
    NP.append(0)                    # Direction (LEFT , RIGHT)
    NP.append(False)                # Colitions
    NP.append(False)                # Gameover
    NP.append(0)                    # Score
    return NP
def drawPlayer( NP ):
    pygame.draw.circle(DISPLAYSURF, NP[3] , (NP[0], NP[1])  , NP[2] )
    return False
def movePlayer( NP ):
    if NP[4] == LEFT and NP[0] >= (GAMEWIDTH - SP_X)/2 :
        NP[0] -= int(OBJ_SPEED/FPS)*2
    elif NP[4] == RIGHT and NP[0] <= (GAMEWIDTH + SP_X)/2:
        NP[0] += int(OBJ_SPEED/FPS)*2
    return False
def colisionOP( NP , SQ ):
    if not(NP[5]):
        if SQ[1] <= NP[1]+(OBJ_SIZE[1]/2) and SQ[1] >= NP[1]-(OBJ_SIZE[1]/2): # COL on Y axis
            if NP[0] > SQ[0] and NP[0] < SQ[0] + OBJ_SIZE[0]:       # COL on X axis
                NP[5] = True
    return

def score( SC ):
    SC += 1
    PSC = str(SC)
    SCORE_FONT = SC_FONT.render(PSC, True , WHITE)
    SCORE = SCORE_FONT.get_rect()
    SCORE.topleft = (SCOREWIDTH/2 , SCOREHEIGHT_END/2)
    DISPLAYSURF.blit(SCORE_FONT , SCORE)
    return SC
# Main code

if __name__ == '__main__':
    main()
