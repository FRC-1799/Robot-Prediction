import pygame
import math
import random
from RobotPredictor import RobotPredictor

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
FPS = 60
robotReadingFPS = 10
ROBOT_SIZE = 20
MAX_SPEED = 5.0  # Maximum speed
ACCELERATION = 0.1  # Acceleration rate
DECELERATION = 0.05  # Deceleration rate
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
target_robot_pos = [400, 300]  # Starting position for target robot
predictor_robot_pos = [200, 300]  # Starting position for predictor robot
target_velocity = [0, 0]  # Add velocity vector
target_acceleration = [0, 0]
current_speed = 0
change_direction_counter = 0
turning_state = "accelerating"  # States: "accelerating", "decelerating", "turning"
next_angle = 0  # Store the next angle to turn to
target_positions = []  # Store target robot positions

# Initialize predictor
predictor = RobotPredictor(robotReadingFPS)

# Add near the other initializations
frame_counter = 0
last_prediction = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # State machine for movement
    if turning_state == "accelerating":

        
        # Accelerate in current direction
        current_speed = min(current_speed + ACCELERATION, MAX_SPEED)
        if change_direction_counter >= DIRECTION_CHANGE_INTERVAL:
            turning_state = "decelerating"
            next_angle = math.radians(random.randint(0, 360))
            change_direction_counter = 0
    
    elif turning_state == "decelerating":

        # Decelerate until slow enough to turn
        current_speed = max(current_speed - DECELERATION, 0)
        if current_speed <= TURN_SPEED_THRESHOLD:
            turning_state = "turning"
    
    elif turning_state == "turning":
        # Change direction and start accelerating again
        target_velocity[0] = math.cos(next_angle)
        target_velocity[1] = math.sin(next_angle)
        turning_state = "accelerating"

    # Update velocity and position
    target_robot_pos[0] += target_velocity[0] * current_speed
    target_robot_pos[1] += target_velocity[1] * current_speed
    
    # Keep robot within screen bounds (with bounce)
    if target_robot_pos[0] < ROBOT_SIZE:
        target_robot_pos[0] = ROBOT_SIZE
        target_velocity[0] *= -1
    elif target_robot_pos[0] > WINDOW_SIZE[0] - ROBOT_SIZE:
        target_robot_pos[0] = WINDOW_SIZE[0] - ROBOT_SIZE
        target_velocity[0] *= -1
    if target_robot_pos[1] < ROBOT_SIZE:
        target_robot_pos[1] = ROBOT_SIZE
        target_velocity[1] *= -1
    elif target_robot_pos[1] > WINDOW_SIZE[1] - ROBOT_SIZE:
        target_robot_pos[1] = WINDOW_SIZE[1] - ROBOT_SIZE
        target_velocity[1] *= -1

    change_direction_counter += 1

    # Store target position
    target_positions.append((target_robot_pos[0], target_robot_pos[1]))
    # Keep only last 10 positions for prediction
    if len(target_positions) > 10:
        target_positions.pop(0)

    # Run prediction every robotReadingFPS frames
    frame_counter += 1
    if frame_counter >= (FPS // robotReadingFPS):  # Every 6 frames at 60 FPS
        prediction = predictor.predict(
            predictor_robot_pos,
            target_positions,
            timeStep=1.5  # Predict 0.5 seconds ahead
        )
        last_prediction = prediction
        frame_counter = 0

    # Clear screen
    screen.fill(WHITE)

    # Draw target robot (red)
    pygame.draw.circle(screen, RED, 
                      (int(target_robot_pos[0]), int(target_robot_pos[1])), 
                      ROBOT_SIZE)

    # Draw predictor robot (blue)
    pygame.draw.circle(screen, BLUE, 
                      (int(predictor_robot_pos[0]), int(predictor_robot_pos[1])), 
                      ROBOT_SIZE)

    # Draw prediction point (green)
    if last_prediction:
        pygame.draw.circle(screen, GREEN, 
                          (int(last_prediction[0]), int(last_prediction[1])), 
                          ROBOT_SIZE//2)

    # Draw target's path
    if len(target_positions) > 1:
        pygame.draw.lines(screen, GREEN, False, 
                         [(int(x), int(y)) for x, y in target_positions], 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit() 