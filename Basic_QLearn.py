import random
import numpy as np


class BasicQLearn:
    # The constructor of the qlearn object, being used or initialized
    # in the robot.ai parameter (game q learning and find max
    def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9):
        self.q_table = {} #Dictionary {key: (state,action), value: Q value}
        self.epsilon = epsilon
        self.alpha = alpha #learning rate
        self.gamma = gamma
        self.actions = actions #range (6)


    # returns the value of (state,action) key
    #If there is no such state and action return 0.0
    def getQValue(self, state, action):
        return self.q_table.get((state, action), 0.0)


    # Choose the next action, being called from 'update' function
    # in game q learning and find max
    def chooseAction(self, state):
        if np.random.uniform(0, 1) <= self.epsilon:
            # random action
            return np.random.choice(self.actions)
        else:
            # greedy action
            values = {}
            for a in self.actions:
                value = self.getQValue(state, a)
                values[a] = value
            return np.random.choice([k for k, v in values.items() if v==max(values.values())])

    # Being called with: last state, last action,reward and state
    # from game_Qlearning and find max
    def updateQTable(self, state, action, reward, newState):
        # in the new state we check the new Qvalue:
        # the max Q_value out of all actions from the new state
        maxQNewState = max([self.getQValue(newState, a) for a in self.actions])
        value = reward + self.gamma*maxQNewState   # Update the value according to maxqnew
        # Update the *last* q (state, action)
        # according to the new value

        # update the values in q-table
        oldv = self.q_table.get((state, action), None)  # If there is no such state and action return None
        if oldv is None:  # if it is the first time assign the reward
            self.q_table[(state, action)] = reward
        else:  # if it is not the first time, update the value with this formula
            self.q_table[(state, action)] = oldv + self.alpha * (value - oldv)


    # Set the state of the robot (Ball x cell, Ball y cell, ball velocity, ball angle, robot position)
    # The robot pos is calculated in consideration that there is 3 robot location on the y Axis
    def calcState(self, robot, ball):
        robotPos = int((3 * (robot.R_cell_y - 1)) / 9)
        return (ball.x_cell - 1, ball.y_cell-1), ball.va_categorial, ball.vd_categorial, robotPos







    # Used for debugging
    def printQ(self):
        keys = self.q_table.keys()
        states = list(set([a for a,b in keys]))
        actions = list(set([b for a,b in keys]))
        
        dstates = ["".join([str(int(t)) for t in list(tup)]) for tup in states]
        print (" "*4) + " ".join(["%8s" % ("("+s+")") for s in dstates])
        for a in actions:
            print ("%3d " % (a)) + \
                " ".join(["%8.2f" % (self.getQValue(s, a)) for s in states])

    # Used for debugging
    def printV(self):
        # get the (x,y) coordinates of the states
        keys = self.q_table.keys()
        states = [a for a,b in keys]
        statesX = list(set([x for x,y in states]))
        statesY = list(set([y for x,y in states]))

        print (" "*4) + " ".join(["%4d" % (s) for s in statesX])
        for y in statesY:
            maxQ = [max([self.getQValue((x, y), a) for a in self.actions])
                    for x in statesX]
            print ("%3d " % (y)) + " ".join([ff(q,4) for q in maxQ])


def ff(f,n):
    fs = "{:f}".format(f)
    if len(fs) < n:
        return ("{:"+n+"s}").format(fs)
    else:
        return fs[:n]
    # s = -1 if f < 0 else 1
    # ss = "-" if s < 0 else ""
    # b = math.floor(math.log10(s*f)) + 1
    # if b >= n:
    #     return ("{:" + n + "d}").format(math.round(f))
    # elif b <= 0:
    #     return (ss + ".{:" + (n-1) + "d}").format(math.round(f * 10**(n-1)))
    # else:
    #     return ("{:"+b+"d}.{:"+(n-b-1)+"

