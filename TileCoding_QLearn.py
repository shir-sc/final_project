import numpy as np
import Basic_QLearn
import tile_coding
import random

class TileCodingQLearn(Basic_QLearn.BasicQLearn):
#class QValueFunction:

    def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9):
        Basic_QLearn.BasicQLearn.__init__(self, actions, epsilon, alpha, gamma)
        # Tile coding Parameters:
        # # -- Our deafault parameters   --- reached  8 percent good score:----------------------------------------------- Shir dive
        # feature_ranges = [[0, 180], [0, 90]]  # 2 features
        # number_tilings = 3
        # bins = [[4, 2], [4, 2], [4, 2]]  # each tiling has a 4*2 grid
        # offsets = [[0, 0], [15, 15], [30, 30]]  # each tiling has different offset from the 0,0


        # #three tilings 9*6 ---- reached 23
        # feature_ranges = [[0, 180], [0, 90]]  # 2 features
        # number_tilings = 3
        # bins = [[9, 6], [9, 6], [9, 6]]  # each tiling has a 4*2 grid
        # offsets = [[0, 0], [0, 0], [0, 0]]  # each tiling has different offset from the 0,0


        # tilings bigger then the field ------- reached 15-------------------------------------We like
        feature_ranges = [[-10, 180], [-10, 90]] #[[-45, 180], [-45, 90]]  # 2 features
        number_tilings = 5
        bins = [[19, 10], [19, 10], [19, 10],[19, 10],[19, 10], [19, 10]]  # each tiling has a 4*2 grid
        offsets = [[0, 0], [2, 2], [4, 4], [6,6], [8,8]]  # each tiling has different offset from the 0,0



        # tilings bigger then the field ---reached no so good 7-8
        # feature_ranges = [[-90, 180], [-45, 90]]  # 2 features
        # number_tilings = 3
        # bins = [[3, 3], [3, 3], [3, 3]]  # each tiling has a 4*2 grid
        # offsets = [[0, 0], [45, 22.5], [90, 45]]  # each tiling has different offset from the 0,0


        # reached 12~
        # feature_ranges = [[-60, 180], [-45, 90]]  # 2 features
        # number_tilings = 3
        # bins = [[4, 3], [4, 3], [4, 3]]  # each tiling has a 4*2 grid
        # offsets = [[0, 0], [20, 15], [40, 30]]  # each tiling has different offset from the 0,0


        # # -- OImpruved num_tilings in our deafault parameters   --- reached  8 percent good score:
        # feature_ranges = [[0, 180], [0, 90]]  # 2 features
        # number_tilings = 2
        # bins = [[3, 3], [3, 3]]  # each tiling has a 4*2 grid
        # offsets = [[0, 0], [90, 45]]  # each tiling has different offset from the 0,0


        # # -- Improved Our offset in deafault parameters  reached  4 percent good score: ----------------------- shir dive
        # feature_ranges = [[0, 180], [0, 90]]  # 2 features
        # number_tilings = 3
        # bins = [[4, 2], [4, 2], [4, 2]]  # each tiling has a 4*2 grid
        # offsets = [[i, j] for i, j in zip(np.linspace(0, 180, number_tilings), np.linspace(0, 90, number_tilings))]  # each tiling has different offset from the 0,0 [[0.0, 0.0], [90.0, 45.0], [180.0, 90.0]]


        # # -- Improved Our bins in deafault parameters   --- reached  ~6_ percent good score:
        # feature_ranges = [[0, 180], [0, 90]]  # 2 features
        # number_tilings = 3
        # bins = [[2, 2], [2, 2], [2, 2]]  # each tiling has a 2*2 grid
        # offsets = [[0, 0], [15, 15], [30, 30]]  # each tiling has different offset from the 0,0


        # # -- 3 tilings 2*1  --- reached ~4 percent good score
        # feature_ranges = [[0, 180], [0, 90]]  # 2 features
        # number_tilings = 3
        # bins = [[2, 1], [2, 1], [2, 1]]  # each tiling has a 4*2 grid
        # offsets = [[0, 0], [15, 15], [30, 30]]  # each tiling has different offset from the 0,0

        # # -- one tilinig 9X6  -- reached 26 percent: ---------------------- shir check small resolutons?
        # feature_ranges = [[0, 180], [0, 90]]  # 2 features
        # number_tilings = 1
        # bins = [[9, 6]]  # each tiling has a 4*2 grid
        # offsets = [[0, 0]]  # each tiling has different offset from the 0,0


        self.tilings = tile_coding.create_tilings(feature_ranges, number_tilings, bins, offsets)
        self.num_tilings = len(self.tilings)
        self.state_sizes = [tuple(len(splits) + 1 for splits in tiling)+ (4,) + (8,) + (3,) for tiling in self.tilings]  # [(4, 2), (4, 2), (4, 2)]

        self.q_tables = [np.zeros(shape=(state_size + (len(self.actions),))) for state_size in self.state_sizes]
        print (self.tilings.shape)
        print('Roni')
        print (self.tilings)

    # checked seems fine
    def getQValue (self, state, action):
        state_codings = state[0]
        action_idx = self.actions.index(action)

        value = 0
        for coding, q_table in zip(state_codings, self.q_tables):
            # for each q table
            value += q_table[tuple(coding) + (state[1],) + (state[2],) + (state[3],) +(action_idx,)]
        return value / self.num_tilings

    #checked seems fine
    def updateQTable(self, state, action, reward, newState):
        maxQNewState = max([self.getQValue(newState, a) for a in self.actions])
        value = reward + self.gamma * maxQNewState

        state_codings = state[0]
        action_idx = self.actions.index(action)

        for coding, q_table in zip(state_codings, self.q_tables):
            oldValue = q_table[tuple(coding) + (state[1],) + (state[2],) + (state[3],) + (action_idx,)]
            delta = value - oldValue
            q_table[tuple(coding) + (state[1],) + (state[2],) + (state[3],) + (action_idx,)] += self.alpha * delta

    def calcState(self, robot, ball):
        robotPos = int((3 * (robot.R_cell_y - 1)) / 9) # robot y axis, 0/1/2
        ball_coding = tile_coding.get_tile_coding((ball.x_continiual, ball.y_continiual), self.tilings)  # [[5, 1], [4, 0], [3, 0]] ...
        return ball_coding, ball.va_categorial, ball.vd_categorial, robotPos

