import pygame
import math
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
import time
import csv
import numpy as np
import sys
import random
from pygame.locals import *
start_time=0
class Button: #create new buttons
    def __init__(self, rect, command):
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.fill((0,0,0))
        self.function = command
 
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
 
    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.function()
 
    def draw(self, surf,x,y): #draws button in center of screen
        self.rect.topleft=(x,y)
        surf.blit(self.image, self.rect)  

    #function for local multiplayer button
def local(): #starts a new game
    global start_time
    start_time = time.time()
    game = Game()  # start a game

    #function for online multiplayer button
def online():
    bg=BoxesGame() #__init__ is called right here
    while 1:
        if bg.update()==1:
            break
    bg.finished()

    #function to show leaderboards
def leaderboard_prt():
    with open ("protleader.csv", "r") as file:
        sortlist=[]
        reader=csv.reader(file)
        for i in reader:
            ix=i[0]
            iy=i[1]
            it=[int(ix),iy]
            sortlist.append(it)
    sortlist.sort() #sort list by inner list
    sortlist.reverse() #descending order
    if(len(sortlist)>5):
        printer=5
    else:
        printer=(len(sortlist))
    for i in range(printer):
        print(sortlist[i])
    screen = pygame.display.set_mode([304,304])
    pygame.init()
    pygame.display.set_caption("Leaderboard")
    font=pygame.font.Font('Arial.ttf',12)
    screen.blit(font.render('Top Scores', True, (255,255,255)), (102, 102))
    y=122
    for i in range(printer):
         screen.blit(font.render(str(sortlist[i][1])+"   "+str(sortlist[i][0]), True, (255,255,255)), (108, y))
         y+=20
    btn = Button(rect=(50,50,105,25), command=menu)
    btn.draw(screen,102,250)
    screen.blit(font.render('Back to Menu', True, (255,255,255)), (102, 250))
    pygame.display.update()

    while(True):
        for event in pygame.event.get():
            btn.get_event(event)
        
    
        #function to launch main menu
def menu():
    screen = pygame.display.set_mode([304,304])
    pygame.init()
    pygame.display.set_caption("Squares")
    btn = Button(rect=(50,50,105,25), command=local)
    x=102
    y=102
    btn.draw(screen,x,y)
    font=pygame.font.Font('Arial.ttf',12)
    screen.blit(font.render('Local Multiplayer', True, (255,255,255)), (x, y))
    btn2 = Button(rect=(50,50,105,25), command=online)
    y=152
    btn2.draw(screen,x,y)
    font=pygame.font.Font('Arial.ttf',12)
    screen.blit(font.render('Online Multiplayer', True, (255,255,255)), (x, y))
    btnldr = Button(rect=(50,50,105,25), command=leaderboard_prt)
    y=202
    btnldr.draw(screen,x,y)
    font=pygame.font.Font('Arial.ttf',12)
    screen.blit(font.render('  Leaderboards', True, (255,255,255)), (x, y))
    pygame.display.update()
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            btn.get_event(event)
            btn2.get_event(event)
            btnldr.get_event(event)
class Game:
    def __init__(self):
        global start_time
        winner=False
        self.grid_size = 10  # default
        if len(sys.argv) > 1:
            self.grid_size = int(sys.argv[1])
        self.clock=pygame.time.Clock()

        # It turns out that there are nice structures when setting ~0.75 walls per slot
        self.start_walls = int(0.75 * self.grid_size ** 2)

        self.accept_clicks = True

        # variables for the boxes for each player (x would be computer)
        self.a_boxes = 0
        self.b_boxes = 0
        self.x_boxes = 0

        self.turn = "X"
        self.caption = "'s turn    "

        # 0 empty 1 is A 2 is B and 3 is X
        self.grid_status = np.zeros((self.grid_size, self.grid_size), np.int)
        self.upper_walls_set_flags = np.zeros((self.grid_size, self.grid_size), np.dtype(bool))
        self.left_walls_set_flags = np.zeros((self.grid_size, self.grid_size), np.dtype(bool))

        # set the outer walls
        for column in range(self.grid_size):
            for row in range(self.grid_size):
                if column == 0:
                    self.left_walls_set_flags[column][row] = True
                if row == 0:
                    self.upper_walls_set_flags[column][row] = True

        # initialize pygame
        pygame.init()

        # set the display size (one slot has 30x30 pixels; Walls: 4x26 Box: 26x26)
        self.screen = pygame.display.set_mode([30 * self.grid_size + 4, 30 * self.grid_size + 4])
        # load all images
        self.empty = pygame.image.load("pics/empty.png")
        self.A = pygame.image.load("pics/A.png")
        self.B = pygame.image.load("pics/B.png")
        self.X = pygame.image.load("pics/X.png")
        self.block = pygame.image.load("pics/block.png")
        self.lineX = pygame.image.load("pics/lineX.png")
        self.lineXempty = pygame.image.load("pics/lineXempty.png")
        self.lineY = pygame.image.load("pics/lineY.png")
        self.lineYempty = pygame.image.load("pics/lineYempty.png")
        self.lineXred=pygame.image.load("pics/lineX red.png")
        self.lineXblue=pygame.image.load("pics/lineX blue.png")
        self.lineYred = pygame.image.load("pics/lineY red.png")
        self.lineYblue= pygame.image.load("pics/lineY blue.png")
        tries = 0
        # set the start walls randomly but do not create any opportunity to directly close boxes
        while self.start_walls > 0 and tries < 4*self.grid_size**2:
            x = np.random.randint(self.grid_size)
            y = np.random.randint(self.grid_size)
            up = np.random.randint(2)

            if up:
                if not self.upper_walls_set_flags[x][y] \
                        and self.get_number_of_walls(x, y) < 2 \
                        and self.get_number_of_walls(x, y - 1) < 2:
                    self.upper_walls_set_flags[x][y] = True
                    self.start_walls -= 1
            else:
                if not self.left_walls_set_flags[x][y] \
                        and self.get_number_of_walls(x, y) < 2 \
                        and self.get_number_of_walls(x - 1, y) < 2:
                    self.left_walls_set_flags[x][y] = True
                    self.start_walls -= 1

            tries += 1

        # now it's the first players turn
        self.turn = "A"
        self.show()
        stop=0
        while (True):
            self.clock.tick(60)
            if(winner==False):
                pygame.display.set_caption(self.turn + self.caption + "     A:" + str(
                            self.a_boxes) + "   B:"+ str(self.b_boxes))
            else:
                if(stop==0): #after winner is declared draw button
                    btn = Button(rect=(50,50,105,25), command=local)
                    btn.draw(self.screen,100,100)
                    font=pygame.font.Font('Arial.ttf',12)
                    self.screen.blit(font.render('New Game', True, (255,255,255)), (100, 100))
                    btn3 = Button(rect=(50,50,105,25), command=menu)
                    btn3.draw(self.screen,100,150)
                    font=pygame.font.Font('Arial.ttf',12)
                    self.screen.blit(font.render('Menu', True, (255,255,255)), (100, 150))
                    ldrbtn = Button(rect=(50,50,105,25), command=leaderboard_prt)
                    ldrbtn.draw(self.screen,100,200)
                    font=pygame.font.Font('Arial.ttf',12)
                    self.screen.blit(font.render('Leaderboard', True, (255,255,255)), (100, 200))
                    pygame.display.update()
                    if(self.a_boxes>self.b_boxes):
                        username="A"
                        score=self.a_boxes
                    else:
                        username="B"
                        score=self.b_boxes
                    with open ("protleader.csv", "a", newline='') as file:
                        fields=['score', 'name']
                        writer=csv.DictWriter(file, fieldnames=fields)
                        writer.writerow({'score' : int(score), 'name' : username})

                    with open ("protleader.csv", "r") as file:
                        sortlist=[]
                        reader=csv.reader(file)
                        for i in reader:
                            sortlist.append(i)
                    for i in range(len(sortlist)):
                        if i != 0:
                            sortlist[i][0]=int(sortlist[i][int(0)])
                    stop=1
            # go through all events and check the types
            for event in pygame.event.get():
                if(stop==1):
                    btn.get_event(event)
                    btn3.get_event(event)
                    ldrbtn.get_event(event)
                # quit the game when the player closes it
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                # left click
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    if not self.accept_clicks:
                        continue

                    # get the current position of the cursor
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]

                    # check whether it was a not set wall that was clicked
                    wall_x, wall_y = self.get_wall(x, y)

                    if not (wall_x >= 0 and wall_y >= 0):
                        continue

                    upper_wall = wall_y % 30 == 0

                    if upper_wall:
                        if not self.upper_walls_set_flags[wall_x//30][wall_y//30]:
                            self.upper_walls_set_flags[wall_x//30][wall_y//30] = True
                            if self.turn=="A":
                                self.screen.blit(self.lineXred, (wall_x, wall_y))
                            else:
                                self.screen.blit(self.lineXblue, (wall_x, wall_y))
                        else:
                            continue
                    else:
                        if not self.left_walls_set_flags[wall_x//30][wall_y//30]:
                            self.left_walls_set_flags[wall_x//30][wall_y//30] = True
                            if self.turn=="A":
                                self.screen.blit(self.lineYred, (wall_x, wall_y))
                            else:
                                self.screen.blit(self.lineYblue, (wall_x, wall_y))
                        else:
                            continue

                    if not self.set_all_slots() > 0:
                        if self.turn == "A":
                            self.turn = "B"
                        elif self.turn == "B":
                            self.turn = "A"

                    if (self.won() or winner==True):
                        winner=True

                    else:
                        pygame.display.flip()
                        
    def get_number_of_walls(self, slot_column, slot_row):
        """
        Get the number of set walls around the passed slot
        :param slot_column: x of the slot
        :param slot_row: y of the slot
        :return: number of set walls
        """
        number_of_walls = 0

        if slot_column == self.grid_size - 1:
            number_of_walls += 1
        elif self.left_walls_set_flags[slot_column + 1][slot_row]:
            number_of_walls += 1

        if slot_row == self.grid_size - 1:
            number_of_walls += 1
        elif self.upper_walls_set_flags[slot_column][slot_row + 1]:
            number_of_walls += 1

        if self.left_walls_set_flags[slot_column][slot_row]:
            number_of_walls += 1

        if self.upper_walls_set_flags[slot_column][slot_row]:
            number_of_walls += 1

        return number_of_walls

    @staticmethod
    def get_wall(pos_x, pos_y):
        rest_x = pos_x % 30
        rest_y = pos_y % 30

        wall_slot_x = pos_x//30
        wall_slot_y = pos_y//30

        # in a corner
        if rest_x < 4 and rest_y < 4:
            return -1, -1

        if rest_x < 4:
            # is left wall of the slot
            return wall_slot_x*30, wall_slot_y*30 + 4

        if rest_y < 4:
            # is upper wall of the slot
            return wall_slot_x*30 + 4, wall_slot_y*30

        # inside the box => not a wall
        return -1, -1

    def set_all_slots(self):
        """
        Find all newly closed boxes and close them for the current player
        :return: number of closed boxes
        """
        to_return = 0

        for column_ in range(self.grid_size):
            for row_ in range(self.grid_size):
                if self.grid_status[column_][row_] != 0 or self.get_number_of_walls(column_, row_) < 4:
                    continue

                if self.turn == "A":
                    self.grid_status[column_][row_] = 1
                    self.screen.blit(self.A, (column_ * 30 + 4, row_ * 30 + 4))
                    self.a_boxes += 1
                elif self.turn == "B":
                    self.grid_status[column_][row_] = 2
                    self.screen.blit(self.B, (column_ * 30 + 4, row_ * 30 + 4))
                    self.b_boxes += 1
                elif self.turn == "X":
                    self.grid_status[column_][row_] = 3
                    self.screen.blit(self.X, (column_ * 30 + 4, row_ * 30 + 4))
                    self.x_boxes += 1

                to_return += 1

        return to_return

    def won(self):
        """
        Check whether the game was finished
        If so change the caption to display the winner
        :return: won or not
        """
        global start_time
        finaltime=round(time.time() - start_time,2)
        if self.a_boxes + self.b_boxes + self.x_boxes == self.grid_size ** 2:
            if self.a_boxes < self.b_boxes:
                won_caption = "Player B won in : "+str(finaltime)
            elif self.b_boxes < self.a_boxes:
                won_caption = "Player A won in : "+str(finaltime)
            else:
                won_caption = "It's a tie after : "+str(finaltime)+" seconds"

            # set the display caption
            pygame.display.set_caption(won_caption)

            # update the players screen
            pygame.display.flip()

            return True
        else:
            return False

    

    def show(self):
        global start_time
        """
        Reload the screen
        Use the current grid and wall information to
        update the players screen
        """
        self.screen.fill(0)

        # loop over all slots
        for column in range(self.grid_size):
            for row in range(self.grid_size):
                x, y = column * 30, row * 30
                self.screen.blit(self.block, (x, y))
                x += 4
                if not self.upper_walls_set_flags[column][row]:
                    self.screen.blit(self.lineXempty, (x, y))
                else:
                    randx=random.randint(0,1)
                    if(randx==0):
                        self.screen.blit(self.lineXred, (x, y))
                    else:
                        self.screen.blit(self.lineXblue, (x, y))
                x -= 4
                y += 4
                if not self.left_walls_set_flags[column][row]:
                    self.screen.blit(self.lineYempty, (x, y))
                else:
                    randx=random.randint(0,1)
                    if(randx==0):
                        self.screen.blit(self.lineYred, (x, y))
                    else:
                        self.screen.blit(self.lineYblue, (x, y))

                # calculate x and y in pixels
                x, y = column * 30 + 4, row * 30 + 4

                if self.grid_status[column][row] == 0:
                    self.screen.blit(self.empty, (x, y))
                elif self.grid_status[column][row] == 1:
                    self.screen.blit(self.A, (x, y))
                elif self.grid_status[column][row] == 2:
                    self.screen.blit(self.B, (x, y))
                elif self.grid_status[column][row] == 3:
                    self.screen.blit(self.X, (x, y))

        pygame.display.set_caption(self.turn + self.caption + "     A:" + str(
                            self.a_boxes) + "   B:"+ str(self.b_boxes))
        pygame.display.flip()


class BoxesGame(ConnectionListener):
    def initSound(self):
        pygame.mixer.music.load("music.wav")
        self.winSound = pygame.mixer.Sound('win.wav')
        self.loseSound = pygame.mixer.Sound('lose.wav')
        self.placeSound = pygame.mixer.Sound('place.wav')
        pygame.mixer.music.play()
    def Network_close(self, data):
        exit()
    def Network_yourturn(self, data):
        #torf = short for true or false
        self.turn = data["torf"]
    def Network_startgame(self, data):
        self.running=True
        self.num=data["player"]
        self.gameid=data["gameid"]
    def Network_place(self, data):
        self.placeSound.play()
        #get attributes
        x = data["x"]
        y = data["y"]
        hv = data["is_horizontal"]
        #horizontal or vertical
        if hv:
            self.boardh[y][x]=True
        else:
            self.boardv[y][x]=True
    
    def __init__(self):
        self.justplaced=10
        self.boardh = [[False for x in range(6)] for y in range(7)]
        self.boardv = [[False for x in range(7)] for y in range(6)]
        #1
        pygame.init()
        pygame.font.init()
        width, height = 389, 489
        #2
        #initialize the screen
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Boxes")
        #3
        #initialize pygame clock
        self.clock=pygame.time.Clock()
        #initialize the graphics
        self.initGraphics()
        self.initSound()
        self.turn = True
        self.owner=[[0 for x in range(6)] for y in range(6)]
        self.me=0
        self.otherplayer=0
        self.didiwin=False
        self.running=False
        address=input("Address of Server: ")
        try:
            if not address:
                host, port="localhost", 8000
            else:
                host,port=address.split(":")
            self.Connect((host, int(port)))
        except:
            print ("Error Connecting to Server")
            print ("Usage:", "host:port")
            print ("e.g.", "localhost:31425")
            exit()
        print ("Boxes client started")
        self.running=False
        self.owner=[[0 for x in range(6)] for y in range(6)]
        while not self.running:
            self.Pump()
            connection.Pump()
            sleep(0.01)
        #determine attributes from player #
        if self.num==0:
            self.turn=True
            self.marker = self.greenplayer
            self.othermarker = self.blueplayer
        else:
            self.turn=False
            self.marker=self.blueplayer
            self.othermarker = self.greenplayer
    def drawBoard(self):
        # This draws all of the lines other than the edges.
        for x in range(6):
            for y in range(6):
                if not self.boardh[y][x]:
                    self.screen.blit(self.normallineh, [(x)*64+5, (y)*64])
                else:
                    self.screen.blit(self.bar_doneh, [(x)*64+5, (y)*64])
                if not self.boardv[y][x]:
                    self.screen.blit(self.normallinev, [(x)*64, (y)*64+5])
                else:
                    self.screen.blit(self.bar_donev, [(x)*64, (y)*64+5])
        for edge in range(6):
            if not self.boardh[6][edge]:
                self.screen.blit(self.normallineh, [edge*64+5, 6*64])
            else:
                self.screen.blit(self.bar_doneh, [edge*64+5, 6*64])
            if not self.boardv[edge][6]:
                self.screen.blit(self.normallinev, [6*64, edge*64+5])
            else:
                self.screen.blit(self.bar_donev, [6*64, edge*64+5])
        #draw separators
        for x in range(7):
            for y in range(7):
                self.screen.blit(self.separators, [x*64, y*64])
    def drawHUD(self):
        #draw the background for the bottom:
        self.screen.blit(self.score_panel, [0, 389])
        #create font
        myfont = pygame.font.SysFont(None, 32)
         
        #create text surface
        label = myfont.render("Your Turn:", 1, (255,255,255))
         
        #draw surface
        self.screen.blit(label, (10, 400))
        self.screen.blit(self.greenindicator if self.turn else self.redindicator, (130, 395))
        #same thing here
        myfont64 = pygame.font.SysFont(None, 64)
        myfont20 = pygame.font.SysFont(None, 20)

        scoreme = myfont64.render(str(self.me), 1, (255,255,255))
        scoreother = myfont64.render(str(self.otherplayer), 1, (255,255,255))
        scoretextme = myfont20.render("You", 1, (255,255,255))
        scoretextother = myfont20.render("Other Player", 1, (255,255,255))

        self.screen.blit(scoretextme, (10, 425))
        self.screen.blit(scoreme, (10, 435))
        self.screen.blit(scoretextother, (280, 425))
        self.screen.blit(scoreother, (340, 435))

    def update(self):
        if self.me+self.otherplayer==36:
            self.didiwin=True if self.me>self.otherplayer else False
            return 1
        #sleep to make the game 60 fps
        self.justplaced-=1
        self.clock.tick(60)
        connection.Pump()
        self.Pump()
        #clear the screen
        self.screen.fill(0)
        self.drawBoard()
        self.drawHUD()
        self.drawOwnermap()

        for event in pygame.event.get():
            #quit if the quit button was pressed
            if event.type == pygame.QUIT:
                exit()
     
        #update the screen
        #1
        mouse = pygame.mouse.get_pos()
         
        #2
        xpos = int(math.ceil((mouse[0]-32)/64.0))
        ypos = int(math.ceil((mouse[1]-32)/64.0))
         
        #3
        is_horizontal = abs(mouse[1] - ypos*64) < abs(mouse[0] - xpos*64)
         
        #4
        ypos = ypos - 1 if mouse[1] - ypos*64 < 0 and not is_horizontal else ypos
        xpos = xpos - 1 if mouse[0] - xpos*64 < 0 and is_horizontal else xpos
         
        #5
        board=self.boardh if is_horizontal else self.boardv 
        isoutofbounds=False
         
        #6
        try: 
            if not board[ypos][xpos]: self.screen.blit(self.hoverlineh if is_horizontal else self.hoverlinev, [xpos*64+5 if is_horizontal else xpos*64, ypos*64 if is_horizontal else ypos*64+5])
        except:
            isoutofbounds=True
            pass
        if not isoutofbounds:
            alreadyplaced=board[ypos][xpos]
        else:
            alreadyplaced=False
        if pygame.mouse.get_pressed()[0] and not alreadyplaced and not isoutofbounds and self.turn and self.justplaced<=0:
            self.justplaced=10
            if is_horizontal:
                self.boardh[ypos][xpos]=True
                self.Send({"action": "place", "x":xpos, "y":ypos, "is_horizontal": is_horizontal, "num": self.num, "gameid": self.gameid})
            else:
                self.boardv[ypos][xpos]=True
                self.Send({"action": "place", "x":xpos, "y":ypos, "is_horizontal": is_horizontal, "num": self.num, "gameid": self.gameid})
        pygame.display.flip()
    def Network_win(self, data):
        self.owner[data["x"]][data["y"]]="win"
        self.boardh[data["y"]][data["x"]]=True
        self.boardv[data["y"]][data["x"]]=True
        self.boardh[data["y"]+1][data["x"]]=True
        self.boardv[data["y"]][data["x"]+1]=True
        #add one point to my score
        self.winSound.play()
        self.me+=1
    def Network_lose(self, data):
        self.owner[data["x"]][data["y"]]="lose"
        self.boardh[data["y"]][data["x"]]=True
        self.boardv[data["y"]][data["x"]]=True
        self.boardh[data["y"]+1][data["x"]]=True
        self.boardv[data["y"]][data["x"]+1]=True
        #add one to other players score
        self.loseSound.play()
        self.otherplayer+=1
    def initGraphics(self):
        self.normallinev=pygame.image.load("normalline.png")
        self.normallineh=pygame.transform.rotate(pygame.image.load("normalline.png"), -90)
        self.bar_donev=pygame.image.load("bar_done.png")
        self.bar_doneh=pygame.transform.rotate(pygame.image.load("bar_done.png"), -90)
        self.hoverlinev=pygame.image.load("hoverline.png")
        self.hoverlineh=pygame.transform.rotate(pygame.image.load("hoverline.png"), -90)
        self.separators=pygame.image.load("separators.png")
        self.redindicator=pygame.image.load("redindicator.png")
        self.greenindicator=pygame.image.load("greenindicator.png")
        self.greenplayer=pygame.image.load("greenplayer.png")
        self.blueplayer=pygame.image.load("blueplayer.png")
        self.winningscreen=pygame.image.load("youwin.png")
        self.gameover=pygame.image.load("gameover.png")
        self.score_panel=pygame.image.load("score_panel.png")
    def drawOwnermap(self):
        for x in range(6):
            for y in range(6):
                if self.owner[x][y]!=0:
                    if self.owner[x][y]=="win":
                        self.screen.blit(self.marker, (x*64+5, y*64+5))
                    if self.owner[x][y]=="lose":
                        self.screen.blit(self.othermarker, (x*64+5, y*64+5))
    def finished(self):
        if(self.didiwin):
            username="Me"
            with open ("protleader.csv", "a", newline='') as file:
                fields=['score', 'name']
                writer=csv.DictWriter(file, fieldnames=fields)
                writer.writerow({'score' : int(self.me), 'name' : username})
        self.screen.blit(self.gameover if not self.didiwin else self.winningscreen, (0,0))
        font=pygame.font.Font('Arial.ttf',12)
        btn = Button(rect=(50,50,105,25), command=menu)
        btn.draw(self.screen,135,280)
        self.screen.blit(font.render('Back to Menu', True, (255,255,255)), (138, 282))
        pygame.display.update()
        while 1:
            for event in pygame.event.get():
                btn.get_event(event)
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()
menu()
