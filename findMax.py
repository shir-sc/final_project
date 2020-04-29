# Unnecessary. It is designed to test Qlearn initial parameters
# Almost everything here is a copy of the Game_Qlearning. with a for loop thar tries it all with different parameters
import cellular
import Basic_QLearn
import time
import sys
import random
import BallSimulation
import csv
import operator

startCell = None

def state2line(state): # Helping for debugging of csv2game
    lineNumber = state[0]+6*state[1]+6*9*state[2]+6*9*4*state[3]+6*9*4*8*state[4]
    return lineNumber

def clc_nextState(state, digit): # Used in nextState function, for better writing style
    for i in range(0,digit):
        state[i] = 0
    state[digit] += 1
    return state

def nextState(state): # The function compute the next state for printig his best action in the cvs file
    if state[0] < 5:
        return clc_nextState(state, 0)
    elif state[1] < 8:
        return clc_nextState(state, 1)
    elif state[2] < 3:
        return clc_nextState(state, 2)
    elif state[3] < 7:
        return clc_nextState(state, 3)
    elif state[4] < 2:
        return clc_nextState(state, 4)
    else: # the input state it the last State
        state[0] = -1
        return state

def calcReward(state,action): # Reward calculation
    ball_x = state[0]
    ball_y = state[1]
    ball_VA = state[2]
    ball_Angle = state[3]
    robot_y = state[4]
    robot_x = 0
    
    if ball_x == 1:
        ball_x = 0
    ball_y = 3*int((3*(ball_y-1))/9)+2
    if action == 0:
        if ball_y < 8:
            ball_y +=3
    elif action == 1:
        if ball_y > 2:
            ball_y -=3
    elif action == 2:
        ball_y += 0
    elif action == 3:
        ball_y += 1
        ball_x += 1
    elif action == 4:
        ball_y += 0
        ball_x += 1
    elif action == 5:
        ball_y -= 1
        ball_x += 1
    
    if [ball_x,ball_y] == [robot_x,robot_y]:
        return hitReward
    elif robot_x ==1:
        return goalReward
    elif action == 2:
        return nothingReward
    else:
        return normalReward

class Cell(cellular.Cell): # The function define the colour of the board square and the initial state of the game
    def __init__(self):
        self.wall = False
        self.robot = False

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
            
class Robot(cellular.Agent): # Robot is the the secones agent togever with ball. He learning during the game to hit the ball.
    def __init__(self,ball,userandom,useprint,epsilonIn,alphaIn,gammaIn):
        self.ai = Basic_QLearn.BasicQLearn(actions=range(6), epsilon=epsilonIn, alpha=alphaIn, gamma=gammaIn) # Q-learning (off policy)
        self.lastAction = None
        self.cell_y = 5
        self.cell_x = 0
        self.good_score = 0 # succesed in hitting the ball
        self.bad_score = 0 # fieled to hit the ball
        self.no_score =0 # the ball didn't arive to the robot
        self.ball = ball
        self.turn  = 0
        self.userandom = userandom # enable using the best policy

    def colour(self):
        return 'red'

    def update(self):
        
        self.turn +=1
        reward = self.calcReward() # reward
        state = self.calcState() # state
        if self.useprint and self.turn >0: # debugging section
            print "turn number " + str(self.turn)
            print "state = " + str(state)
            print "ball x = " + str(self.ball.x)
        action = self.ai.chooseAction(state) # Choosing the next move by the policy algorithm
        R_Action = action
        
        self.cell = self.world.getCell(self.cell_x, self.cell_y) # printing the robot in the game
        
        if self.lastAction is not None:
            self.ai.updateQTable(self.lastState, self.lastAction, reward, state) # learning
        self.lastAction = action
        self.lastState = state
        
        if self.ball.x_cell==1: # miss the ball or hit him
            self.ball.randomRelocate()
            self.cell_y = 5
            self.cell_x = 0
            self.lastAction = None
            self.turn = 0
        elif self.turn > 10: # the ball stoped before it cames to the robot range
            self.ball.randomRelocate()
            self.cell_y = 5
            self.cell_x = 0
            self.lastAction = None
            self.turn = 0
            self.no_score +=1
        else: # This section calculateing the next location of the robot
            if self.cell_x == 1:
                self.cell_x = 0
            self.cell_y = 3*int((3*(self.cell_y-1))/9)+2
            if R_Action == 0:
                if self.cell_y < 8:
                    self.cell_y +=3
            elif R_Action == 1:
                if self.cell_y > 2:
                    self.cell_y -=3
            elif R_Action == 2:
                self.cell_y += 0
            elif R_Action == 3:
                self.cell_y += 1
                self.cell_x += 1
            elif R_Action == 4:
                self.cell_y += 0
                self.cell_x += 1
            elif R_Action == 5:
                self.cell_y -= 1
                self.cell_x += 1
        
    def calcState(self): # state
        robotPos = int((3*(self.cell_y-1))/9)
        return self.ball.x_cell - 1, self.ball.y_cell-1,self.ball.VAmplitude,self.ball.Angle,robotPos
        
    def calcReward(self): # Reward calculation
        if [self.cell_x,self.cell_y] == [self.ball.x_cell,self.ball.y_cell]:
            self.good_score += 1
            return hitReward
        elif self.ball.x_cell==1:
            self.bad_score += 1
            return goalReward
        elif self.lastAction == 2:
            return nothingReward
        else:
            return normalReward


normalReward = -1 # prevent in vain moving
nothingReward = 0
goalReward = -10
hitReward = 10

''' for cheking the simulation of the ball
world = cellular.World(Cell, directions=directions, filename='simulationField.txt')
ball = BallSimulation.Ball(world,0.0416,60,30)
'''

numbers = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

initialValues = {}

for epsilon in [0.1]:
    for alpha in numbers:
        for gamma in numbers:
            directions = 4
            world = cellular.World(Cell, directions=directions, filename='soccerField.txt')
            ball = BallSimulation.Ball(world,1,6,9)
            world.addAgent(ball)
            robot = Robot(ball,True,False,epsilon,alpha,gamma) # True for ranom using, false for debugging printing
            world.addAgent(robot)

            pretraining = 500001
            for i in range(pretraining): # fast learning before the board is display
                world.update()

            robot.userandom = False # for using the best moves of the policy without gambeling

            pretraining = 100001
            for i in range(pretraining): # test the succesion per cent of the robot in hitting the ball
                if i % 100000 == 0 and i > 0:
                    succesionValue = (100*(robot.good_score))/(robot.good_score+robot.bad_score+robot.no_score)
                    line2print = ["epsilon = " + str(epsilon) + ' alpha = ' + str(alpha) + ' gamma = ' + str(gamma) +
                    " : good score: " + str(succesionValue)+"%"]
                    print line2print
                    robot.good_score = 0
                    robot.bad_score = 0
                    robot.no_score = 0
                world.update()
            
            initialValues[(epsilon,alpha,gamma)] = succesionValue

max_initialValue = max(initialValues.iteritems(), key=operator.itemgetter(1))[0]

print max_initialValue
print initialValues[max_initialValue]
print ''
print initialValues






