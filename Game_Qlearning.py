import cellular
import time
import sys
import random
import BallSimulation
import csv
import numpy as np
import LearningRobot
import HumanRobot

isTileCoding = True
NumberOfMesirot = 0

# For debugging of csv2game. given a state returns the line in the csv file
def state2line(state):
    lineNumber = state[0]+6*state[1]+6*9*state[2]+6*9*4*state[3]+6*9*4*8*state[4]
    return lineNumber

    # # This section handle the cvs file for submission
def trainTheRobot(pretraining):
    for i in range(pretraining): # fast learning before the board is display
        # print the success percentage of the robot (per 10000 round )
        if i % 100000 == 0 and i > 0:
            print("round number: " + str(i))
            print ('Good score: ' + str(LearningRobot.good_score) + ". Bad score: " + str(
                LearningRobot.bad_score) + ". No score: " + str(LearningRobot.no_score))
            print ('Good score percent: ' + str(100 * LearningRobot.good_score / (LearningRobot.no_score + LearningRobot.bad_score + LearningRobot.good_score)))
            LearningRobot.good_score = 0
            LearningRobot.bad_score = 0
            LearningRobot.no_score = 0
        world.update()

def exportToCsv():
    filename = "C:/Users/roni.ravina/Desktop/wb.csv"
    with open(filename, 'wb') as csvfile:
        solwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        row = ['0','0','0','0','0','0']
        jj=0  # runs on all possible states
        if isTileCoding:
            states = np.array(np.meshgrid([0, 1, 2, 3], [0, 1], [0, 1, 2, 3], [0, 1], [0, 1, 2, 3], [0, 1], [0, 1, 2, 3],[0, 1, 2, 3, 4, 5, 6, 7],[0, 1, 2])).T.reshape(-1, 9)
            while jj <49152:
                state = states[jj]
                for i in range(len(row)):
                    row[i] = str(LearningRobot.ai.getQValue(state=([[state[0], state[1]], [state[2], state[3]], [state[4], state[5]]], state[6], state[7], state[8]), action=i))
                solwriter.writerow(row)
                jj += 1

        else:
            states = np.array(np.meshgrid([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3], [0, 1, 2, 3, 4, 5, 6, 7],[0, 1, 2])).T.reshape(-1, 5)
            while jj < 5148:
                state = states[jj]
                for i in range(len(row)):
                    row[i] = str(LearningRobot.ai.getQValue(state= ((state[0], state[1]), state[2], state[3], state[4]), action= i))
                solwriter.writerow(row)
                jj +=1
    csvfile.close()

def diaplayGUI():
    world.display.activate(size=40)
    world.display.delay = 0

class Cell(cellular.Cell):
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
            

if __name__== '__main__':
# Initiate the parameters and the objects of the game
# Rewards, World, ball, robots
# Then, adding the robots and the ball into the world
    world = cellular.World(Cell, directions=4, filename='soccerField.txt')
    ball = BallSimulation.Ball(world, 1, 18, 9)
    world.addAgent(ball)
    LearningRobot = LearningRobot.LearningRobot(ball)
    world.addAgent(LearningRobot)
    HumanRobot = HumanRobot.HumanRobot(ball)
    # world.addAgent(HumanRobot)
    trainTheRobot(1000001)
    print ('I am trained now. Validation:')
    trainTheRobot(100001)
    # exportToCsv()
    diaplayGUI()

# Activate the game
    while 1:
        world.update()
        time.sleep(1)
