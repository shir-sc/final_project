import random
import math
import numpy
import time
import cellular

'''
VAmplitude = [0,1,2,3] # Amplitude (0-20,20-40,40-60,60<) cm/s #velocity size
Angle = [0,1,2,3,4,5,6,7] # Angle (0-45,45-90,90-135,135-180,180-225,225-270,270-315,315-360) #direction
x_discrete = [0,1,2,3,4,5] # X states vector
y_discrete = [0,1,2,3,4,5,6,7,8] # Y state vector
# State = ball_x,ball_y,Vamplitude,ang,RobotState_y
'''
#parameters
X_max = 180;  # centimeters (continues)
Y_max = 90;  # centimeters (continues)
Va_max = 80  # centimeters/seconds, Angular velocity
Vd_max = 360  # degrees
damp_acceleration = -0.075  # during the motion the ball slowing down
damp_wall_hit = 0.8  # The ball losing velocity after it hit the wall
# The quantization noise large enough to neglect the other noise
sigma_x = 0
sigma_y = 0
sigma_Va_ratio = 0  # The error in the velocity is in ratio to the velocity
sigma_Vd = 0


class Ball(cellular.Agent):

    # Initializes the ball agent. arguments:
    # 1)world - An obejct of type World (defined in Cellular.py). The environment the agent operates in.
    # 2)dt - time difference
    # 3)Nx_cells - number of cells in x direction
    # 4)Ny_cells - number of cells in y direction
    # called by csv2game, by Game_Qlearning, by findMax
    def __init__(self, world, dt, Nx_cells, Ny_cells):
        self.X_max = X_max #size of the X_board in centimeters
        self.Y_max = Y_max #size of the y_board in centimeters
        self.Va_max = Va_max
        self.world = world
        self.dt = dt
        self.Nx_cells = Nx_cells
        self.Ny_cells = Ny_cells

        self.randomRelocate()

    # first location of the ball
    # called by Init method
    #called by csv2game robot.update()
    def randomRelocate(self):
        self.x_continiual = float(X_max - 1)  # in centimeters, simple start scenario
        self.y_continiual = float(random.uniform(0, Y_max))  # in centimeters
        # self.y = float(0.25*Y_max)
        self.Va = float(random.uniform(10, Va_max))
        # self.Va = float(80)
        self.Vd = float(random.uniform(120, 240))
        # self.Vd = float(180)
        self.t = 0 #representing the time which passed from the beginning of an round

    #color of the ball in the field
    def colour(self):
        return 'blue'


    # Uses kinematics equations for calculate the ball location
    def find_current_location (self):
        self.x_continiual = self.x_continiual + self.dt * self.Va * math.cos(float(self.Vd / 360) * 2 * math.pi) + random.normalvariate(0, sigma_x)  # future x location
        self.y_continiual = self.y_continiual + self.dt * self.Va * math.sin(float(self.Vd / 360) * 2 * math.pi) + random.normalvariate(0, sigma_y)  # future y location
        self.Va = math.exp(damp_acceleration * self.dt) * self.Va + random.normalvariate(0, sigma_Va_ratio * self.Va)  # future Vd velocity
        self.Vd = self.Vd + random.normalvariate(0, sigma_Vd)  # future Vd direction
        self.t = self.t + self.dt #the time that passed from the beginning of the maaracha

    # fixing the location of the ball such that it remains in the field
    # And updates the location of the ball in the game
    # called by new_locate method
    def fix_location(self):
        if (self.x_continiual > X_max) or (self.x_continiual < 0):  # Handling wall collision at x direction
            self.x_continiual = X_max - self.x_continiual % X_max #change the location on X axis
            self.Vd = 180 - (self.Vd % 180) + (self.Vd - self.Vd % 180) #change the direction of the velocity - mirror direction fix
            self.Va = damp_wall_hit * self.Va # change the size of the the velocity
        if (self.y_continiual > Y_max) or (self.y_continiual < 0):  # Handling wall collision at y direction
            self.y_continiual = Y_max - self.y_continiual % Y_max #change the location on Y axis
            self.Vd = -self.Vd % 360 #change the direction of the velocity - mirror direction fix
            self.Va = damp_wall_hit * self.Va  # change the size of the the velocity


    # Convert from continual cordinates to discrete cordinates
    def convert_continious_to_discrete(self):
        self.x_discrete = int(self.Nx_cells * (self.x_continiual / X_max))
        self.y_discrete = int(self.Ny_cells * (self.y_continiual / Y_max))
        self.vd_categorial = int(float(8 * self.Vd) / 360) #directions
        if self.Va < 60:
            self.va_categorial = int((3 * self.Va) / 60) #size/amplitude
        else:
            self.va_categorial = 3


    #called by world.update
    #called by cellular.activate
    def update(self):
        # If the time difference between two steps is too long in compare to the size of
        # the court divided by the ball maximal velocity, prints an error message
        if self.dt > min(Y_max, X_max) / Va_max:
            print
            "Error: too long self.dt - The simulation will be with problems"
            return
        #Else:
        self.find_current_location()
        self.fix_location() #of the current location, for edge cases
        self.convert_continious_to_discrete() # The converted values used only in cases of: isTileCoding = False
        # updating x_cell, y_cell for locating the ball in the board
        self.x_cell = self.x_discrete + 1
        self.y_cell = self.y_discrete + 1
        self.cell = self.world.getCell(self.x_cell, self.y_cell)  # This command relocate the ball in the board during the game
