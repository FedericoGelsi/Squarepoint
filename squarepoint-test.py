# Just a simple game made with pygame

# Imports

import sys, pygame, random

#Funtions

def menu():                             #Main menu

    return False

def create_sq( SIZE , sq_pos):  #Creates a new square
    x = random.randint(0, SIZE[0])  #Sets position on map (SIZE[0] = WIDTH)
    y = random.randint(0, SIZE[1])  #Sets position on map (SIZE[0] = HEIGHT)
    sq_pos.append([ x , y , True , True])    # sq = [ x , y , FP]
    return False

def move_sq(sq , SIZE , SQUARE_T):                          #Moves the square on the map
    qr = random.uniform(2.0,7.0)
    check_sq(sq , SIZE , SQUARE_T)
    if sq[2]:
        sq[0] += qr
    else:
        sq[0] -= qr
    if sq[3]:
        sq[1] += qr
    else:
        sq[1] -= qr
    return False

def check_sq(sq , SIZE , SQUARE_T):                          #Checks if the square is on the map
    if sq[0] >= SIZE[0]-SQUARE_T[0]:
        sq[2] = False
    elif sq[0] <= 0:
        sq[2] = True
    if sq[1] >= SIZE[1]-SQUARE_T[1]:
        sq[3] = False
    elif sq[1] <= 0:
        sq[3] = True
    return False

def show_score():                       #Shows the score

    return False

def


# Main code


    #CONSTANTS
SIZE = WIDTH , HEIGHT = 360 , 640
SCREEN = pygame.display.set_mode(SIZE, 0 , 32)
SQUARE_T = SQUARE_W, SQUARE_H = 25 , 25
    #COLORS        R   G    B
DISPLAY_C   =   ( 27 , 27 , 27  )            #Black
SQUARE_C_1  =   ( 95 , 208, 159 )            #Green
SQUARE_C_2  =   ( 255, 255, 255 )            #White

    #SETUP
FPS = 60                                #Frames per second setting
fpsClock = pygame.time.Clock()
pygame.init()                           #Game start

q_sq = 0
sq_pos = []
while True:
    SCREEN.fill(DISPLAY_C)                  #Set the color of the display
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    if q_sq < 10:
        create_sq( SIZE , sq_pos)
        q_sq += 1
    for i in range(len(sq_pos)):
        move_sq(sq_pos[i] , SIZE , SQUARE_T)
        square = (sq_pos[i][0], sq_pos[i][1], SQUARE_W , SQUARE_H)
        draw_sq = pygame.draw.rect(SCREEN,SQUARE_C_1,square)
    pygame.display.update()
    fpsClock.tick(FPS)
