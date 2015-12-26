## Final Project --Snake Game 2.0
## Gábor Csapó
#gc1569
## Nghiem Huynh 
#nh1221

import random
import time

#p is the variable for the playing mode (single, hard, multi) it comes in play in the menu
p = 0   
#is the variable for the time for which the execution goes to sleep WHEN WE NEED IT. It is updated accordingly                                                                                             
waittime = 0                                                                                         

#code for the music
add_library('minim')                                                                                 
minim = Minim(this)
music = minim.loadFile('soundtrack.mp3')

#both the Snake and the Apple is made up of units that take 2 coordinates as attributes
class UNIT:                                                                                           
    def __init__(self, xcoordinate, ycoordinate):
        self.x = xcoordinate
        self.y = ycoordinate

# we need the difficulty as it matters because in hard mode the size is different
class APPLE:                                                                                          
    def __init__(self, difficulty, x, y):
        #self.unit stores the unit of the apple
        self.unit = UNIT(x, y)                                                                        
        self.difficulty = difficulty
    
    #if the apple is eaten it creates a new one
    def Placement(self):                                                                             
        x = random.randint(12/self.difficulty, 48/self.difficulty)*10*self.difficulty
        y = random.randint(18/self.difficulty, 52/self.difficulty)*10*self.difficulty
        self.unit = UNIT(x, y)


#instantiation of the apple for the easy and the hard mode
Appleeasy = APPLE(1, 200, 200)                                                                       
Applehard = APPLE(2, 200, 200)


class SNAKE:
    def __init__(self, difficulty, x,y, Apple):
        #the units of the snake are stored in self.units
        self.units = [UNIT(x, y)] 
        # attribute that tells which way the snake is going                                                                   
        self.moveonx = 10                                                                             
        self.moveony = 0
        self.score = 0
        #difficulty is used to determine the size of the snake  
        self.difficulty = difficulty  
        #apple that is used for the snake (depends on the difficulty)                                                             
        self.Apple = Apple 
    
    #deletes the last unit of the snake (which is the first in the list) and adds a new one according to the direction of the snake                                                                           
    def move(self):                                                                                   
        newunit = UNIT((self.units[-1].x + self.moveonx*self.difficulty), (self.units[-1].y + self.moveony*self.difficulty))
        
        #here we check whether the new apple is inside of the snake if it is we create a new one
        if self.Apple.unit.x == newunit.x and self.Apple.unit.y == newunit.y:                         
            g = 1 
            while g:
                g = 0
                self.Apple.Placement()
                for i in self.units:        
                    if i.x == self.Apple.unit.x and i.y == self.Apple.unit.y:
                        g = 1
                        continue
            self.score += 50
            newunit = UNIT((self.units[-1].x + self.moveonx*self.difficulty), (self.units[-1].y + self.moveony*self.difficulty))
            (self.units).append(newunit)
            return
        (self.units).append(newunit)
        self.units.pop(0)
    
    # if the player reaches a certain size we end the game as he won
    def winner(self):                                                                                 
        if self.units == 400* self.difficulty:
            p = 0 
    
    # we check if the player is in a position that means it should die   
    def die(self, snake):  
        #if the x coordinate is outside the play area                                                                          
        if self.units[-1].x < 100 or self.units[-1].x >= 500:                                         
            return True
        
        #if the y coordinate is outside the play area
        if self.units[-1].y < 160 or self.units[-1].y >= 560:                                         
            return True
        
        #if he has bumped into itself
        for i in self.units:                                                                         
                if self.units[-1].x == i.x and self.units[-1].y == i.y and not i == self.units[-1]:
                    return True
        
        # if it is a multiplayer. The rules are complex read more about it in the documentation.
        if p == 3:                                                                                    
            for j in snake.units: 
                if self.units[-1].x == j.x and self.units[-1].y == j.y:
                    if snake.units.index(j) == (len(snake.units)-1):
                        if len(snake.units) >= len(self.units):
                            return True
                        return False
                    return True    
        else:
            return False


#the gameplay in the multiplayer mode. Takes the two snakes and the apple as an attribute 
def multiplayer(snake1, snake2, Apple):                                                              
    q = [snake1, snake2]
    
    #unfortunately we need to declare p and waittime as global variable we found this the easiest way to do it
    global p                                                                                          
    global waittime
    
    #checks if the two players have bumped into each other with the head and with the same lenght                                     
    if Snake.die(Snake_new) and Snake_new.die(Snake):                                                 
        p = 0
        waittime = 3
        image(loadImage("Im-a-LOSER.png"), 200, 300, 200, 200)
        fill(0)
        text("Both of you lost", 200, 230)
        textSize(20) 
        text("Next time try to last longer!", 160, 260) 
        textSize(35)
        fill(255)
    
    #check if player 1 has died or not, if yes p is set to 0 so that after this the menu pops up, the waittime is set to 3 seconds and a message for the defeated person pops up
    elif Snake.die(Snake_new):                                                                                    
        p = 0
        waittime = 3
        image(loadImage("Im-a-LOSER.png"), 200, 300, 200, 200)
        fill(0)
        text("White player lost", 200, 230)
        textSize(20)
        text("Next time try to last longer!", 160, 260)
        textSize(35) 
        fill(255)
        return True
    
    # checks if the other player has died or not...
    elif Snake_new.die(Snake):                                                                        
        p = 0
        waittime = 3
        image(loadImage("Im-a-LOSER.png"), 200, 300, 250, 250)
        fill(0)
        text("Black player lost", 200, 230)
        textSize(20)
        text("Next time try to last longer!", 160, 260)
        textSize(35)
        fill(255)
        return True
    
    # if nobody died we can play!
    else: 
        #looping through the players                                                                                            
        for k in q: 
            #variable to check which players is actually playing                                                                                  
            m = q.index(k) + 1                                                                        
            fill(200, 200, 200)
            #score
            text("Player" +' ' + str(m), (200+200*q.index(k) - 60), 100 )             
            text(str(k.score), (200+200*q.index(k)), 130)
            #setting colours for the players and the apple
            fill(80,80,80)
            stroke(80, 80, 80)
            
            if m != 2:                                                                               
                fill(255, 255, 255)
                stroke(255, 255, 255)
            
            #displaying the units of one player
            for i in k.units:                                                                         
                rect(i.x, i.y, 10*k.difficulty, 10*k.difficulty)
            
            stroke(122, 10, 15)
            fill(122, 10, 15)
            
            #displaying the apple
            rect(Apple.unit.x, Apple.unit.y, 10*k.difficulty, 10*k.difficulty) 
            
            #moving the snake                       
            k.move()                                                                                  
            
            k.winner()
        return False


#singleplayer mode take one snake (hard, easy) and the apple accordingly. it is baasically the simplified version of the multiplayer
def singleplayer(snake, Apple):                                                                       
    global p                                                                                          
    global waittime
    
    if snake.die(Snake_new):
        image(loadImage("Im-a-LOSER.png"), 150, 200, 300, 300)
        p = 0
        waittime = 3
    else:
        snake.move()
        
        stroke(200, 200, 200)
        fill(200, 200, 200)
        text(str(snake.score), 120, 120)
        stroke(80, 80, 80)
        fill(80,80,80)
        
        for i in snake.units:
            rect(i.x, i.y, 10*snake.difficulty, 10*snake.difficulty)
        
        stroke(122, 10, 15)
        fill(122, 10, 15)
        
        rect(Apple.unit.x, Apple.unit.y, 10*snake.difficulty, 10*snake.difficulty)        
        

#instantiation of the snakes for the different modes
Snake= SNAKE(1,400,300, Appleeasy)                                                                     
Snake_new = SNAKE(1,200,400,Appleeasy) 
SnakeH = SNAKE(2,200,400,Applehard)


#this is where we check what button the player presses, up, down, left or right (w,a,s,d) and we change the direction of the snake accordingly
def keyPressed():                                                                                       
    if keyCode == UP and Snake.moveonx != 0 and Snake.moveony != 10 and SnakeH.moveonx != 0 and SnakeH.moveony != 10:
        Snake.moveonx = 0
        Snake.moveony = -10
        SnakeH.moveonx = 0
        SnakeH.moveony = -10
    if keyCode == DOWN and Snake.moveonx != 0 and Snake.moveony != -10 and SnakeH.moveonx != 0 and SnakeH.moveony != -10:
        Snake.moveonx = 0
        Snake.moveony = 10
        SnakeH.moveonx = 0
        SnakeH.moveony = 10
    if keyCode == LEFT and Snake.moveonx != 10 and Snake.moveony != 0 and SnakeH.moveonx != 10 and SnakeH.moveony != 0:
        Snake.moveonx = -10
        Snake.moveony = 0
        SnakeH.moveonx = -10
        SnakeH.moveony = 0
    if keyCode == RIGHT and Snake.moveonx != -10 and Snake.moveony  != 0 and SnakeH.moveonx != -10 and SnakeH.moveony  != 0:
        Snake.moveonx = 10
        Snake.moveony = 0
        SnakeH.moveonx = 10
        SnakeH.moveony = 0   
         
    if keyCode == 87 and Snake_new.moveonx != 0 and Snake_new.moveony != 10: #W
        Snake_new.moveonx = 0
        Snake_new.moveony = -10
    if keyCode == 83 and Snake_new.moveonx != 0 and Snake_new.moveony != -10: #S
        Snake_new.moveonx = 0
        Snake_new.moveony = 10
    if keyCode == 65 and Snake_new.moveonx != 10 and Snake_new.moveony != 0: #A 
        Snake_new.moveonx = -10
        Snake_new.moveony = 0
    if keyCode == 68 and Snake_new.moveonx != -10 and Snake_new.moveony  != 0: #D 
        Snake_new.moveonx = 10
        Snake_new.moveony = 0


def menu():
    image(loadImage("snakemenu1.jpg"), 0 , 0, 600, 600)


#the framerate is very important for the speed of the game and the responsiveness   
def setup():                                                                                               
    size(600, 600)    
    frameRate(8)
    background(100, 100, 100)
    stroke(0)
    
    #playing background music
    music.loop()                                                                                           
       
   
def draw():
    global waittime
    background(80, 80, 80)
    fill(192, 203, 41)
    stroke(0,0,0)
    
    #the playing field must be different from the background
    rect(100, 160, 400, 400)  
    
    #if somebody died we wait 3 seconds so that the player has time to read the message for the loser                                                                              
    stroke(80, 80, 80)
    time.sleep(waittime)                                                                                   
    waittime = 0
    
    #we check which mode is currently being played
    if p == 1:                                                                                            
        singleplayer(Snake, Appleeasy)
    elif p == 2:
        singleplayer(SnakeH, Applehard)
    elif p == 3:
        multiplayer(Snake, Snake_new, Appleeasy)
    #if none we display the menu
    else:                                                                                                   
        menu()
        

#it plays a big role in the menu we check where the player clicks (only) when in the menu and set the variable p accordingly
def mouseClicked():                                                                                                       
    global p
    global Snake
    global Snake_new
    global SnakeH
    x = 24
    y = 290
    z = 355-290
    t = 80 -24
    
    #if a new game is started we need new snakes
    if p == 0:
        if mouseX in range(x, x + t) and mouseY in range(y,y + z):
            Snake= SNAKE(1,300,300, Appleeasy)                                                                
            Snake_new = SNAKE(1,200,400,Appleeasy) 
            SnakeH = SNAKE(2,200,400,Applehard)
            textSize(50)
            p = 1
        if mouseX in range (300 ,300 + t) and mouseY in range (y, y + z):
            Snake= SNAKE(1,300,300, Appleeasy)
            Snake_new = SNAKE(1,200,400,Appleeasy) 
            SnakeH = SNAKE(2,200,400,Applehard)
            textSize(50)
            p = 2
        if mouseX in range (180 ,180 + t) and mouseY in range (480, 480 + z):
            Snake= SNAKE(1,300,300, Appleeasy)
            Snake_new = SNAKE(1,200,400,Appleeasy) 
            SnakeH = SNAKE(2,200,400,Applehard)
            textSize(35)
            p = 3



