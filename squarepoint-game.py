# Just a simple game made with pygame

# Imports

import sys
import pygame
import random
# Funtions
"""
def main():
    global FPSCLOCK, DISPLAYSURF
    SQUARES = []
    pygame.init()
    look = 0
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
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


def colisionOP( NP , SQ ):
    if not(NP[5]):
        if SQ[1] <= NP[1]+(OBJ_SIZE[1]/2) and SQ[1] >= NP[1]-(OBJ_SIZE[1]/2): # COL on Y axis
            if NP[0] > SQ[0] and NP[0] < SQ[0] + OBJ_SIZE[0]:       # COL on X axis
                NP[5] = True
    return
"""
# Main code
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.bg_color = (0,0,0)
        self.map = pygame.display.set_mode((width, height))
        pygame.display.set_caption('SquarePoint')
        self.bar = Bar(20, 500)
        self.lose_limit = self.height-self.height//6
        self.squares = []
        self.player = None
    
    def set_bg_color(self, r, g, b):
        self.bg_color = (r,g,b)

    def create_map(self):
        self.map = pygame.display.set_mode((self.width, self.height))

    def update_canvas(self):
        self.map.fill(self.bg_color)
        self.bar.draw_bar(self.player, self.map, self.lose_limit, self.width)
        self.player.draw_player(self.map)
        """
        for square in self.squares:
            square.draw_square(self.map)
        """
        pygame.display.update()
        
class Bar:
    def __init__(self, px, py):
        self.px = px                # Horizontal position 
        self.py = py                # Vertical position
        self.color = (46, 47, 66)   # Dark Black
    
    def set_color(self, r, g, b):
        self.color = (r,g,b)        # Change the bar color

    def draw_bar(self, player, map, lose_limit, width):
        SP_R = pygame.Rect((width-self.px)/2, lose_limit - (lose_limit-width), self.px, player.radius)
        pygame.draw.rect(map, self.color, SP_R)
        SP_C = ((width-self.px)//2, lose_limit - (lose_limit-width) + player.radius//2)
        pygame.draw.circle(map, self.color , SP_C  , int(player.width/2))
        SP_C = ((width+self.px)//2, lose_limit - (lose_limit-width) + player.radius//2)
        pygame.draw.circle(map, self.color , SP_C  , int(player.radius/2))

class Player:
    def __init__(self, px, py, name="AAA"):
        self.px = px
        self.py = py
        self.speed = 5
        self.color = (95, 208, 159)
        self.name = name
        self.score = 0
        self.radius = 10
    
    def change_color(self, r, g, b):
        self.color = (r,g,b)

    def draw_player(self, window):
        pygame.draw.circle(window, self.color , (self.px, self.py)  , self.radius )

    def move_player(self, dir, bar):
        if dir == "L" and self.px <= (bar.width - self.radius)/2:
            self.px -= int(self.speed/canvas.fps)*2
        elif dir == "R" and self.px <= (canvas.width + self.radius)/2:
            self.px += int(self.speed/canvas.fps)*2

    def get_event(self, bar):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a):
                    self.move_player("L", bar)
                elif (event.key == K_RIGHT or event.key == K_d):
                    self.move_player("R", bar)
                elif event.key == K_ESCAPE:
                    pygame.quit()

    def add_point(self):
        self.score += 1

class Square:
    def __init__(self, radius, map_w, color=(255,255,255)):
        self.px = random.randint(self.radius, map_w)
        self.py = 0
        self.radius = radius
        self.color = color

def main():
    pygame.init()
    pygame.font.init()
    FPS = 60
    FPSCLOCK = pygame.time.Clock()
    game = Map(600, 800)
    game.set_bg_color(0,0,0)
    game.create_map()
    game.player = Player(200,500)
    while True:
        game.player.get_event(game.bar)
        FPSCLOCK.tick(FPS)  


if __name__ == '__main__':
    main()

