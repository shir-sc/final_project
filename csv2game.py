# The script check tha the cvs file is correct, and work well

import cellular
import Basic_QLearn
import time
import sys
import random
import BallSimulation
import csv

debug = False
# lines in csv = states
#columns in csv = actions
filename = "C:/Users/roni.ravina/Desktop/wb.csv"
# reading the lines from the csv file
with open(filename, 'rb') as csvfile:
    solreader = csv.reader(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    lines = list(solreader) #returning a list of the lines from the csv
    print len(lines) #number of rows in the file
csvfile.close()

# read the best action for given state from the csv file
#called by Robot.Update
def readAction(state):
    if state2line(state) > 5148: #number of rows(=states) in csv
        print "Error: line number " +str(state2line(state)) + " > 5148" 
        print state
    line = lines[state2line(state)] #returns a specific state (a row of Qvalues)
    line = [float(i) for i in line] #returns a array of Qvalues of a specific state
    maxl = max(line) #choose the max Qvalue from the arrray
    action = line.index(maxl) #defines the action to be the one that gives the max Qvalue
    return action

# enabling computation of the corresponding line for given state
#called by readAction
def state2line(state):
    lineNumber = state[0]+6*state[1]+6*9*state[2]+6*9*4*state[3]+6*9*4*8*state[4]#hve no idea?????????????????????
    return lineNumber

#the class is descendant of the class Cell from cellular
class Cell(cellular.Cell):
    # defines the initial state of the game
    def __init__(self):
        self.wall = False
        self.robot = False

    # defines the color of the wall, robot, and the rest of the board
    def colour(self):
        if self.wall:
            return 'black'
        elif self.robot:
            return 'red'
        else:
            return 'white'

    def load(self, data):
        global startCell
        if data == 'R':
            startCell = self
        if data == '.':
            self.wall = True
            
class Robot(cellular.Agent):
    #Initialize robot in the game
    #called by csv2game
    def __init__(self,ball):
        self.cell_y = 5 # initialize robot in y=5 (the middle cell)
        self.cell_x = 0 # initialize robot in X=0
        self.good_score = 0 # succeed in hitting the ball
        self.bad_score = 0 # failed to hit the ball
        self.no_score =0 # the ball didn't arrive to the robot
        self.ball = ball
        self.turn  = 0 #initialize the turn number

    # the color of the robot in the board
    def colour(self):
        return 'red'

    def update(self):
        self.turn +=1 #increase the turn number
        state = self.calcState() #returns the state vector of the current state
        if debug and self.turn >0: # debugging section
            print "turn number " + str(self.turn)
            print "state = " + str(state)
            print "ball x = " + str(self.ball.x)
        action = readAction(state) # in this script we decided on the next action by using the csv file and choosing the action that gives the max Qvalue
        R_Action = action
        #print "action: " + str(action)
        
        self.cell = self.world.getCell(self.cell_x, self.cell_y) # returns the cell in location[y][x] in the array
        
        if self.ball.x_cell == self.cell_x and self.ball.y_cell==self.cell_y: # the robot and the ball are on the same cell = hit the ball
            self.ball.randomRelocate() #reset the ball location, velocity and time
            self.cell_y = 5 #reset the robot cell y location
            self.cell_x = 0 #reset the robot cell x location
            self.lastAction = None #reset action
            self.turn = 0 #reset the turns of the last maaracha
            self.good_score += 1
        elif self.ball.x_cell==1: # miss the ball
            self.ball.randomRelocate() #reset the ball location, velocity and time
            self.cell_y = 5
            self.cell_x = 0
            self.lastAction = None
            self.turn = 0
            self.bad_score += 1
        elif self.turn > 10: # the ball stoped before it cames to the robot range
            self.ball.randomRelocate()
            self.cell_y = 5
            self.cell_x = 0
            self.lastAction = None
            self.turn = 0
            self.no_score +=1
        else: # This section calculating the next location of the robot according to the action
            #return to basic location, if needed
            if self.cell_x == 1:
                self.cell_x = 0
            self.cell_y = 3*int((3*(self.cell_y-1))/9)+2 #calc the y

            #summary: 0->right (down), 1->left (up), 2->no movement, 3-> right diagonally, 4->straight,5-> left diagonally
            #move 3 down ->5,8
            if R_Action == 0:
                if self.cell_y < 8:
                    self.cell_y +=3
            #move 3 up ->2,5
            elif R_Action == 1:
                if self.cell_y > 2:
                    self.cell_y -=3
            #don't move
            elif R_Action == 2:
                self.cell_y += 0
            #move diagonally
            elif R_Action == 3:
                self.cell_y += 1
                self.cell_x += 1
            #move straight in x_direction
            elif R_Action == 4:
                self.cell_y += 0
                self.cell_x += 1
            #move diagonally in other direction
            elif R_Action == 5:
                self.cell_y -= 1
                self.cell_x += 1

    #calculating the state vector after the action(only x,y,robotpos are being changed)
    def calcState(self):
        robotPos = int((3*(self.cell_y-1))/9) #represents the Y value of the robot
        return self.ball.x_cell - 1, self.ball.y_cell-1,self.ball.VAmplitude,self.ball.Angle,robotPos #returns the States Vector
    #don't understand the calculation????????

directions = 4
world = cellular.World(Cell, directions=directions, filename='soccerField.txt')
ball = BallSimulation.Ball(world,1,6,9)
world.addAgent(ball)
robot = Robot(ball)
world.addAgent(robot)

print "Doing the best"


# test the success percentage of the robot in hitting the ball - the measure
pretraining = 10001
for i in range(pretraining):
    if i % 10000 == 0 and i > 0:
        line2print = ["round number: " + str(i) + '. ' + "good score: " +
        str((100*(robot.good_score))/(robot.good_score+robot.bad_score+robot.no_score))
        +"%" +". no score: " + str((100*(robot.no_score))/(robot.good_score+robot.bad_score+robot.no_score))
        +"%"+". not fail:" + str(100 - (100*(robot.bad_score))/(robot.good_score+robot.bad_score+robot.no_score))+"%"]
        print line2print
        robot.good_score = 0
        robot.bad_score = 0
        robot.no_score = 0
    world.update()
    

robot.useprint = False
world.display.activate(size=40)
world.display.delay = 0

while 1: # Showing the game in live
    world.update()
    time.sleep(1)