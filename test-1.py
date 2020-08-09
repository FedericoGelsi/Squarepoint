# Imports
import sys, pygame , random

# Funtions

def object_move( sq ):
    if sq[2]:
        sq[0] += random.random()
    else:
        sq[0] -= random.random()
    if sq[3]:
        sq[1] += random.random()
    else:
        sq[1] -= random.random()
    return False

def check_position( sq , w , h , sq_tam):
    if sq[0] >= w-sq_tam[0]:
        sq[2] = False
    elif sq[0] <= 0:
        sq[2] = True
    if sq[1] >= h-sq_tam[1]:
        sq[3] = False
    elif sq[1] <= 0:
        sq[3] = True
    return False

def make_sq( width , height ):
    q_sq = []
    rsq = 0
    while rsq != 25:
        rsq = random.randint(1,100)
    if len(q_sq)<=10:
        x = random.randint(0, width)
        y = random.randint(0, height)
        q_sq.append([ x , y , True , True])     # sq = [ x , y , fx , fy ]
    return q_sq

def draw_sq ( sq , sq_tam, screen):
        #Square
    c_sq = (95, 208, 159)
    square = (sq[0], sq[1], sq_tam[0], sq_tam[1])
    draw_sq = pygame.draw.rect(screen,c_sq,square)
    return False
def play_sq ( width , height , screen ):
    sq_tam = [25, 25]
    q_sq = make_sq(width , height)
    for i in range(len(q_sq)):
        object_move( q_sq[i] )
        check_position( q_sq[i] , width , height , sq_tam)
        draw_sq( q_sq[i] , sq_tam, screen)
    return False
pygame.init()
    #Screen
size = width, height = 360,640
screen = pygame.display.set_mode(size,0,32)
black = (27, 27, 27)

screen.fill(black)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    # rect = (sq[0], sq[1] , sq_tam[0], sq_tam[1] )
    play_sq( width , height , screen)
    # draw_sq = pygame.draw.rect(screen,c_sq,rect)
    pygame.display.flip()
