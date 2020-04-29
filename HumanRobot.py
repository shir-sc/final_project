import Game_Qlearning
import cellular

class HumanRobot(cellular.Agent):
    def __init__(self, ball):
        self.R_cell_y = 5
        self.R_cell_x = 19
        self.boundLine = 18
        self.ball = ball


    def color(self):
        return 'green'


    def update(self):
        gameOver = self.IsGameOver()
        if gameOver:
            self.reset()
        else:
            self.ChooseAndTakeAction()
            self.checkMesirot()
        self.cell = self.world.getCell(self.R_cell_x, self.R_cell_y)         # printing the robot in the game (x,y)--> grid[y,x]

    def checkMesirot(self):
        # Reached a cell that the ball is in. good score incremented
        if [self.R_cell_x, self.R_cell_y] == [self.ball.x_cell, self.ball.y_cell]:
            Game_Qlearning.NumberOfMesirot += 1
            print ('human: '+ str(Game_Qlearning.NumberOfMesirot))
            return

    def ChooseAndTakeAction (self):
        if self.R_cell_x == 18:
            self.R_cell_x = 19 #---------???? Maybe it should be 19 or 17????_______
        self.R_cell_y = 5 # in this game the human Robot is always in the middle position
        if self.ball.x_cell==18: # ---------???? Maybe it should be 19????_______
            if self.ball.y_cell ==4 or self.ball.y_cell ==5 or self.ball.y_cell ==6:
                self.R_cell_x=self.ball.x_cell
                self.R_cell_y=self.ball.y_cell

    def reset (self):
        self.ball.randomRelocate()
        self.R_cell_y = 5
        self.R_cell_x = 19
        Game_Qlearning.NumberOfMesirot = 0

    def IsGameOver(self):
        # If the ball is in the next to leftmost column of the board.
        # round over
        # Need to relocate the ball in a new random location.
        if self.ball.x_cell == self.boundLine:
            return True
        return False