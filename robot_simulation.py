import pygame
import math
import random
from RobotPredictor import RobotPredictor
from AccuracyCheck import AccuracyCheck  # Import the AccuracyCheck class

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
FPS = 60
robotReadingFPS = 10
ROBOT_SIZE = 20
PREDICTION_SIZE = ROBOT_SIZE
MAX_SPEED = 5.0  # Maximum speed
ACCELERATION_FACTOR = 0.1  # Acceleration rate
DECELERATION = 0.92  # Deceleration rate
TURN_SPEED_THRESHOLD = 1.0  # Speed threshold before turning
DIRECTION_CHANGE_INTERVAL = 120  # Increased to allow time for deceleration

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
robotToPredictPos = [0, 0]  # Starting position for target robot
ourRobotPos = [200, 300]  # Starting position for predictor robot

change_direction_counter = 0
robotToPredictLoations = []  # Stores the robot to predict's locations

# Initialize predictor and accuracy check
predictor = RobotPredictor(robotReadingFPS)
accuracy_check = AccuracyCheck(ourRobotPos)  # Create an instance of AccuracyCheck

# Add near the other initializations
frame_counter = 0
last_prediction = None

changeX, changeY = 0, 0
accelX, accelY = 0, 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Set the acceleration value.
            if event.key == pygame.K_LEFT:
                accelX = -.2
                
            if event.key == pygame.K_RIGHT:
                accelX = .2
                
            if event.key == pygame.K_UP:
                accelY = -.2
                
            if event.key == pygame.K_DOWN:
                accelY = .2
                
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                accelX = 0
            
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                accelY = 0

    changeX += accelX  # Accelerate X value
    changeY += accelY  # Accelerate Y value
    
    if abs(changeX) >= MAX_SPEED:  # If max_speed is exceeded.
        # Normalize the changeX and multiply it with the max_speed.
        if changeX != 0:
            changeX = changeX / abs(changeX) * MAX_SPEED
    
    if abs(changeY) >= MAX_SPEED:
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
    robotToPredictLoations.append((robotToPredictPos[0], robotToPredictPos[1])) #change this to a list of tuples for multiple robots. Will affect predictor code
    # Keep only last 10 positions for prediction
    if len(robotToPredictLoations) > 10:
        robotToPredictLoations.pop(0)

    # Run prediction every robotReadingFPS frames
    frame_counter += 1
    if frame_counter >= (FPS // robotReadingFPS):  # Every 6 frames at 60 FPS
        prediction = predictor.predict(ourRobotPos, robotToPredictLoations, timeStep=1.5) # Predict 1.5 seconds ahead
        last_prediction = prediction
        frame_counter = 0

    # Clear screen
    screen.fill(WHITE)

    # Draw target robot (red)
    pygame.draw.circle(screen, RED, 
                      (int(robotToPredictPos[0]), int(robotToPredictPos[1])), 
                      ROBOT_SIZE)

    # Draw predictor robot (blue)
    pygame.draw.circle(screen, BLUE, 
                      (int(ourRobotPos[0]), int(ourRobotPos[1])), 
                      ROBOT_SIZE)

    # Draw prediction point (green)
    if last_prediction:
        pygame.draw.circle(screen, GREEN, 
                          (int(last_prediction[0]), int(last_prediction[1])), 
                          PREDICTION_SIZE)

    # Draw target's path
    if len(robotToPredictLoations) > 1:
        pygame.draw.lines(screen, GREEN, False, 
                         [(int(x), int(y)) for x, y in robotToPredictLoations], 2)

    # A* pathfinding
    if last_prediction:
        predicted_robot_position = (int(last_prediction[0]), int(last_prediction[1]))  # Use as a tuple
        target_position = (600, 300)  # Example target position
        obstacles = [predicted_robot_position]  # Create a list of obstacles

        path = accuracy_check.astar(tuple(ourRobotPos), target_position, predicted_robot_position)  # Pass obstacles as a list

        # Draw the path found by A*
        if path:
            pygame.draw.lines(screen, BLUE, False, path, 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
