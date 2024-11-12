import pygame
import math
import random
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from RobotPredictor import RobotPredictor

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
FPS = 60
robotReadingFPS = 10
ROBOT_SIZE = 20
MAX_SPEED = 5.0  # Maximum speed
ACCELERATION_FACTOR = 0.1  # Acceleration rate
DECELERATION = 0.92  # Deceleration rate

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Set up display
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Robot Prediction Simulation")
clock = pygame.time.Clock()

# Initialize robots
robotToPredictPos = [400, 300]  # Starting position for target robot
ourRobotPos = [200, 300]  # Starting position for predictor robot

robotToPredictLocations = []  # Stores the robot to predict's locations

# Initialize predictor
predictor = RobotPredictor(robotReadingFPS)

frame_counter = 0

coefficients = None

changeX, changeY = 0, 0
accelX, accelY = 0, 0

time_step = 2 # amout of time to go ahead by

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Set the acceleration value.
            if event.key == pygame.K_LEFT:
                accelX = -.2
                
            elif event.key == pygame.K_RIGHT:
                accelX = .2
                
            elif event.key == pygame.K_UP:
                accelY = -.2
                
            elif event.key == pygame.K_DOWN:
                accelY = .2
                
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                accelX = 0
            
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                accelY = 0

    changeX += accelX  # Accelerate X value
    changeY += accelY  # Accelerate Y value
    
    if abs(changeX) >= MAX_SPEED:  # If max_speed is exceeded.
        # Normalize the changeX and multiply it with the max_speed.
        if changeX != 0:
            changeX = changeX / abs(changeX) * MAX_SPEED

        if changeY != 0:  # Check to avoid division by zero
            changeY = changeY / abs(changeY) * MAX_SPEED

    # Decelerate if no key is pressed.
    if accelX == 0:
        changeX *= DECELERATION
    if accelY == 0:
        changeY *= DECELERATION

    robotToPredictPos[0] += changeX  # Move the object.
    robotToPredictPos[1] += changeY

    # Store target position
    robotToPredictLocations.append((robotToPredictPos[0], robotToPredictPos[1]))

    # Keep only the last 10 positions for prediction
    if len(robotToPredictLocations) > 10:
        robotToPredictLocations.pop(0)

    screen.fill(WHITE)

    # Draw target robot (red)
    pygame.draw.circle(screen, RED, 
                      (int(robotToPredictPos[0]), int(robotToPredictPos[1])), 
                      ROBOT_SIZE)

    # Predict the next position of the target robot
    frame_counter += 1
    if frame_counter >= (FPS // robotReadingFPS) and predictor.able_to_predict(robotToPredictLocations):  # Every 6 frames at 60 FPS
        frame_counter = 0
        coefficients = predictor.predict(location=ourRobotPos, otherRobotLocations=robotToPredictLocations, timeStep=2)
        coefficientA, coefficientB, coefficientC, predictedRobotPosition = coefficients[0][0], coefficients[0][1], coefficients[0][2], coefficients[1]
        robotToPredictXValues = predictor.return_xy_values()[0]
        robotToPredictYValues = predictor.return_xy_values()[1]

        for i in range(len(robotToPredictXValues) - 1):
            pygame.draw.line(screen, GREEN, 
                             (robotToPredictPos[0], robotToPredictPos[1]),
                             (predictedRobotPosition[0], 4), 3)




    # Draw predictor robot (blue) after the prediction
    pygame.draw.circle(screen, BLUE, 
                      (int(ourRobotPos[0]), int(ourRobotPos[1])), 
                      ROBOT_SIZE)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
