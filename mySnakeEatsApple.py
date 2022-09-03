from distutils.command.build_scripts import first_line_re
import pygame, random
pygame.init()
screenwidth, screenheight = 600, 400
win = pygame.display.set_mode((screenwidth, screenheight)) #create game window
pygame.display.set_caption("Snake Game")

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,128,0)
BLUE = (0,0,255)
PURPLE = (112, 51, 173)

clock = pygame.time.Clock() #controls game pulse

class Snake(object):
    def __init__(self):
        self.head =[0,0] #coordinates of start of snake
        self.coords = [self.head] #list of all coordinates of snake body
        self.width = 10
        self.height = 10
        self.velocity = 10
        self.direction = ""


    def draw(self):
        for x in self.coords:
            pygame.draw.rect(win, BLUE, [x[0], x[1], self.width, self.height])


    def move(self, x_change, y_change, snakeLarger):
        # "head" is stored at end of list
        # every time this function runs - create new head, delete tail if snake length didn't change
        if (x_change == 0) and (y_change == 0): #prevent unnecessary runs 
            return

        #create new coordinates for head of snake
        new_x = self.head[0] + x_change
        new_y = self.head[1] + y_change

        #if snake head crosses border, goes through to opposite side
        if new_x < 0:
            new_x = screenwidth - self.width
        if new_y < 0:
            new_y = screenheight - self.height
        if new_x + self.width > screenwidth:
            new_x = 0
        if new_y + self.height > screenheight:
            new_y = 0

        self.coords.append([new_x, new_y])
        if not snakeLarger: #if don't need to increase snake length
            del self.coords[0] #delete tail
        player.head = self.coords[-1] #change snake head!
        
    def isClash(self): 
        #returns True if finds that snake head has hit another part of it's body
        if len(self.coords) <= 1:
            return False
        
        head_center = ((self.head[0] + (self.head[0] + self.width)) /2, (self.head[1] + (self.head[1] + self.height)) / 2)
        for coord in self.coords[:-1] : #compare headcenter to all other cord centers
            coord_center = ((coord[0] + coord[0] + self.width) /2, (coord[1] + coord[1] + self.height) / 2)
            if coord_center == head_center:
                return True
        return False
        

class Apple(object):
    def __init__(self):
        self.width = 10
        self.height = 10
        self.coord = (0,0)
        self.prev_coords = []
        self.center = (0,0)
        self.generateCoord() #when apple is initialised automatically generates random coordinate location

    def draw(self):
        pygame.draw.rect(win, GREEN, [self.coord[0], self.coord[1], self.width, self.height])


    def generateCoord(self):
        #generates new random coordinate and saves new center
        f = True
        while f:
            x = random.randrange(0, screenwidth, self.width) #random x coordinate from range 0 - screenwidth, only on iterations of self.width
            y = random.randrange(0, screenheight, self.height)

            duplicate = ()
            for coord in self.prev_coords: #loop through previous coords
                if coord == (x,y): #if new coordinate existed previously - continue running loop
                    duplicate = coord
            if duplicate == (): #new coordinate didn't exist previously - loop breaks
                f = False

        self.coord = (x,y)
        self.prev_coords.append(self.coord)

        xcenter = (x + x+self.width) / 2
        ycenter = (y + y+self.height) / 2
        self.center = (xcenter, ycenter)


def redrawGameWindow(): #draw function that needs to be run at every loop
    win.fill(BLACK) #filling black color so we don't draw over previous rectangle
    player.draw()
    apple.draw()
    pygame.display.update()


def redrawMainWindow():
    #introductory window that leads to game
    text_height = 25
    first_line_height = (screenheight // 2) - 15

    win.fill(PURPLE)
    font = pygame.font.Font('freesansbold.ttf', text_height)
    gameName = font.render("SNAKE EATS APPLE", True, BLACK, WHITE)
    text2 = font.render("Press SPACE to start", True, BLACK, PURPLE)
    text3 = font.render("EXIT using top right X button", True, BLACK, PURPLE)
    gameNameRect, textRect2, textRect3 = gameName.get_rect(), text2.get_rect(), text3.get_rect()
    gameNameRect.center = (screenwidth // 2, first_line_height)
    textRect2.center = (screenwidth // 2, first_line_height + 25)
    textRect3.center = (screenwidth // 2, first_line_height + 50)
    win.blit(gameName, gameNameRect)
    win.blit(text2, textRect2)
    win.blit(text3, textRect3)
    pygame.display.update()

player = Snake()

#loop of main game
def PlayGame():
    snake_longer = False #keeps track of when snake needs to get larger (longer)
    run = True
    x_change, y_change = 0, 0 #store coordinate changes

    while run:
        clock.tick(27)
        if player.isClash() == True: #found that head clashes with its own body part
           run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if user presses exit button on top right of window
                run = False #closes window properly - doesn't cause error if user exited

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and player.direction != "left":
            x_change = player.velocity
            y_change = 0
            player.direction = "right"
        elif keys[pygame.K_LEFT] and player.direction != "right":
            x_change = -player.velocity
            y_change = 0
            player.direction = "left"
        elif keys[pygame.K_UP] and player.direction != "down":
            x_change = 0
            y_change = -player.velocity
            player.direction = "up"
        elif keys[pygame.K_DOWN] and player.direction != "up":
            x_change = 0
            y_change = player.velocity
            player.direction = "down"


        head_center = ((player.head[0] + player.head[0] + player.width) /2, (player.head[1] + player.head[1] + player.height) /2 )
        if head_center == apple.center: #center point of snake head is equal to center point of apple
            snake_longer = True
            apple.generateCoord()

        player.move(x_change, y_change, snake_longer) #always implements change to snakes coordinates. if no change occured keeps snake moving according to last instruction
        snake_longer = False

        redrawGameWindow()

Main = True
while Main: #runs main page until receives instruction to run game
    redrawMainWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Main = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player = Snake()
        apple = Apple()
        PlayGame() #runs game until game ends naturally, then goes back to loop
